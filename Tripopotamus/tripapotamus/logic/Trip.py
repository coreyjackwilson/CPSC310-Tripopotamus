# represents a trip.  A trip contains a vehicle object and a price in USD.

class Trip(object):
    vehicle = None
    price = 0.00

    def __init__(self, vehicle, price):
        self.vehicle = vehicle
        self.price = price

