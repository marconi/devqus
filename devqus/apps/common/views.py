import redis
import logging
import simplejson as json
from jinja2.utils import escape
from socketio.namespace import BaseNamespace
from socketio import socketio_manage
from socketio.mixins import BroadcastMixin

from pyramid.view import view_config
from pyramid.response import Response

from .models import Message


logger = logging.getLogger('devqus')


@view_config(route_name='home', renderer='home.jinja2')
def home(request):
    return {}


@view_config(route_name='stream', request_method='GET')
def stream(request):
    headers = {'Content-Type': 'text/event-stream',
               'Cache-Control': 'no-cache'}

    body = ''
    last_msg_id = request.headers.get('Last-Event-ID', 0)
    messages = Message.objects.zfilter(mid__gt=last_msg_id).order('created')
    try:
        response_messages = []
        messages = messages[-2:]  # display only last 10 messages
        for message in messages:
            msg = ["id:%s" % message.id,
                   'data:{"body":"%s",' % message.body,
                   'data:"created":"%s",' % message.created.strftime("%H:%M:%S"),
                   'data:"author":"%s"}\n\n' % message.author]
            response_messages.append('\n'.join(msg))
        body = ''.join(response_messages)
    except IndexError:
        pass
    return Response(body=body, headers=headers)


@view_config(route_name='post', request_method='POST', renderer='json')
def post(request):
    message = Message(body=escape(request.POST.get('body', '')),
                      author=escape(request.POST.get('author', '')))
    if message.is_valid():
        message.save()
        body = {'status': 'SUCCESS'}
    else:
        body = dict(message.errors)
        body.update({'status': 'FAILED'})
    return Response(body=json.dumps(body))


class ChatNamespace(BaseNamespace, BroadcastMixin):

    def __init__(self, *args, **kwargs):
        super(ChatNamespace, self).__init__(*args, **kwargs)
        self.online_key = 'online:users'
        self.redis_db = redis.StrictRedis()

    def _broadcast_online_users(self):
        online_users = list(self.redis_db.smembers(self.online_key))
        self.broadcast_event('online-users',
                             json.dumps({'online_users': online_users}))

    def recv_connect(self):
        sorted_users = self.redis_db.sort(self.online_key, desc=True)
        if sorted_users:
            online_users_count = 0
            for user in sorted_users:
                tmp = user.split('-')
                if tmp:
                    online_users_count = int(tmp[1])
                    break
        else:
            online_users_count = 0
        self.nick = 'Anonymous-%s' % str(online_users_count + 1)
        self.redis_db.sadd(self.online_key, self.nick)
        self.emit('nick', self.nick)
        self._broadcast_online_users()

    def recv_disconnect(self):
        super(ChatNamespace, self).disconnect(silent=True)
        self.redis_db.srem(self.online_key, self.nick)
        self._broadcast_online_users()

    def on_change_nick(self, new_nick):
        self.redis_db.srem(self.online_key, self.nick)
        self.nick = new_nick
        self.redis_db.sadd(self.online_key, self.nick)
        self._broadcast_online_users()


@view_config(route_name='socketio', renderer='string')
def socketio_service(request):
    response = socketio_manage(
        request.environ, {'/stream': ChatNamespace}, request=request)
    logger.debug(response)
    return ''
