from django.shortcuts import render;
from forms import AccountCreationForm
from models import Trip, Member, Bookmark
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from logic.VehicleRequests import get_all_trips_json
from logic.TripEditing import addTrip
from logic.AccountManagement import deleteAccount
from django.contrib import messages
from logic.AmazonRequests import *
import math
from django.db.models import Sum
from itertools import chain

def main(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                messages.add_message(request, messages.INFO, "Please enter a valid username and password",)
        else:
            messages.add_message(request, messages.INFO, "Please enter a valid username and password",)
            
    user = request.user

    if user.is_active:
        user = request.user.id

        totalDistanceSavedQuery = Trip.objects.all().filter(user=user).aggregate(Sum('distanceTravelled'))
        totalMoneySavedQuery = Trip.objects.all().filter(user=user).aggregate(Sum('moneySaved'))
        history_trips = Trip.objects.all().filter(user=user).order_by('-time')[:5]
        score_board_top_five = Member.objects.all().order_by('-averageSaved')[:5]
        score_board_user = Member.objects.filter(user=user)

        user = request.user

        user.moneySaved = totalMoneySavedQuery["moneySaved__sum"]
        user.distanceTravelled = totalDistanceSavedQuery["distanceTravelled__sum"]

        user.save()

        context_dict = {'history_trips': history_trips, 'score_board_top_five': score_board_top_five, 'score_board_user': score_board_user,}

        return render(request, 'Tripapotamus/main.html', context_dict)
    return render(request, 'Tripapotamus/main.html')

def createUser(request):
    user = AccountCreationForm(request.POST or None)

    if user.is_valid():
        user.save()
        return HttpResponseRedirect(reverse(main))
    else:
        user = AccountCreationForm()

    return render(request, 'Tripapotamus/create_user.html', {'form': user})

def about(request):
    context_dict = {'foo': 'bar'}
    return render(request, 'Tripapotamus/about.html', context_dict)


def getVehicleOptions(request):
    lat = float(request.GET['lat'])
    long = float(request.GET['long'])
    distance = float(request.GET['distance'])
    time = float(request.GET['time'])
    response = get_all_trips_json(lat, long, distance, time)
    return HttpResponse(response)

def addBookmark(request, tripID):
    user = request.user
    trips = Trip.objects.all().filter(id=tripID).filter(user=user)
    trip = trips[0]
    bookmark = Bookmark.objects.create(startPoint=trip.startPoint, endPoint=trip.endPoint)

    if user.bookmark1_id == None:
        user.bookmark1_id = bookmark
    elif user.bookmark2_id == None:
        user.bookmark2_id = bookmark
    elif user.bookmark3_id == None:
        user.bookmark3_id = bookmark
    elif user.bookmark4_id == None:
        user.bookmark4_id = bookmark
    elif user.bookmark5_id == None:
        user.bookmark5_id = bookmark
    else:
        messages.add_message(request, messages.INFO, "Please delete a bookmark",)
    user.save()

    return HttpResponseRedirect(reverse(main))

def deleteBookmark(request, bookmarkID):
    user = request.user
    if bookmarkID == 'bookmark1_id':
        user.bookmark1_id.delete()
    elif bookmarkID == 'bookmark2_id':
        user.bookmark2_id.delete()
    elif bookmarkID == 'bookmark3_id':
        user.bookmark3_id.delete()
    elif bookmarkID == 'bookmark4_id':
        user.bookmark4_id.delete()
    elif bookmarkID == 'bookmark5_id':
        user.bookmark5_id.delete()
    else:
        messages.add_message(request, messages.INFO, "No bookmark to delete",)

    return HttpResponseRedirect(reverse(main))

def deleteHistoryTrip(request, tripID):
    Trip.objects.all().filter(id=tripID).delete()
    return HttpResponseRedirect(reverse(main))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(main))

@login_required
def deactivate(request):
    user = request.user
    logout(request)
    deleteAccount(user)
    user.save()
    return HttpResponseRedirect(reverse(main))

def userDataTransfer(request):
    curr = str(request.GET['curr'])
    dest = str(request.GET['dest'])
    price = float(request.GET['price'])
    distance = float(request.GET['distance'])

    user = request.user
    
    thisTrip = Trip.objects.create(user=user, startPoint=curr, endPoint=dest, moneySaved=price, distanceTravelled=distance)
    thisTrip.save()

    addTrip(thisTrip)

    user.save()

    return HttpResponse("")


@login_required
def getAmazonProducts(request):
    user = request.user
    totalQuery = Trip.objects.all().filter(user=user).aggregate(Sum('moneySaved'))
    cents_saved = float(totalQuery["moneySaved__sum"]) * 100
    if cents_saved < 0:
        cents_saved *= -1
    if cents_saved < 1000:
        high_price = int(cents_saved)
        low_price = 10
        total_response = request_amazon_product(high_price, low_price)
        response = [total_response]
    else:
        high_price_for_low = int(math.floor(cents_saved * 0.5))
        low_price_for_low = int(math.floor(cents_saved * 0.01))
        high_price_for_high = int(cents_saved)
        low_price_for_high = int(math.floor(cents_saved * 0.75))

        low_response = request_amazon_product(high_price_for_low, low_price_for_low)
        high_response = request_amazon_product(high_price_for_high, low_price_for_high)
        response = [high_response, low_response]
    json_response = jsonpickle.encode(response)
    return HttpResponse(json_response)

