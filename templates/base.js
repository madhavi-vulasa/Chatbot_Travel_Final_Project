var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function () {
    socket.send('User has connected!');
});

socket.on('bot_message', function (msg) {
    var messagesDiv = document.getElementById("messages");
    var messageDiv = document.createElement("div");
    messageDiv.className = "message-container";
    var botMessageDiv = document.createElement("div");
    botMessageDiv.className = "message bot-message";
    botMessageDiv.innerText = msg.message;
    messageDiv.appendChild(botMessageDiv);
    messagesDiv.appendChild(messageDiv);
});

function enterListener(event) {
    if (event.keyCode === 13) {
        var inputBox = document.getElementById("inputbox");
        var userMessage = inputBox.value;
        var messagesDiv = document.getElementById("messages");
        var messageDiv = document.createElement("div");
        messageDiv.className = "message-container";
        var userMessageDiv = document.createElement("div");
        userMessageDiv.className = "message human-message";
        userMessageDiv.style.marginLeft = "auto";
        userMessageDiv.innerText = userMessage;
        messageDiv.appendChild(userMessageDiv);
        messagesDiv.appendChild(messageDiv);
        inputBox.value = "";

        // Send the user message to the server using SocketIO
        socket.send(userMessage);
    }
}
