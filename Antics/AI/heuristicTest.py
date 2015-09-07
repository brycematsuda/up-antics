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
        super(AIPlayer,self).__init__(inputPlayerId, "Heuristic AI Test")
    
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
                    else: # Pick a random spot for anthill for now (not on grass)
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

            # Get opponent's anthill coordinates
            oppConstr = getConstrList(currentState, PLAYER_TWO)
            oppAnthill = None
            if (oppConstr[0].type == ANTHILL):
                oppAnthill = oppConstr[0].coords
            else:
                oppAnthill = oppConstr[1].coords

            moves = []
            move = None
            tileDist = [] # List of tuples representing all distances from empty spaces to anthill
            for x in range(0, 10):
                for y in range(6, 10):
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        steps = stepsToReach(currentState, (x, y), oppAnthill)
                        coord = (x, y)
                        tileDist.append((steps, coord))

            # http://stackoverflow.com/a/3121985 -- sorts list from highest distance to lowest
            tileDist.sort(key=lambda tup: tup[0], reverse=True)

            # Place opponent's food in the farthest 2 distances from their anthill
            # (TODO: Find a better method. The farthest 2 distances could be the shortest two to the tunnel)
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
        moves = listAllLegalMoves(currentState)
        ants = getAntList(currentState, PLAYER_ONE)
        constrList = getConstrList(currentState, None)
        foodList = []
        storageList = []

        for constr in constrList:
            if (constr.type == FOOD):
                foodList.append(constr.coords)
            elif (constr.type == TUNNEL or constr.type == ANTHILL):
                storageList.append(constr.coords)

        for ant in ants:
            if ant.hasMoved: continue
            else:
                for move in moves:
                    if move.moveType == END: continue
                    for coord in move.coordList:
                        # If worker ant is near food source and not carrying food, get food.
                        # If worker ant is near anthill or tunnel and carrying food, go drop it off.
                        if ant.coords in move.coordList and ((coord in foodList and not ant.carrying) or (coord in storageList and ant.carrying)):
                                return move
                return moves[len(moves) - 1] # last resort: end thy turn
    
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
        #Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]
