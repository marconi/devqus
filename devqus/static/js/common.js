$(function() {

    var WEB_SOCKET_SWF_LOCATION = '/static/js/socketio/WebSocketMain.swf';

    $("#message-stream").scrollTo('100%', 800);
    $("#msg-input").keypress(function(e) {
        if (e.keyCode === 13) {
            var data = $(this).val().trim(),
                author = $("#nick").val().trim();

            author = (author !== "") ? author : "Anonymous";

            if (data !== "") {
                $.ajax({
                    type: "POST",
                    url: "/post",
                    data: {body: data, author: author},
                    dataType: "json",
                    beforeSend: function() {
                        $("#msg-input").val("");
                    }
                });
            }
            else {
                $(this).focus();
            }
            e.preventDefault();
        }
    });

    if (window.EventSource) {
        var stream = new EventSource('/stream');
        stream.addEventListener('message', function(e) {
            var data = JSON.parse(e.data),
                message = document.createElement('div'),
                name = document.createElement('span'),
                body = document.createElement('p');

            message.className = 'message';
            name.className = 'name';
            name.innerHTML = data.author + ' ' + data.created + ': ';
            body.innerHTML = data.body;

            message.appendChild(name);
            message.appendChild(body);
            $("#message-stream").append(message);
            $("#message-stream").scrollTo('100%');
        }, false);

        stream.addEventListener('error', function(e) {
            if (e.readyState == EventSource.CLOSED) {
                // Connection was closed.

            }
        }, false);

        stream.addEventListener('connections', function(e) {

        }, false);
    }

    $("#msg-input").focus();

});