import random
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import addCoords
from AIPlayerUtils import *

##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "Chandler & Bryce's Simple Build-Attack Agent")
    

    ##
    #getPlacement
    #
    #Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        numToPlace = 0
        if currentState.phase == SETUP_PHASE_1:    # stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    if i == 0: # Placing anthill as far back as possible
                        x = random.randint(0, 9)
                        y = 0
                    elif i > 1: # Placing grass on edge of territory
                        y = 3
                        for j in range(0, 9):
                            move = (j, y)
                            if move not in moves: x = j
                    else: # Pick a random spot for tunnel but not on grass
                        x = random.randint(0, 9)
                        y = random.randint(0, 2)

                    # Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        # Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   # stuff on foe's side
            oppId = getOpponentId(self)
                
            oppConstr = getConstrList(currentState, oppId)
            oppTunnel = None
            if (oppConstr[0].type == TUNNEL):
                oppTunnel = oppConstr[0].coords
            else:
                oppTunnel = oppConstr[1].coords

            moves = []
            move = None
            tileDist = [] # List of tuples representing all distances from empty spaces to tunnel
            for x in range(0, 10):
                for y in range(6, 10):
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        steps = stepsToReach(currentState, (x, y), oppTunnel)
                        coord = (x, y)
                        tileDist.append((steps, coord))

            # Source: http://stackoverflow.com/a/3121985
            # Reason for usage: Wanted an easy way to sort a list of tuple values 
            # from highest to lowest based on the first element in the tuple.
            # (In this case, the number of steps to a coordinate given in the second tuple element)
            tileDist.sort(key=lambda tup: tup[0], reverse=True)

            # Place opponent's food in the farthest 2 distances from their tunnel
            # since that is where the first worker ant is placed
            farthestTile1 = tileDist[0]
            farthestCoord1 = farthestTile1[1]

            farthestTile2 = tileDist[1]
            farthestCoord2 = farthestTile2[1]
            
            moves.append(farthestCoord1)
            moves.append(farthestCoord2)
            return moves
        else:
            return [(0, 0)]
    
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        oppId = getOpponentId(self)
        inventories = currentState.inventories
        playerInventory = None
        oppInventory = None

        for inv in inventories:
            if inv.player == currentState.whoseTurn:
                playerInventory = inv
            elif inv.player == oppId:
                oppInventory = inv

        moves = listAllLegalMoves(currentState)
        buildMoves = listAllBuildMoves(currentState)

        ants = playerInventory.ants
        constrList = getConstrList(currentState, None)
        
        foodList = []
        storageList = []
        antCoordsList = []

        anthill = playerInventory.getAnthill()
        anthillCoords = anthill.coords
        hillTunnelList = playerInventory.getTunnels()
        hillTunnelList.append(anthill)

        enemyQueen = oppInventory.getQueen()
        enemyQueenCoords = enemyQueen.coords
        enemyAnthill = oppInventory.getAnthill()
        enemyAnthillCoords = enemyAnthill.coords
        
        if buildMoves:
            # have at least 2 worker ants to grab from 2 food sources
            if (numAnts(ants, WORKER) < 2):
                return buildMoves[0]
            # have at least 3 soldiers to attack enemy base/queen
            if (numAnts(ants, SOLDIER) < 3 and len(buildMoves) > 3):
                return buildMoves[2]

        # only get ant coordinates (don't care about other info like HP/type/etc)
        for ant in ants:
            antCoordsList.append(ant.coords)

        # Make sure constructs aren't already occupied by another ant
        for constr in constrList:
            if constr.coords not in antCoordsList and (constr.type == FOOD):
                foodList.append(constr.coords)

        for hillTunnel in hillTunnelList:
            if (hillTunnel.coords not in antCoordsList):
                storageList.append(hillTunnel.coords)

        for ant in ants:
            if ant.hasMoved: continue
            antMoveList = getAntMoveList(ant, moves)
            if ant.type != WORKER:
                if ant.type == QUEEN:
                    # Move off any anthill/food/ tunnel so other ants can use them
                    if ((ant.coords == anthillCoords) or \
                        (ant.coords in storageList) or \
                        (ant.coords in foodList)): 
                        return antMoveList[random.randint(0, len(antMoveList) - 2)]

                    for coord in listAdjacent(ant.coords):
                        if coord in antCoordsList:
                            # Trust no ant. If any are nearby, run away
                            return antMoveList[random.randint(0, len(antMoveList) - 2)]

                elif ant.type == SOLDIER:
                    if ant.coords == enemyAnthillCoords:
                        return moves[len(moves) - 1] # start capturing the enemy base by ending turn

                    stepsToQueen = stepsToReach(currentState, ant.coords, enemyQueenCoords)
                    stepsToAnthill = stepsToReach(currentState, ant.coords, enemyAnthillCoords)

                    # If queen is closer, focus attack on her. Otherwise, go towards enemy base
                    if (stepsToQueen < stepsToAnthill):
                        return getOptimalMove(currentState, enemyQueenCoords, antMoveList)
                    else:
                        return getOptimalMove(currentState, enemyAnthillCoords, antMoveList)
            else:
                bestMove = moves[random.randint(0, len(moves) - 1)] # default best move: do a random move
                for move in antMoveList:
                    for coord in move.coordList:
                        if ant.coords in move.coordList:
                        # If worker ant is near food source and not carrying food, get food.
                        # If worker ant is near anthill or tunnel and carrying food, go drop it off.
                            if ((coord in foodList and constr.coords not in antCoordsList and not ant.carrying) or \
                                (coord in storageList and constr.coords not in antCoordsList and ant.carrying)):
                                bestMove = move
                                # Otherwise, find the closest anthill/tunnel or food source
                            elif not ant.carrying:
                                closestFoodCoord = getClosestCoordInList(currentState, ant.coords, foodList)
                                bestMove = getOptimalMove(currentState, closestFoodCoord, antMoveList)
                            elif ant.carrying:
                                closestStorageCoord = getClosestCoordInList(currentState, ant.coords, storageList)
                                bestMove = getOptimalMove(currentState, closestStorageCoord, antMoveList)
                    if (len(bestMove.coordList) == 1): # ant is stuck, do a random move
                        bestMove = moves[random.randint(0, len(moves) - 1)]
                return bestMove
        return moves[len(moves) - 1] # if all ants have moved, end thy turn
    
    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        # Attack anyone in sight.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

