##
#UserInterface
#Description: This class renders the game board through pygame library method calls
#
##
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
CELL_SIZE = (10,10)
BOARD_SIZE = (10,10)
CELL_SPACING = 10

class UserInterface:
    def __init__(self, inputSize):
        self.screen = pygame.display.set_mode(inputSize)

    def drawConstruction(self, item, position):
        Xpixel = CELL_SPACING * (position[1] + 1) + CELL_SIZE[0] * position[1]
        Ypixel = CELL_SPACING * (position[0] + 1) + CELL_SIZE[1] * position[0]
        self.screen.blit(self.constructions[item.type], (Xpixel, Ypixel))
    
    def drawAnt(self, ant, position):
        Xpixel = CELL_SPACING * (position[1] + 1) + CELL_SIZE[0] * position[1]
        Ypixel = CELL_SPACING * (position[0] + 1) + CELL_SIZE[1] * position[0]
        self.screen.blit(self.ants[ant.type], (Xpixel, Ypixel))
        
    def drawBoard(self, currentState):
        for row in xrange(0, len(currentState.board)):
            for col in xrange(0, len(currentState.board[row])):
                currentLoc = currentState.board[row][col]
                if currentLoc.constr != None:
                    self.drawConstruction(currentLoc.constr, (row, col))
                if currentLoc.ant != None:
                    self.drawAnt(currentLoc.ant, (row, col))
        for key in self.buttons:
            pass
            #drawButton(buttons[key][:2], buttons[2])
        pygame.display.flip()
    
    def initAssets(self):
        #Load textures as Surfaces.
        self.grass = pygame.image.load("grass.bmp")
        self.ants = []
        self.ants.append(pygame.image.load("ant.bmp"))
        #Make CELL_SIZE equal to the size of an ant image.
        CELL_SIZE = (self.grass.get_width(), self.grass.get_height())
        #Make White transparent (alpha 0) for all textures.
        self.grass.set_colorkey(WHITE)
        for ant in self.ants:
            ant.set_colorkey(WHITE)
        #Set up fonts.
        pygame.font.init()
        self.gameFont = pygame.font.Font(None, 25)
        #Button statistics in order: x, y, buttonState(pressed/released)
        self.buttons = {
        'move':(700,10, 1),
        'wait':(700,60, 1),
        'end':(700,110, 1),
        'tournament':(700,510, 1),
        'human':(700,540, 1),
        'ai':(700,570, 1),
        'load':(700,600, 1),
        'start':(700,650, 1)
        }
      
#Stuff that shouldn't exist in the final product.
#I'm using all this to check my drawboard method.
import GameState, Location, Inventory, Ant
a=UserInterface((760,760))
a.initAssets()
b = [[ Location.Location(True, 1, (row, col)) for col in xrange(0, BOARD_SIZE[0])] for row in xrange(0, BOARD_SIZE[1])]
b[0][0].ant = Ant.Ant(0, (0,0), 0, 0)
c = GameState.GameState(b, "inventories", "phase")

while(True):
    a.drawBoard(c)