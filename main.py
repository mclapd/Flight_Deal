from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "SYD"

data = DataManager()
sheet_data = data.get_destination_data()
notification_manager = NotificationManager()
flight_search = FlightSearch()

is_empty_iata_code = False


for city in sheet_data:
    if city["iataCode"] == "":
        is_empty_iata_code = True
        city["iataCode"] = flight_search.get_destination_code(city["city"])

if is_empty_iata_code:
    data.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flight.price < destination["lowestPrice"]:
        notification_manager.send_sms(
            message=f"Low price alert! Only AU${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."