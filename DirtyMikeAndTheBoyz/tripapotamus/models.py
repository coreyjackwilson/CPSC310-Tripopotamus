from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from logic.TripEditing import deleteTrip, addTrip

class Bookmark(models.Model):
    id = models.AutoField(primary_key=True)
    startPoint = models.CharField(max_length=75, null=True)
    endPoint = models.CharField(max_length=75, null=True)
    
class Member(User):
    user = models.OneToOneField(User, blank=True)
    moneySaved = models.DecimalField(max_digits=10,decimal_places=2, default=Decimal('0.00'))
    distanceTravelled = models.DecimalField(max_digits=20,decimal_places=4, default=Decimal('0.0000'))
    averageSaved = models.DecimalField(max_digits=10,decimal_places=2, default=Decimal('0.00'))
    bookmark1_id = models.ForeignKey(Bookmark, related_name="bookmark1", blank=True, null=True, on_delete=models.SET_NULL)
    bookmark2_id = models.ForeignKey(Bookmark, related_name="bookmark2", blank=True, null=True, on_delete=models.SET_NULL)
    bookmark3_id = models.ForeignKey(Bookmark, related_name="bookmark3", blank=True, null=True, on_delete=models.SET_NULL)
    bookmark4_id = models.ForeignKey(Bookmark, related_name="bookmark4", blank=True, null=True, on_delete=models.SET_NULL)
    bookmark5_id = models.ForeignKey(Bookmark, related_name="bookmark5", blank=True, null=True, on_delete=models.SET_NULL)
    distance_street = models.BooleanField(default=False)
    distance_ocean = models.BooleanField(default=False)
    distance_marathon = models.BooleanField(default=False)
    distance_space = models.BooleanField(default=False)
    distance_denmark = models.BooleanField(default=False)
    distance_texas = models.BooleanField(default=False)
    distance_sahara = models.BooleanField(default=False)
    distance_tourdefrance = models.BooleanField(default=False)
    distance_moon = models.BooleanField(default=False)
    distance_world = models.BooleanField(default=False)
    money_1 = models.BooleanField(default=False)
    money_10 = models.BooleanField(default=False)
    money_25 = models.BooleanField(default=False)
    money_50 = models.BooleanField(default=False)
    money_100 = models.BooleanField(default=False)
    twitter_posted = models.BooleanField(default=False)
    
class Trip(Bookmark):
    user = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField(auto_now=True)
    moneySaved = models.DecimalField(max_digits=10,decimal_places=2, default=Decimal('0.00'))
    distanceTravelled = models.DecimalField(max_digits=20,decimal_places=4, default=Decimal('0.0000'))
    
    def delete(self):
        deleteTrip(self)
        super(Trip, self).delete()
        
    def create(self, *args, **kwargs):
        super(Trip, self)
        addTrip(self)
        
        

class Scoreboard(models.Model):
    totalMoneySaved = models.DecimalField(max_digits=20,decimal_places=2, default=Decimal('0.00'))
    totalDistanceTravelled = models.DecimalField(max_digits=30,decimal_places=4, default=Decimal('0.0000'))

class TaxiRate(models.Model):
    city = models.CharField(max_length=75, null=True,)
    state = models.CharField(max_length=75, null=True)
    country = models.CharField(max_length=75, null=True)
    base_fare = models.DecimalField(max_digits=20,decimal_places=2, default=Decimal('2.60'))
    distance_fare = models.DecimalField(max_digits=20,decimal_places=2, default=Decimal('2.70'))
    time_fare = models.DecimalField(max_digits=20,decimal_places=2, default=Decimal('0.50'))
    minimum_fare = models.DecimalField(max_digits=20,decimal_places=2, default=Decimal('0.00'))
    service_fee = models.DecimalField(max_digits=20,decimal_places=2, default=Decimal('0.00'))
    surge_multiplier = models.DecimalField(max_digits=20,decimal_places=2, default=Decimal('1.00'))

