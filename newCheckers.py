#imports relevant libraries
import pygame
import time
import random
import sys
import os
from checkers.constants import empty, white, red, yellow, black, boardImg, empty #imports these constants from the constants python file
from checkers.map import Map #imports the map class from this package
from checkers.game import game



# Initialize Pygame
pygame.init()

            
# Define a class called startMenu
class startMenu:
    # Initialize the class with required attributes
    def __init__(self):
        # Define the size of the starting window
        self.startWndSize = 504
        # Set up the starting window using pygame
        self.startWnd = pygame.display.set_mode((self.startWndSize,self.startWndSize))
        # Set the title of the starting window
        self.title = "Checkers"
        # Set up a clock to control the frame rate of the game
        self.clock = pygame.time.Clock()
        # Set the frame rate of the game
        self.fps = 60
        # Initialize the quit and exit flags
        self.quit = False
        self.exit = False

    #   set up initial window       
    def setWnd(self):
        # Fill the starting window with a grey colour
        self.startWnd.fill((200,200,200))
        # Set the caption of the starting window to the game title
        pygame.display.set_caption(self.title)
        # Call a function to draw the title of the game on the window
        self.drawTitle((self.startWndSize /2 ,self.startWndSize /4))
        # Call a function to draw the buttons on the window
        self.drawButtons((152,200), white)
        # Update the display of the starting window
        pygame.display.update()
        # Set the frame rate of the game
        self.clock.tick(self.fps)
        
    #   writes and positions the title 
    def drawTitle(self, (x,y)):
        font = pygame.font.Font("font.otf",80)
        textDisplay = font.render("Checkers", True, red)
        textRect = textDisplay.get_rect()
        textRect.center = (x, y)
        self.startWnd.blit(textDisplay, textRect)
        
    #   adds buttons to the star menu by drawing rectangles
    def drawButtons(self, (x,y), colour):
        pygame.draw.rect(self.startWnd, colour, (x,y,200,50))
        pygame.draw.rect(self.startWnd, colour, (x,y + 75,200,50))
        pygame.draw.rect(self.startWnd, colour, (x,y + 150,200,50))
        self.addButtonText((x,y), 200,50)
        
    #   adds text to each button (two players, easy, hard)
    def addButtonText(self, (x,y), width, height, btn = "all"):
        if btn == 1 or btn == "all":
            font = pygame.font.Font("font.otf", 20)
            firstBtn = font.render("Two players", True, empty)
            firstRect = firstBtn.get_rect()
            firstRect.center = (x + (width/2), y + (height/2))
            self.startWnd.blit(firstBtn, firstRect)
            
        if btn == 2 or btn == "all":
            font = pygame.font.Font("font.otf", 20)
            secBtn = font.render("Easy", True, empty)
            secRect = secBtn.get_rect()
            secRect.center = (x + (width/2), y + 75 + (height/2))
            self.startWnd.blit(secBtn, secRect)
            
        if btn == 3 or btn == "all":
            font = pygame.font.Font("font.otf", 20)
            thirdBtn = font.render("Hard", True, empty)
            thirdRect = thirdBtn.get_rect()
            thirdRect.center = (x + (width/2), y + 150 + (height/2))
            self.startWnd.blit(thirdBtn, thirdRect)

    #   given a mouse position, x and y coordinates of the top left corner of the first button, and the button
    #   parameters it would return the button on which button the mouse is. return 0 mouse is not
    #   on any of the buttons
    def whichBtn(self, mouse, (x,y), width, height):
        btn = 0
        xPos = mouse[0]
        yPos = mouse[1]
        if x + width > xPos > x and y + height > yPos > y:
            btn = 1
        elif x + width > xPos > x and y + height + 75 > yPos > y + 75:
            btn = 2
        elif x + width > xPos > x and y + height + 150 > yPos > y + 150:
            btn = 3
        return btn
        
    #   if mouse is on one of the buttons the function would change the button colour to yellow
    def redrawButton(self, mouse, (x,y), width, height):
        xPos = mouse[0]
        yPos = mouse[1]
        btn = self.whichBtn(mouse, (x,y), width, height) #  the button on which the mouse is
        
        if btn == 1:
            pygame.draw.rect(self.startWnd, yellow, (x,y,200,50))
            self.addButtonText((x,y), width, height,1)
        elif btn == 2:
            pygame.draw.rect(self.startWnd, yellow, (x,y + 75,200,50))
            self.addButtonText((x,y), width, height,2)
        elif btn == 3:
            pygame.draw.rect(self.startWnd, yellow, (x,y + 150,200,50))
            self.addButtonText((x,y), width, height,3)
        else:
            self.drawButtons((152,200), white)
        
    #   events loop that controls the start menu
    def Main(self, bOrW):
        mousePos = pygame.mouse.get_pos()
        self.redrawButton(mousePos, (152,200), 200, 50)
        
        for event in pygame.event.get():
            #   quits
            if event.type == pygame.QUIT:
                self.exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                #   checks if first button is clicked if it is then it would create an instance of
                #   game class with Ai = False (default) and calls runGame function to start
                #   the game
                if self.whichBtn(mousePos, (150,200), 200,50) == 1:
                    g = game(self, self.startWnd, False, 0, bOrW)
                    g.runGame()
                #   checks if second button is clicked if it is then it would create an instance of
                #   game class with Ai = True and difficulty = 0 (default) for easy mode and calls
                #   runGame function to start the game
                elif self.whichBtn(mousePos, (150,200), 200,50) == 2:
                    g = game(self, self.startWnd, True, 0, bOrW)
                    g.runGame()
                    
                #   checks if second button is clicked if it is then it would create an instance of
                #   game class with Ai = True and difficulty = 1 (hard mode) calls runGame function to
                #   start the game
                elif self.whichBtn(mousePos, (150,200), 200,50) == 3:
                    g = game(self, self.startWnd, True, bOrW)
                    g.runGame()


    # sets up window as long as self. exit is false and runs Main() as long as self.quit is false.                
    def runMain(self, bOrW): #passes in the players colout option
        while not self.exit:  
            self.setWnd()
            self.quit = False
            while not self.quit and not self.exit:
                self.Main(bOrW) #passes out the players colour option
                pygame.display.update()
        self.quitWnd()
    
    
        
    def quitWnd(self):
        pygame.quit()
        sys.exit

        
#"s = startMenu()" removed to be ran in the main menu python file
#"s.runMain()"  removed to be ran in the main menu python file
