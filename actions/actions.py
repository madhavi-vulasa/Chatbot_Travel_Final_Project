import os
import openai
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker 
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv

load_dotenv()
class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_greet")
        return []

class ActionCheerUp(Action):
    def name(self) -> Text:
        return "action_cheer_up"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_cheer_up")
        dispatcher.utter_message(response="utter_did_that_help")
        return []

class ActionHappy(Action):
    def name(self) -> Text:
        return "action_happy"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_happy")
        return []

class ActionGenerateTripItinerary(Action):
    def name(self):
        return "action_generate_trip_itinerary"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):

        user_input = tracker.latest_message.get('text')
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"Generate a trip itinerary for a trip to London for 3 days: {user_input}"

        # Use the OpenAI API to generate a trip itinerary based on user input
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=100
        )
        generated_itinerary = response.choices[0].text.strip()
        # Send the generated itinerary as a response to the user
        dispatcher.utter_message(text=generated_itinerary)
        return []