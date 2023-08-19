from flask import Flask, request, jsonify
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa.core.agent import Agent
import openai
import random
import os

app = Flask(__name__)

# Replace with your model path
model_path = "path_to_your_rasa_model"

# Load Rasa model
agent = Agent.load(model_path)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class RasaAction(Action):
    def name(self) -> str:
        return "rasa_action"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Extract user message
        user_message = tracker.latest_message.get("text")

        # Send user message to Rasa model
        responses = agent.handle_text(user_message)

        # Extract and send bot response
        bot_response = responses[0]['text']
        dispatcher.utter_message(text=bot_response)

        return []

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data["message"]

    # Send user message to Rasa model
    responses = agent.handle_text(user_message)

    # Extract and return bot response
    bot_response = responses[0]['text']
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
