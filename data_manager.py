import requests
# from pprint import pprint

sheety_endpoint = "https://api.sheety.co/66165be1890adf2886b5427a6b60208f/chrisFlightDeals/prices"

class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=sheety_endpoint)
        response.raise_for_status()
        response = requests.get(url=sheety_endpoint)
        response.raise_for_status()
        self.destination_data = response.json()["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{sheety_endpoint}/{city['id']}", json=new_data)
            response.raise_for_status()
            print(response.text)
