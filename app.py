from flask import request,jsonify
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import json
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_message = request.form['user_message']
        
        # Process the user message and generate a response
        response = process_user_message(user_message)  # Replace with your actual response logic
        
        # Emit the response to the client using WebSockets
        socketio.emit('bot_message', {'message': response})
        
        return jsonify({"response": response})
    
    # Return a response for GET requests
    return render_template('index.html')

def process_user_message(user_message):
    # Replace with the URL of your Rasa API
    rasa_api_url = "http://localhost:5005/webhooks/rest/webhook"
    
    # Get the Rasa API key from the environment variable
    trip_api_key = os.environ.get("TRIP_PLANNER_API_KEY")
    
    # Prepare the headers for the Rasa API request
    headers = {
        "Authorization": f"Bearer {trip_api_key}"
    }
    
    # Prepare the payload for the Rasa API request
    payload = {
        "sender": "User",
        "message": user_message
    }
    
    # Make the POST request to the Rasa API
    response = requests.post(rasa_api_url, json=payload, headers=headers)
    
    # Check if the request was successful and parse the response
    if response.status_code == 200:
        rasa_response = response.json()
        if rasa_response:
            return rasa_response[0]['text']  # Assuming Rasa returns the response in this format
    else:
        return "Sorry, I'm having trouble processing your request."

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)