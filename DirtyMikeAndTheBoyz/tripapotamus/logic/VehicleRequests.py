import jsonpickle
from tripapotamus.models import TaxiRate, Trip, Member

from VehicleRequestsHelpers import request_uber_products, make_uber_options, get_etas, get_surge_pricing, make_trips, make_trip
from Vehicle import Taxi

# return a serializable JSON array of all trip options
def get_all_trips_json(lat, lon, distance, traffic_time):
    return jsonpickle.encode(get_all_trips(lat, lon, distance, traffic_time))

# return a serializable JSON array of uber product trips
def get_uber_trips_json(lat, lon, distance, traffic_time):
    return jsonpickle.encode(get_uber_trips(lat, lon, distance, traffic_time))

# return a serializable JSON array consisting of a taxi trip
def get_taxi_trip_json(distance, traffic_time):
    return jsonpickle.encode(get_taxi_trips(distance, traffic_time))

# testing method.  returns something simple
def test_method(arg):
    return arg * 2

# returns a single array containing all possible trip options
def get_all_trips(lat, lon, distance, traffic_time):
    all_trips = []
    all_trips += get_taxi_trips(distance, traffic_time)
    all_trips += get_uber_trips(lat, lon, distance, traffic_time)
    return all_trips

# returns an array containing all trips for all available uber products
def get_uber_trips(lat, lon, distance, traffic_time):
    uber_data = request_uber_products(lat, lon)
    uber_options = make_uber_options(uber_data)
    get_etas(lat, lon, uber_options)
    get_surge_pricing(lat, lon, uber_options)
    uber_trips = make_trips(uber_options, distance, traffic_time)
    return uber_trips

# returns an array containing trip information for a taxi
def get_taxi_trips(distance, traffic_time):
    taxi_trip = []
    taxi = Taxi()
    thisTrip = make_trip(taxi, distance, traffic_time)
    taxi_trip.append(thisTrip)
    return taxi_trip

def get_last_three(user):
    userTrips = Trip.objects.filter(user=user).order_by('time')
    last3 = userTrips[:3]
    return jsonpickle.encode(last3)

def get_leaderboard():
    allUsers = Member.objects.filter().order_by('averageSaved')
    top5 = allUsers[:5]
    return jsonpickle.encode(top5)