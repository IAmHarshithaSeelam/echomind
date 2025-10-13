$(document).ready(function () {

    // display speak message
    eel.expose(DisplayMessage)
    function DisplayMessage(message){
        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');
    }
    
    eel.expose(showHood)
    function showHood(){
        $("#Oval").attr("hidden",false);
        $("#SiriWave").attr("hidden",true);

    }

    eel.expose(senderText)
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }
    
    eel.expose(receiverText);
function receiverText(message, responseTime) {
    var chatBox = document.getElementById("chat-canvas-body");

    if (!message || message.trim() === "" || responseTime === undefined || isNaN(responseTime)) {
        console.warn("Ignored invalid message or response time:", message, responseTime);
        return;
    }

    chatBox.innerHTML += `
        <div class="row justify-content-start mb-4">
            <div class="width-size">
                <div class="receiver_message">${message}</div>
                <div class="response-time">(${responseTime}s --- response time)</div>
            </div>
        </div>`;

    chatBox.scrollTop = chatBox.scrollHeight;
}



function getCurrentLocationAndWeather() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            eel.get_weather_with_city(lat, lon);
        }, function(error) {
            console.error("Geolocation error:", error);
        });
    } else {
        console.error("Geolocation not supported.");
    }
}

getCurrentLocationAndWeather();


    

    
});