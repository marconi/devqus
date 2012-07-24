$(function() {

    var WEB_SOCKET_SWF_LOCATION = '/static/js/socketio/WebSocketMain.swf',
        socket = io.connect('/stream'),
        nick = null;

    socket.on('nick', function(newNick) {
        nick = newNick;
    });
    socket.on('disconnect', function() {
        console.log("disconnected!");
    });
    socket.on('online-users', function(data) {
        data = JSON.parse(data);
        console.log(data);
        if (data.online_users.length > 0) {
            $("#sidebar li").remove();
            $.each(data.online_users, function() {
                var li = document.createElement('li');
                li.innerHTML = this;
                $("#sidebar ul").append(li);
            });
        }
    });
    socket.on('error', function() {
        console.log("error!");
    });

    $("#message-stream").scrollTo('100%', 800);
    $("#msg-input").keypress(function(e) {
        if (e.keyCode === 13) {
            var data = $(this).val().trim(),
                author = $("#nick").val().trim();

            author = (author !== "") ? author : nick;
            if (author !== nick) {
                nick = author;
                socket.emit("change_nick", author);
            }

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

    // listen for incoming messages from server
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