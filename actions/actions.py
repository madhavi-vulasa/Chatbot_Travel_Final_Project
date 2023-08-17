import os
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

# Weather
class ActionAskWeather(Action):
    def name(self) -> Text:
        return "action_ask_weather"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city = tracker.latest_message['text']  # Get the city value from the user's latest message

        # Make an API call to get weather information for the city
        weather_api_url = f"https://api.example.com/weather?city={city}"
        response = requests.get(weather_api_url)

        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data.get("temperature")
            condition = weather_data.get("condition")
            response_message = f"The weather in {city} is {condition} with a temperature of {temperature}°C."
            dispatcher.utter_message(response="utter_weather_response", city=city, condition=condition, temperature=temperature)
        else:
            response_message = "Sorry, I couldn't retrieve the weather information."
            dispatcher.utter_message(response="Weather information not available", city=city)

        return []

#Trip Itinary
class ActionGenerateTripItinerary(Action):
    def name(self) -> Text:
        return "action_generate_trip_itinerary"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination_city")
        duration = tracker.get_slot("duration")


        # Make an API call to generate a travel itinerary using the provided API
        trip_planner_api_key = os.environ.get('TRIP_PLANNER_API_KEY')
        url = "https://ai-trip-planner.p.rapidapi.com/"
        headers = {
            "X-RapidAPI-Key": "trip_planner_api_key",
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

        dispatcher.utter_message(text=response_message)
        return []

# Currency Exchange
class ActionCurrencyExchangeRates(Action):
    def name(self) -> Text:
        return "action_currency_exchange_rates"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve values from slots (if needed)
        currency_type = tracker.get_slot("currency_type")  # Replace with your slot name for currency_type

        # Make an API call to fetch currency exchange rate information
        currency_exchange_api_key = os.environ.get('CURRENCY_EXCHANGE_API_KEY')
        url = "https://currency-exchange.p.rapidapi.com/listquotes"
        headers = {
            "X-RapidAPI-Key": "CURRENCY_EXCHANGE_API_KEY",
            "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            exchange_rates = response.json()
            response_message = "Here are the currency exchange rates:\n"

            for currency, rate in exchange_rates.items():
                response_message += f"{currency}: {rate}\n"
        else:
            response_message = "Sorry, I couldn't fetch currency exchange rates at the moment."

        dispatcher.utter_message(text=response_message)
        return []


#Hotelmetadata

class ActionGetHotelMetaData(Action):
    def name(self) -> Text:
        return "action_get_hotel_meta_data"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve values from slots
        destination_city = tracker.get_slot("destination_city")  # Replace with your slot name for destination

        # Make an API call to fetch hotel meta-data
        hotels_meta_api_key = os.environ.get('HOTELS_META_API_KEY')
        url = "https://hotels4.p.rapidapi.com/v2/get-meta-data"
        headers = {
            "X-RapidAPI-Key": "HOTELS_META_API_KEY",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        params = {
            "destination_city": destination_city
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            hotel_meta_data = response.json()
            # Process the hotel meta-data and create a response message
            response_message = f"Here is the hotels information for {destination_city}:\n"
            # Add relevant information from the hotel meta-data to the response_message

        else:
            response_message = f"Sorry, I couldn't fetch hotels information for {destination_city} at the moment."

        dispatcher.utter_message(text=response_message)
        return []

#Info about Destination

class ActionGetDestinationInfo(Action):
    def name(self) -> Text:
        return "action_get_destination_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve values from slots
        country = tracker.get_slot("country")  # Replace with your slot name for country
        region = tracker.get_slot("region")    # Replace with your slot name for region

        # Make an API call to fetch administrative divisions (geo data)
        destination_info_api_key = os.environ.get('DESTINATION_INFO_API_KEY')
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/adminDivisions"
        headers = {
            "X-RapidAPI-Key": "DESTINATION_INFO_API_KEY",
            "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
        }
        params = {
            "country": country,
            "region": region
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            admin_divisions_data = response.json()
            # Process the admin_divisions_data and create a response message
            response_message = f"Here is the information about {region}, {country}:\n"
            # Add relevant information from the admin_divisions_data to the response_message

        else:
            response_message = f"Sorry, I couldn't fetch information about {region}, {country} at the moment."

        dispatcher.utter_message(text=response_message)
        return []

# Flight fares

class ActionGetFlightFare(Action):
    def name(self) -> Text:
        return "action_get_flight_fare"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get values from slots
        from_city = tracker.get_slot("from_city")  # Replace with your slot name
        to_city = tracker.get_slot("to_city")  # Replace with your slot name
        travel_date = tracker.get_slot("travel_date")  # Replace with your slot name

    
        # Define API parameters
        flight_fare_api_key = os.environ.get('FLIGHT_FARE_API_KEY')
        url = "https://flight-fare-search.p.rapidapi.com/v2/flights/"
        querystring = {
            "from": from_city,
            "to": to_city,
            "date": travel_date,
            "adult": "1",
            "type": "economy",
            "currency": "USD"
        }
        headers = {
            "X-RapidAPI-Key": "FLIGHT_FARE_API_KEY",  # Replace with your actual RapidAPI Key
            "X-RapidAPI-Host": "flight-fare-search.p.rapidapi.com"
        }

        # Make the API request
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            fare_data = response.json()
            response_message = f"Here is the flight fare information:\n{fare_data}"
        else:
            response_message = "Sorry, I couldn't fetch flight fare information at the moment."

        dispatcher.utter_message(text=response_message)
        return []

