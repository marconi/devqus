import logging
import transaction
import simplejson as json
from jinja2.utils import escape

from pyramid.view import view_config
from pyramid.response import Response

from .models import DBSession, Message


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
    messages = DBSession.query(
        Message).filter(Message.id > last_msg_id).order_by(Message.created.asc())
    if not messages.count() == 0:
        response_messages = []
        for message in messages:
            msg = ["id:%s" % message.id,
                   'data:{"body":"%s",' % message.body,
                   'data:"created":"%s",' % message.created.strftime("%H:%M:%S"),
                   'data:"author":"%s"}\n\n' % message.author]
            response_messages.append('\n'.join(msg))
        body = ''.join(response_messages)
    return Response(body=body, headers=headers)


@view_config(route_name='post', request_method='POST', renderer='json')
def post(request):
    message = Message(body=escape(request.POST.get('body', '')),
                      author=escape(request.POST.get('author', '')))
    with transaction.manager:
        DBSession.add(message)
    return Response(body=json.dumps({}))
