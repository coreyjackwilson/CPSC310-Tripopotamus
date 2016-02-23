def calculateMoneyBadges(activeUser):
    money = activeUser.moneySaved
    if money >= 1:
        activeUser.money_1 = True
    else:
        activeUser.money_1 = False
    if money >= 10:
        activeUser.money_1 = False
        activeUser.money_10 = True
    else:
        activeUser.money_10 = False
    if money >= 25:
        activeUser.money_10 = False
        activeUser.money_25 = True
    else:
        activeUser.money_25 = False
    if money >= 50:
        activeUser.money_25 = False
        activeUser.money_50 = True
    else:
        activeUser.money_50 = False
    if money >= 100:
        activeUser.money_50 = False
        activeUser.money_100 = True
    else:
        activeUser.money_100 = False

def calculateDistanceBadges(activeUser):
    distance = activeUser.distanceTravelled
    if distance > 0:
        activeUser.distance_street = True
    else:
        activeUser.distance_street = False
    if distance >= 6.783:
        activeUser.distance_street = False
        activeUser.distance_ocean = True
    else:
        activeUser.distance_ocean = False
    if distance >= 26.2:
        activeUser.distance_ocean = False
        activeUser.distance_marathon = True
    else:
        activeUser.distance_marathon = False
    if distance >= 62:
        activeUser.distance_marathon = False
        activeUser.distance_space = True
    else:
        activeUser.distance_space = False
    if distance >= 220:
        activeUser.distance_space = False
        activeUser.distance_denmark = True
    else:
        activeUser.distance_denmark = False
    if distance >= 660:
        activeUser.distance_denmark = False
        activeUser.distance_texas = True
    else:
        activeUser.distance_texas = False
    if distance >= 1118:
        activeUser.distance_texas = False
        activeUser.distance_sahara = True
    else:
        activeUser.distance_sahara = False
    if distance >= 2200:
        activeUser.distance_sahara = False
        activeUser.distance_tourdefrance = True
    else:
        activeUser.distance_tourdefrance = False
    if distance >= 7926:
        activeUser.distance_tourdefrance = False
        activeUser.distance_world = True
    else:
        activeUser.distance_world = False
    if distance >= 238900:
        activeUser.distance_world = False
        activeUser.distance_moon = True
    else:
        activeUser.distance_moon = False
    
