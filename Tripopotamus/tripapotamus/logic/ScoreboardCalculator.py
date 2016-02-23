from tripapotamus.models import Scoreboard

def getBoard():
    board, created = Scoreboard.objects.get_or_create()
    return board
        

def updateScoreboard(distance, price, board):
    curDist = float(board.totalDistanceTravelled)
    curMoney = float(board.totalMoneySaved)
    board.totalDistanceTravelled = curDist + distance
    board.totalMoneySaved = curMoney + price
    board.save()
