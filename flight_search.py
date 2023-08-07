import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = YOUR_TEQUILA_API_KEY

class FlightSearch:

    def __init__(self):
        pass

    def get_destination_code(self, city_name):

        location_query_header = {
            "apikey": TEQUILA_API_KEY
        }

        location_query_params = {
            "term": city_name,
            "location_types": "city"
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", params=location_query_params, headers=location_query_header)
        # response.raise_for_status()

        data = response.json()["locations"]
        print(data[0]['code'])
        # print(f"{data[0]['name']}: {data[0]['code']}")
        # return data[0]['code']


    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):

        search_query_header = {
            "apikey": TEQUILA_API_KEY
        }

        search_query_params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 1,
            "nights_in_dst_to": 90,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "select_airlines": "JQ,TW",
            "select_airlines_exclude": True,
            "curr": "AUD"
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=search_query_params, headers=search_query_header)
        # response.raise_for_status()

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            airline=data["route"][0]["airline"],
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: Airline: {flight_data.airline}, AU${flight_data.price}, out date: {flight_data.out_date}, return date: {flight_data.return_date}")
        return flight_data