##
#getClosestCoordInList
#Description: Finds the closest coordinate in a list to a starting source coord
#
#Parameters:
#    currentState - A clone of the current state (GameState)
#    src - the starting coordinate (an x, y tuple)
#    defList - list of x, y tuples
#
#Return: the closest coordinate as a tuple
##
def getClosestCoordInList(currentState, src, defList):
    if not defList: return src

    closest = [] 
    for dest in defList:
        steps = stepsToReach(currentState, src, dest)
        closest.append((steps, dest))

    # Sorts list from lowest to highest steps
    closest.sort(key=lambda tup: tup[0])

    closestTile = closest[0]
    closestCoord = closestTile[1]

    return closestCoord

##
# getOptimalMove
# 
# Description: Finds best move that will move ant closer to a destination coord if out of range
# 
# Parameters:
#   - currentState - copy of the currentState (GameState)
#   - dest - desired destination coord (x, y tuple)
#   - antMoveList - a list of the current ant's moves to pick from
# Returns:
#   Move that is closest to dest
##
def getOptimalMove(currentState, dest, antMoveList):
    bestOptMove = Move(MOVE_ANT, [antMoveList[0].coordList[0]], None) # default best move: staying in place
    for move in antMoveList:
        # Use the final coordinate/destination coord for each move
        bestOptSteps = stepsToReach(currentState, bestOptMove.coordList[-1], dest)
        currMoveSteps = stepsToReach(currentState, move.coordList[-1], dest)
        if currMoveSteps < bestOptSteps: # we've found a better move that takes less steps
            bestOptMove = move
    return bestOptMove

##
# getAntMoveList
#
# Description: Returns the subset of moves specific to an individual ant (except for end turn)
#
# Parameters:
#   ant - the ant whose moves we want (Ant)
#   moves - the list of all legal moves across all ants
# 
# Returns:
#   a list of Moves specific to the provided ant
##
def getAntMoveList(ant, moves):
    antMoveList = []
    for move in moves:
        if move.moveType != END and ant.coords == move.coordList[0]:
            antMoveList.append(move)
    return antMoveList

##
# numAnts
# Description: returns the current number of a given ant type in an Ant array (Ant[])
#
# Parameters:
# - ants - the array of players Ants on the field (Ant[])
# - antType - type of ant to be counted (WORKER, SOLDIER, etc. - see Constants.py)
#
# Return: num - the number of ants of the given type
##
def numAnts(ants, antType):
    num = 0
    for ant in ants:
        if (ant.type == antType):
            num += 1
    return num

##
# getOpponentId
# Description: returns opponents id (for looking up opponent-related items)
# 
# Parameters:
#   self - a reference to the current player (the opponent's id is not the current players)
# 
# Returns:
# oppId - the opponent's id
##
def getOpponentId(self):
    oppId = PLAYER_TWO

    # Switch if the "good" player is player 2
    if (self.playerId == PLAYER_TWO):
        oppId = PLAYER_ONE

    return oppId