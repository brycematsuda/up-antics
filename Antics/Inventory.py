##
#Inventory
#Description: This class keeps track of the resources at a player's disposal
#
#Variables
#   player - The id of the player that this inventory belongs to
#   ants - The ants belonging to the player
#    queen - The Player's queen Ant
#    anthill - The player's anthill
#    constructions - An array of all the Player's Constructions
#   foodCount - The amount of food that the player has to use
##
class Inventory:

    ##
    #__init__
    #Description: Creates a new Inventory
    #Parameters:
    #   playerId - The id of the player that owns the Inventory (int)
    #   antArray - An array containing the Player's Ants (Ant[])
    #   inputFood - The amount of food in the Inventory (int)
    #   inputConstructions - An array containing all of the Player's Constructions (Construction[])
    ##
    def __init__(self, playerId, antArray, inputFood, inputConstructions):
        self.player = playerId
        self.ants = antArray
        self.foodCount = inputFood
        self.queen = self.findQueen(antArray)
        self.constructions = inputConstructions
        self.anthill = findAnthill(constructions)
        
    def findQueen(self, antArr):
        for checkAnt in antArr:
            if checkAnt.type == Ant.QUEEN: return checkAnt
            
        return None
