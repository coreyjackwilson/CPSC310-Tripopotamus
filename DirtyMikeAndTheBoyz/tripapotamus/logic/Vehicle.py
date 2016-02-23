from tripapotamus.models import TaxiRate

class Vehicle(object):
    name = ""
    base_fare = 0.0
    distance_fare = 0.0
    time_fare = 0.0
    minimum_fare = 0.0
    service_fee = 0.0
    surge_multiplier = 0.0

    def __init__(self, name, base_fare, minimum_fare, distance_fare, time_fare):
        self.name = name
        self.base_fare = base_fare
        self.distance_fare = distance_fare
        self.time_fare = time_fare
        self.minimum_fare = minimum_fare

    def calculate_trip_price(self, distance, traffic_time):
        trip_price = (self.base_fare + self.service_fee +
                      (traffic_time * self.time_fare) + (distance * self.distance_fare)) * self.surge_multiplier
        return max(self.minimum_fare, trip_price)

class Taxi(Vehicle):
    def __init__(self):
        Taxi = TaxiRate.objects.get(city='Seattle')
        self.name = "Taxi"
        self.base_fare = float(Taxi.base_fare)
        self.distance_fare = float(Taxi.distance_fare)
        self.time_fare = float(Taxi.time_fare)
        self.minimum_fare = float(Taxi.minimum_fare)
        self.service_fee = float(Taxi.service_fee)
        self.surge_multiplier = float(Taxi.surge_multiplier)

class UberCar(Vehicle):
    eta = 0
    surge_multiplier = 1.0

    def __init__(self, name, base_fare, service_fee, minimum_fare, distance_fare, time_fare):
        self.name = name
        self.base_fare = base_fare
        self.distance_fare = distance_fare
        self.time_fare = time_fare
        self.minimum_fare = minimum_fare
        self.service_fee = service_fee

    def set_eta(self, new_eta):
        self.eta = new_eta

    def set_surge_multiplier(self, multiplier):
        self.surge_multiplier = multiplier

    def calculate_trip_price(self, distance, traffic_time):
        trip_price = (self.base_fare + self.service_fee +
                      (traffic_time * self.time_fare) + (distance * self.distance_fare)) * self.surge_multiplier
        return max(self.minimum_fare, trip_price)

