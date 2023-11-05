import pygame
import random
from .constants import black, red
from .map import Map
from .graphics import gameGraphics

class game:
    def __init__(self, menu, wnd, Ai = True, difficulty = 0, bOrW =0): #changed default value of Ai from False to True
        # Set initial values for various attributes
        if bOrW == 0:
            self.playerColour = black
            self.aiColour =  red
        else:
            self.playerColour = red
            self.aiColour = black
        self.board = Map(self)
        self.allowedMoves = []
        self.clicked = None
        self.passed = False
        self.done = False
        self.menu = menu
        self.Ai = Ai
        self.AiTurn = False
        self.wnd = gameGraphics(self.playerColour, self.board, wnd, self.menu, self) 
        self.AiMode= difficulty
        
        
    #   This is the game loop the function detects mouse click or quit and calls other functionc accordingly
    def gameEvents(self):
        self.mousePos = pygame.mouse.get_pos()
        #   self.simpleMouse is the position of the moues in terms of simple coordinates of squares eg(0,1),(4,5)
        self.simpleMousePos = (self.mousePos[0] / self.wnd.squareSize, self.mousePos[1] / self.wnd.squareSize)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                self.menu.exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.done = True               
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.passed == False:
                    #   check if the clicked square has one of the players pieces
                    #   if it does then assign self.clicked to that mouse position
                    if ((self.board.boardState[self.simpleMousePos[1]][self.simpleMousePos[0]][1] != None) and
                        (self.board.boardState[self.simpleMousePos[1]][self.simpleMousePos[0]][0] == self.playerColour) and
                        (self.Ai == False or self.AiTurn == False)):
                        self.clicked = self.simpleMousePos
                    #   check if there is already a clicked piece and if the new clicked mouse positions is an available move for that piece
                    elif self.clicked != None and self.simpleMousePos in self.board.availableMoves(self.clicked, self.passed):
                        self.board.movePiece(self.clicked,self.simpleMousePos)
                        #   check if an attack move was made
                        if self.simpleMousePos not in self.board.diagonalSquares(self.clicked):
                            x = self.clicked[0] + (self.simpleMousePos[0] - self.clicked[0]) / 2
                            y = self.clicked[1] + (self.simpleMousePos[1] - self.clicked[1]) / 2
                            self.board.removePiece((x,y))
                            self.passed = True
                            self.clicked = self.simpleMousePos
                        else:
                            if self.Ai == True:
                                self.resetAi()
                            else:
                                self.reset()
                #   if self.passed == True (an attack move was made)
                else:
                    availMoves = self.board.availableMoves(self.clicked, self.passed)
                    if self.clicked != None and (self.simpleMousePos in availMoves):
                        #   check if a second attack move is available (double jump)
                        if self.simpleMousePos not in self.board.diagonalSquares(self.clicked):
                            self.board.movePiece(self.clicked, self.simpleMousePos)
                            x = self.clicked[0] + (self.simpleMousePos[0] - self.clicked[0]) / 2
                            y = self.clicked[1] + (self.simpleMousePos[1] - self.clicked[1]) / 2
                            self.board.removePiece((x,y))
                            self.passed = False
                            if self.Ai == True:
                                self.resetAi()
                            else:
                                self.reset()
                                
                    else:
                        if self.Ai == True:
                            self.resetAi()
                        else:
                            self.reset()
            #   check if a piece is clicked and it is the player's piece it would assign available moves to
            #   self.allowedMoves so that a yellow circle would be drawn to represent available move
            elif self.clicked != None and (self.Ai == False or self.AiTurn == False):
                self.allowedMoves = self.board.availableMoves(self.clicked, self.passed)
            
            #   easy Ai turn                
            elif self.AiTurn == True and self.AiMode == 0:
                self.AiMove()
                
            #   hard Ai turn
            elif self.AiTurn == True and self.AiMode == 1:
                self.hardAi()

    #   sets up the board and runs the game events loop until a player quits (when self.done == True)
    def runGame(self):
        self.wnd.initialWnd()

        while not self.done:
            self.gameEvents()
            self.updateGameDisplay()
        self.menu.quit = True

    #   uses function in gameGraphics class to update the scree
    def updateGameDisplay(self):
        self.wnd.updateWnd(self.board, self.allowedMoves, self.clicked)
        
    
            
    #   checks if one of the players won (run out of moves or pieces)
    def checkSomeoneWon(self): 
        for column in range(8):
            for row in range(8):
                if self.AiTurn == False and self.board.boardState[row][column][0] == self.playerColour:
                    if self.board.availableMoves((column, row), self.passed) != []:
                        return False
                if self.Ai == True and self.AiTurn == True:
                    if self.board.boardState[row][column][0] == self.aiColour: #changed from red to self.aiColour
                        if self.board.availableMoves((column, row), self.passed) != []:
                            return False
                                           
        return True

    #   returns if the given player has won or not to specifically determine which player won in Ai mode
    def whoWon(self, player):
        if player == "Ai":
            for column in range(8):
                for row in range(8):
                    if self.board.boardState[row][column][0] == self.playerColour: #changed from black to self.playerColour
                        if self.board.availableMoves((column, row), self.passed) != []:
                            return False
            return True
        
        elif player == "human":
            for column in range(8):
                for row in range(8):
                    if self.board.boardState[row][column][0] == self.aiColour: #changed from red to self.aiColour
                        if self.board.availableMoves((column, row), self.passed) != []:
                            return False
            return True
            

        
    #   loops through board stat list in board class and returns a dictionary with the key as the Ai piece
    #   and the value is list of avialble moves (moves and piece are in the form (column,row)
    def getAiPieces(self):
        pieces = dict()
        for column in range(8):
            for row in range(8):
                if self.board.boardState[row][column][0] == self.aiColour: #changed from red to self.aiColour
                    pieces[(column,row)] = []
        return pieces

    #   loops through board stat list in board class and returns a dictionary with the key as the human player
    #   piece and the value is list of avialble moves (moves and piece are in the form (column,row)
    def getPlayerPieces(self):
        pieces = dict()
        for column in range(8):
            for row in range(8):
                if self.board.boardState[row][column][0] == black:
                    pieces[(column,row)] = []
        return pieces

    #   loops through a dictionary of pieces and available moves and returns a dictionary with only the pieces
    #   that have availble moves (removes pieces that cannot move)   
    def getAiAvailMoves(self,pieces):
        updated = dict()
        for pieceCoords in pieces:
            availMoves = self.board.availableMoves(pieceCoords, self.passed)
            if availMoves != []:
                updated[pieceCoords] = availMoves
        return updated

        
    # Ai that makes a random move for the easy Ai mode
    def AiMove(self):
        #   a dictionary with pieces and available move
        AiPieces = self.getAiPieces()
        #   an updated dictionary with only pieces that have available moves
        updateAiPieces = self.getAiAvailMoves(AiPieces) 
        piecesPos = updateAiPieces.keys()
        #   check if there are pieces with available moves
        if piecesPos != []:
            #   choose a random piece
            pieceIndex = random.randint(0,len(piecesPos) - 1) 
            pieceCoords = piecesPos[pieceIndex]
            
            #   choose a random move for that piece
            moves = updateAiPieces[pieceCoords]
            whichMove = random.randint(0, len(moves) - 1)
            move = moves[whichMove]
            
            if self.passed == False:
                self.board.movePiece(pieceCoords, move)
                #   check if an attack move was made
                if move not in self.board.diagonalSquares(pieceCoords):
                    x = pieceCoords[0] + (move[0] - pieceCoords[0]) / 2
                    y = pieceCoords[1] + (move[1] - pieceCoords[1]) / 2
                    self.board.removePiece((x,y))
                    self.updateGameDisplay()
                    self.passed = True
                    pieceCoords = move
                    
                else:
                    self.resetAi()
                    
             #  after an attack move checks for another possible attack move                   
            if self.passed == True:
                AiPieces = self.getAiPieces()
                moves = AiPieces[pieceCoords]
                if moves != []:
                    whichMove = random.randint(0, len(moves) - 1)
                    move = moves[whichMove]
                    if move not in self.board.diagonalSquares(pieceCoords):
                        self.board.movePiece(pieceCoords, move)
                        x = pieceCoords[0] + (move[0] - pieceCoords[0]) / 2
                        y = pieceCoords[1] + (move[1] - pieceCoords[1]) / 2
                        self.board.removePiece((x,y))
                        self.passed = False
                        self.resetAi()
                                                   
                else:
                    self.resetAi()
   
    #   moves an Ai piece by updating board stat list in board class
    def move(self,fromCoords, toCoords):
        self.board.movePiece(fromCoords, toCoords)
        if toCoords not in self.board.diagonalSquares(fromCoords):
            x = fromCoords[0] + (toCoords[0] - fromCoords[0]) / 2
            y = fromCoords[1] + (toCoords[1] - fromCoords[1]) / 2
            self.board.removePiece((x,y))
    #   undos a move by updating boards stat list in board class (for minmax function)       
    def undoMove(self,fromPos,fromStat,toPos, enemyRemoved):
        row = fromPos[1]
        column = fromPos[0]
        
        self.board.boardState[row][column] = (fromStat[0], fromStat[1])
        self.board.removePiece(toPos)

        #   returns an enemy piece to the list if it has been removed
        if enemyRemoved != None:
            self.board.boardState[enemyRemoved[1]][enemyRemoved[0]] = (enemyRemoved[2],enemyRemoved[3])
     
            
    #   checks if a given move from (fromCoords) to (toCoords) is an attack move (for minmax function)          
    def ifJump(self,fromCoords, toCoords):
        if toCoords not in self.board.diagonalSquares(fromCoords):
            x = fromCoords[0] + (toCoords[0] - fromCoords[0]) / 2
            y = fromCoords[1] + (toCoords[1] - fromCoords[1]) / 2
            removedColor = self.board.boardState[y][x][0]
            removedStat = self.board.boardState[y][x][1]
            return [x,y,removedColor, removedStat]
        
        return None
    
    #   scores the board (for minmax function)        
    def evaluate(self, Colour):
        redNum = 0
        blackNum = 0
        redKingsNum = 0
        blackKingsNum = 0

        # Iterate over each position on the board.
        for column in range(8):
            for row in range(8):
                # Count the number of red and black pieces and kings.
                if self.board.boardState[row][column][0] == self.aiColour: #changed from red to self.aiColour
                    if self.board.boardState[row][column][1].stat == "king":
                        redKingsNum += 1
                    else:
                        redNum += 1
                if self.board.boardState[row][column][0] == self.playerColour: #changed from black to self.playerColour
                    if self.board.boardState[row][column][1].stat == "king":
                        blackKingsNum += 1
                    else:
                        blackNum += 1
        
        # Calculate the final score based on the difference in counts and weights.
        if Colour == black:
            return (blackNum - redNum) + (1.5 * (blackKingsNum - redKingsNum))
        else:
            return (redNum - blackNum) + (1.5 * (redKingsNum - blackKingsNum))

    #   makes the move determined by the minmax function for the hard Ai mode           
    def hardAi(self):
        #   if minmax return a score of either 100 or -100 then the player can make a random move
        #   since it wouldn't matter (it already won or lost)
        if isinstance (self.minMax("Ai"), int):
            AiPieces = self.getAiPieces()
            updateAiPieces = self.getAiAvailMoves(AiPieces)
            pieces = updateAiPieces.keys()
            pieceIndex = random.randint(0,len(pieces)-1)
            piece = pieces[pieceIndex]
            moves = updateAiPieces[piece]
            whichMove = random.randint(0,len(moves)-1)
            move = moves[whichMove]
        #   gets a move from minmax
        else:
            move = self.minMax("Ai")[1]
            piece = self.minMax("Ai")[0]

    
        if self.passed == False:
            self.board.movePiece(piece, move)
            #   checks if it is an attack move
            if move not in self.board.diagonalSquares(piece):
                x = piece[0] + (move[0] - piece[0]) / 2
                y = piece[1] + (move[1] - piece[1]) / 2
                self.board.removePiece((x,y))
                self.updateGameDisplay()
                self.passed = True
                piece = move
            else:
                self.resetAi()
                
        #   if an attack move was already made
        if self.passed == True:
            AiPieces = self.getAiPieces()
            moves = AiPieces[piece]
            for move in moves:
                if move not in self.board.diagonalSquares(piece):
                    self.board.movePiece(piece, move)
                    x = piece[0] + (move[0] - piece[0]) / 2
                    y = piece[1] + (move[1] - piece[1]) / 2
                    self.board.removePiece((x,y))
                    self.passed = False
                    
            self.resetAi()
                
        
    #   uses minmax algorithm to a depth of 3 to determine the best move for the Ai              
    def minMax(self, player, depth=5):
        playerPieces = self.getPlayerPieces()
        AiPieces = self.getAiPieces()
        updateAiPieces = self.getAiAvailMoves(AiPieces)
        updatedPlayerPieces = self.getAiAvailMoves(playerPieces)
        
        # key is the piece and the value is a list of tuples (move,score)
        AiMoves = dict()
        playerMoves = dict()
        
        if self.whoWon("Ai"): #changed from checkSomeoneWon to whoWon
            return 100
            
        if self.whoWon("human"): #changed from checkSomeoneWon to whoWon
            return -100
            
        if depth == 3: #finds the depth of the minimax tree
            if player =="Ai":
                return self.evaluate(self.aiColour) #changed from red to self.aiColour
                
            else:
                return self.evaluate(self.aiColour) #changed from red to self.aiColour
                
        #finds the best moeve the ai can make
        if player == "Ai":
            for piece in updateAiPieces:
                movesInfo = [] #creates a temporary tuple array
                for move in updateAiPieces[piece]:
                    originalPos = piece
                    originalStat = [self.board.boardState[piece[1]][piece[0]][0],self.board.boardState[piece[1]][piece[0]][1]]
                    enemyPieceRemoved = self.ifJump(piece,move) #can be none or [x,y,removedColour, removedStat]
                    self.move(piece,move)
                    result = self.minMax("human", depth+1)
                    if isinstance(result, tuple):
                        moveInfo = (move,result[2])
                    else:
                        moveInfo = (move,result)
                
                    movesInfo.append(moveInfo) #appends the tuple into this array
                    self.undoMove(originalPos,originalStat, move, enemyPieceRemoved)
                
                AiMoves[piece] = movesInfo

        #finds the best move that player can make
        if player == "human":
            for piece in updatedPlayerPieces:
                movesInfo = [] #resets the temporary tuple array
                for move in updatedPlayerPieces[piece]:
                    originalPos = piece 
                    originalStat = [self.board.boardState[piece[1]][piece[0]][0],self.board.boardState[piece[1]][piece[0]][1]]
                    enemyPieceRemoved = self.ifJump(piece,move) #can be none or [x,y,removedColour, removedStat]
                    self.move(piece,move)
                    result = self.minMax("Ai", depth+1)
                    if isinstance(result, tuple):
                        moveInfo = (move,result[2])
                    else:
                        moveInfo = (move,result)
                        
                    movesInfo.append(moveInfo) #appends the tuple into this array
                    self.undoMove(originalPos,originalStat, move, enemyPieceRemoved)
                    
                playerMoves[piece] = movesInfo
                
        bestMove = 0
        bestPiece = 0
        if player == "Ai":
            bestScore = -10000 #initialise bestScore
            for piece in AiMoves:
                for move in AiMoves[piece]:
                    if move[1] > bestScore:
                        bestScore = move[1]
                        bestMove = move[0]
                        bestPiece = piece
                        
        #   if player is human player
        else:
            bestScore = 10000 #initialise bestScore
            for piece in playerMoves:
                for move in playerMoves[piece]:
                    if move[1] < bestScore:
                        bestScore = move[1]
                        bestMove = move[0]
                        bestPiece = piece
        return (bestPiece, bestMove, bestScore)

    #   resets game in Ai modes and checks if someone won
    def resetAi(self):
        if self.AiTurn == False:
            self.AiTurn = True
        else:
            self.AiTurn = False
        self.passed = False
        self.clicked = None
        self.allowedMoves = []
        if self.checkSomeoneWon():
            if self.AiTurn == True:
                if self.playerColour == red:
                    self.wnd.winMessage("Red Won!") #changed from black to self.playerColour
                else:
                    self.wnd.winMessage("Black Won!")
            else:
                if self.aiColour == red:
                    self.wnd.winMessage("Red Won!") #changed from black to self.playerColour
                else:
                    self.wnd.winMessage("Black Won!") #changed from red to self.aiColour

    #   resets game for two players mode and checks if someone won using another function 
    def reset(self):
        if self.playerColour == black:
            self.playerColour = red
        else:
            self.playerColour = black
        self.passed = False
        self.clicked = None
        self.allowedMoves = []
        if self.checkSomeoneWon():
            if self.playerColour == red:
                self.wnd.winMessage("black Won!")
            else:
                self.wnd.winMessage("Red Won!")
                       
