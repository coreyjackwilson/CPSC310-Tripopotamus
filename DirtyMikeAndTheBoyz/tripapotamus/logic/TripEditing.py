from BadgeCalculator import calculateMoneyBadges, calculateDistanceBadges

def deleteTrip(trip):
    user = trip.user
    total = float(user.moneySaved) - float(trip.moneySaved)
    user.moneySaved = total
    totalDist = float(user.distanceTravelled) - float(trip.distanceTravelled)
    user.distanceTravelled = totalDist
    if totalDist != 0:
        user.averageSaved = total/totalDist
    else:
        user.averageSaved = 0
        
    calculateDistanceBadges(user)
    calculateMoneyBadges(user)

    user.save()
    
def addTrip(trip):
    user = trip.user
    total = float(user.moneySaved) + float(trip.moneySaved)
    user.moneySaved = total
    totalDist = float(user.distanceTravelled) + float(trip.distanceTravelled)
    user.distanceTravelled = totalDist
    if totalDist != 0:
        user.averageSaved = total/totalDist
    else:
        user.averageSaved = 0
        
    calculateDistanceBadges(user)
    calculateMoneyBadges(user)

    user.save()
    