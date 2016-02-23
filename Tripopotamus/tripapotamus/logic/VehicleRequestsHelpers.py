import requests
from Vehicle import UberCar
from Trip import Trip

# makes a list of UberCar objects from an input decoded JSON string
def make_uber_options(uber_data):
    uber_options = []
    for product in uber_data["products"]:
        uber_car = make_uber_car(product)
        uber_options.append(uber_car)
    return uber_options

# makes a list of trips given vehicle options and route metrics
def make_trips(vehicle_options, distance, traffic_time):
    vehicle_trips = []
    for option in vehicle_options:
        trip = make_trip(option, distance, traffic_time)
        vehicle_trips.append(trip)
    return vehicle_trips

# makes a trip object with its vehicle option and estimated price
def make_trip(option, distance, traffic_time):
    price = option.calculate_trip_price(distance, traffic_time)
    trip = Trip(option, price)
    return trip

# converts uber product data into UberCar objects
def make_uber_car(product):
    name = product["display_name"]
    price_details = product["price_details"]
    minimum_fare = price_details["minimum"]
    base_fare = price_details["base"]
    distance_fare = price_details["cost_per_distance"]
    time_fare = price_details["cost_per_minute"]
    service_fees = get_total_service_fees(price_details)
    return UberCar(name, base_fare, service_fees, minimum_fare, distance_fare, time_fare)

# gets the total services fees for a particular uber product.
def get_total_service_fees(price_details):
    total_service_fee = 0.00
    service_fees = price_details["service_fees"]
    for serviceFee in service_fees:
        total_service_fee += serviceFee["fee"]
    return total_service_fee

def request_uber_etas(lat, lon):
    url = 'https://api.uber.com/v1/estimates/time'
    parameters = {
        'server_token': 'i4Ox_ro3BEu6WkV5_QoMfOd7LmnQdZgexFMD5LW5',  # top secret... shh! ;)
        'start_latitude': lat,
        'start_longitude': lon,
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    return data

def request_uber_products(lat, lon):
    url = 'https://api.uber.com/v1/products'
    parameters = {
        'server_token': 'i4Ox_ro3BEu6WkV5_QoMfOd7LmnQdZgexFMD5LW5',  # top secret... shh! ;)
        'latitude': lat,
        'longitude': lon,
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    return data

def request_uber_surge_pricing(lat, lon):
    url = 'https://api.uber.com/v1/estimates/price'
    parameters = {
        'server_token': 'i4Ox_ro3BEu6WkV5_QoMfOd7LmnQdZgexFMD5LW5',  # top secret... shh! ;)
        'start_latitude': lat,
        'start_longitude': lon,
        'end_latitude': lat,
        'end_longitude':lon,
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    return data

def get_etas(lat, lon, uber_options):
    eta_dict = request_uber_etas(lat, lon)
    map_etas(eta_dict, uber_options)
    return uber_options

def get_surge_pricing(lat, lon, uber_options):
    pricing_dict = request_uber_surge_pricing(lat, lon)
    map_prices(pricing_dict, uber_options)
    return uber_options

def map_prices(pricing_dict, uber_options):
    prices_list = pricing_dict['prices']
    for price in prices_list:
        for option in uber_options:
            if option.name == price['display_name']:
                option.set_surge_multiplier(price['surge_multiplier'])
    return uber_options

def map_etas(eta_dict, uber_options):
    times_list = eta_dict['times']
    for time in times_list:
        for option in uber_options:
            if option.name == time['display_name']:
                option.set_eta(time['estimate'])
    return uber_options