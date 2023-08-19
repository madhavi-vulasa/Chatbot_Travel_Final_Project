import os
import openai
import requests
import spacy
import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker 
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv
from rasa_sdk.forms import FormAction


load_dotenv()
spacy_model_name = "en_core_web_md"  # Replace with your model name if different
nlp = spacy.load(spacy_model_name)

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
    def name(self) -> Text:
        return "action_generate_trip_itinerary"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        duration = tracker.get_slot("duration")

        # Use the OpenAI API key from the environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Create a prompt for the OpenAI API
        prompt = f"Generate a trip itinerary for a trip to {destination} for {duration}:"

        # Use the OpenAI API to generate the trip itinerary
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=100
        )
        generated_itinerary = response.choices[0].text.strip()

        # Use the extracted values in the response template
        response_template = random.choice(domain["responses"]["utter_generate_trip_itinerary"])
        response = response_template.format(destination=destination, duration=duration, itinerary=generated_itinerary)
        dispatcher.utter_message(text=response)

        return []

class ActionTripForm(FormAction):
    def name(self) -> Text:
        return "action_trip_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["destination", "duration"]

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        destination = tracker.get_slot("destination")
        duration = tracker.get_slot("duration")

        # Your logic to generate the trip itinerary here

        response_template = random.choice(domain["responses"]["utter_generate_trip_itinerary"])
        response = response_template.format(destination=destination, duration=duration, itinerary="Generated Itinerary")
        dispatcher.utter_message(text=response)

        return []