//still i am developing this code 
const webchat = window.WebChat.create({
    customData: { language: "en" },
    socketUrl: "http://localhost:5055",  // Replace with your Flask app's server URL
    socketPath: "/socket.io/",
    title: "Rasa Bot",
    displayUnreadCount: true,
    displayTypingIndicator: true,
    openLauncherImage: "bot.png",  // Replace with your bot's image URL
    closeLauncherImage: "bot.png",  // Replace with your bot's image URL
});

document.querySelector("send-btn").addEventListener("click", () => {
    const userInput = document.querySelector("user-input").value;
    document.querySelector("user-input").value = "";
    webchat.send(userInput);
});

document.querySelector("user-input").addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        const userInput = document.querySelector("user-input").value;
        document.querySelector("#user-input").value = "";
        webchat.send(userInput);
    }
});

webchat.renderWebChat();
