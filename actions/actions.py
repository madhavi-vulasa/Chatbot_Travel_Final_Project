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


#Trip Itinary
class ActionGenerateTripItinerary(Action):
    def name(self) -> Text:
        return "action_generate_trip_itinerary"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        duration = tracker.get_slot("duration")


        # Make an API call to generate a travel itinerary using the provided API
        trip_planner_api_key = os.environ.get('TRIP_PLANNER_API_KEY')
        url = "https://ai-trip-planner.p.rapidapi.com/"
        headers = {
            "X-RapidAPI-Key": trip_planner_api_key,
            "X-RapidAPI-Host": "ai-trip-planner.p.rapidapi.com"
        }
        params = {
            "days": duration,
            "destination": destination
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            trip_itinerary = response.json()
            response_message = f"Sure! Here's a {duration} day trip itinerary for {destination}: {trip_itinerary}"
        else:
            response_message = "Sorry, I couldn't generate the travel itinerary at the moment."

        print("API Response Status Code:", response.status_code)  # Add this line to print the status code

        dispatcher.utter_message(response="utter_trip_itinerary_generated", trip_itinerary=response_message)
        return []
