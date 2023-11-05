import pygame  #import required modules
import time
from .constants import black, empty, boardImg, yellow, red #import constants from constants.py file
class gameGraphics: # initialize the class with required attributes
    def __init__(self, colour, board, wnd, game, menu):
        self.wndSize = 504 # size of game window
        self.wnd = wnd # game window object
        self.title = "Checkers"  # game title
        self.squareSize = self.wndSize / 8  #size of each square on the board
        self.pieceRad = self.squareSize / 4 # radius of each game piece
        self.board = board # current state of the game board
        self.initialWnd() # call method to initialize game window and board display
        self.playerColour = colour
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.won = False
        self.menu = menu
        self.message = ""
        self.game = game

    #   displays an instruction message at the beginning of the game
    def startMessage(self):
        message = "Press E to go back to start menu. Have fun!"
        self.font = pygame.font.Font("font.otf", 17)
        self.surface = self.font.render(message,True, empty)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.center = (self.wndSize / 2, self.wndSize / 2)
        pygame.draw.rect(self.wnd, yellow, ((self.wndSize / 2) - 225,(self.wndSize / 2) - 35 ,450,70))
        pygame.draw.rect(self.wnd,empty, ((self.wndSize / 2) - 225,(self.wndSize / 2) - 35 ,450,70), 5)
        self.wnd.blit(self.surface, self.surfaceRect)
        
    #   sets up the initial board and pieces positions         
    def initialWnd(self):
        self.wnd.blit(boardImg, (0,0))
        self.startMessage()
        time.sleep(3)
        self.addPieces(self.board.boardState)
        pygame.display.update()
        
    # updates the board displayed
    def updateWnd(self, board, availMoves, clickedPiece):
        self.wnd.blit(boardImg, (0,0))
        self.addPieces(self.board.boardState) # draw pieces according to board stat lis
        self.indicatePossibleMoves(availMoves, clickedPiece) #  if a piece is clicked it would draw a yellow circle at possible move
        #   displays a win message if a player won
        if self.won:
            self.winMessage(self.message)
            pygame.display.update()
            time.sleep(2)
            self.game.done = True 
        pygame.display.update()
        self.clock.tick(self.fps)
        
    #   draws the pieces
    def addPieces(self,board):
        for column in range(8):
            for row in range(8):
                if (board[row][column][0] == red) or (board[row][column][0] == black): #board[row][column][0] != white or board[row][column][0] != empty:
                    pygame.draw.circle(self.wnd, board[row][column][0], self.pieceCoords((column,row), self.pieceRad),self.pieceRad)
                    if board[row][column][1].stat == "king": #crowns all pieces if their stat is "king"
                        self.drawCrown((column,row))
                                 

    #   draws yellow circle in squares that are possible moves for a selected piece
    def indicatePossibleMoves(self, movesPos, selected):
        for pos in movesPos:
            pygame.draw.circle(self.wnd, yellow,self.pieceCoords((pos[0], pos[1]), 5), 5)

    #   draws a yellow ring on a piece to represent a king piece
    def drawCrown(self, coords):
        pygame.draw.circle(self.wnd, yellow, self.pieceCoords((coords[0],coords[1]),self.pieceRad),10,5) 
        return
    
    #   claculate coordinates of the piece based on square coordinates
    def pieceCoords(self, squareCoords, radius ):
        x = squareCoords[0] * self.squareSize + 2 * radius
        y = squareCoords[1] * self.squareSize + 2 * radius
        return (x,y)
    
    #   draw a rectangle and add text for win message
    def winMessage(self, message):
        self.message = message
        self.won = True
        self.font = pygame.font.Font("font.otf", 30)
        self.surface = self.font.render(message,True, empty)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.center = (self.wndSize / 2, self.wndSize / 2)
        pygame.draw.rect(self.wnd, yellow, ((self.wndSize / 2) - 100,(self.wndSize / 2) - 35 ,200,70))
        pygame.draw.rect(self.wnd,empty, ((self.wndSize / 2) - 100,(self.wndSize / 2) - 35 ,200,70), 5)
        self.wnd.blit(self.surface, self.surfaceRect) 