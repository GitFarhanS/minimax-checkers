from .constants import empty, white, red, black

class pieceState:
    def __init__(self, stat = "normal"):
        self.stat = stat

class Map:
    def __init__(self, currentGame):
        self.boardState = self.initBoard()
        self.game = currentGame
#   returns a list of lists where the index of the element in outer list
#   is the column number and the index of element in inner list is row
#   number. The inner list would have the colour of the square empty or
#   white if a piece is in the square then colour would be colour of piece

    def initBoard(self):
        # Initialize a 2D array of size 8x8 with all values set to None
        colourLocation = [[None] * 8 for i in range(8)] 

        # Loop through all columns and rows in the array
        for column in range(8):
                for row in range(8):
                        # Check if the current cell should be empty or white based on its row and column index
                        if (row % 2 == 0) and (column % 2 == 0):
                                # Set the current cell to be empty
                                colourLocation[row][column] = (empty, pieceState(None))
                        elif (row % 2 != 0)  and (column % 2 != 0):
                                # Set the current cell to be empty
                                colourLocation[row][column] = (empty, pieceState(None))
                        elif (row % 2 != 0) and (column % 2 == 0):
                                # Set the current cell to be white
                                colourLocation[row][column] = (white, pieceState(None))
                        elif (row % 2 == 0) and (column % 2 != 0):
                                # Set the current cell to be white
                                colourLocation[row][column] = (white, pieceState(None))
                                
        # Call the initPieces function to add pieces to the board
        newcolourLocation = self.initPieces(colourLocation)
        return newcolourLocation

#   starting board list updates the list with colours of pieces at the start
#   of the game in indices corresponding to positions
    def initPieces(self,pos):
        for column in range(8):
                for row in range(0,3):
                        if pos[row][column][0] == empty:
                                pos[row][column] = (red, pieceState())

                for row in range(5,8):
                        if pos[row][column][0] == empty:
                                pos[row][column] = (black, pieceState())
        return pos

# returns coords of surrounding squares
    def diagonalSquares(self, (column,row)):
        x1 = column + 1 #   right
        x2 = column - 1 #   left
        y1 = row + 1    #   down
        y2 = row - 1    #   up
        moves = [(x1,y2),(x2,y2),(x1,y1),(x2,y1)] # [upper right, upper left, down right, down left]
        return moves
        
#   given position of a piece (column, row) it would return all move both allowed and not allowed
    def allMoves(self, (column,row)):
        moves = []
        if self.boardState[row][column][1].stat != None:
            
            if self.boardState[row][column][1].stat != "king" and self.boardState[row][column][0] == red:
                moves = [self.diagonalSquares((column,row))[2],self.diagonalSquares((column,row))[3]] #   [down right, down left]
                
            elif self.boardState[row][column][1].stat != "king" and self.boardState[row][column][0] == black:
                moves = [self.diagonalSquares((column,row))[0],self.diagonalSquares((column,row))[1]] #   [upper right, upper left]
                
            # if king
            else:
                moves = self.diagonalSquares((column,row)) # [upper right, upper left, down right, down left]
                
        else:
            moves = []
        
        return moves

    #   eliminate positions that are not in the board and positions that are filled by current player and add
    #   positions that allow attacking of enemy  
    def availableMoves(self, (column,row), goOver):
        moves = self.allMoves((column,row))
        allowedMoves = []
        if goOver == False:
            for move in moves:
                if self.foundOnBoard(move):
                    if self.boardState[move[1]][move[0]][1].stat == None: #  move[1] is row and move[0] is column
                        allowedMoves.append(move)
                        
                    elif self.game.Ai == True and self.game.AiTurn == True:
                        #   check for attack move
                        if self.boardState[move[1]][move[0]][0] != red: 
                            newCoords = (2 * move[0] - column, 2 * move[1] - row) # coords of attack move (column,row)
                            if self.foundOnBoard(newCoords) and self.boardState[newCoords[1]][newCoords[0]][1].stat == None:
                                allowedMoves.append(newCoords)
                                
                    #   check for attack move                      
                    elif self.boardState[move[1]][move[0]][0] != self.game.playerColour:
                        newCoords = (2 * move[0] - column, 2 * move[1] - row) # coords of attack move (column,row)
                        if self.foundOnBoard(newCoords) and self.boardState[newCoords[1]][newCoords[0]][1].stat == None:
                            allowedMoves.append(newCoords)
        else:
            for move in moves:
                if self.foundOnBoard(move):
                    if self.game.Ai == True and self.game.AiTurn == True:
                        if self.boardState[move[1]][move[0]][0] != red and self.boardState[move[1]][move[0]][1].stat != None:
                            newCoords = (2 * move[0] - column, 2 * move[1] - row) # (column,row)
                            if self.foundOnBoard(newCoords) and self.boardState[newCoords[1]][newCoords[0]][1].stat == None:
                                allowedMoves.append(newCoords)
                            
                    elif self.boardState[move[1]][move[0]][0] != self.game.playerColour and self.boardState[move[1]][move[0]][1].stat != None:
                        newCoords = (2 * move[0] - column, 2 * move[1] - row) # (column,row)
                        if self.foundOnBoard(newCoords) and self.boardState[newCoords[1]][newCoords[0]][1].stat == None:
                            allowedMoves.append(newCoords)
        
        return allowedMoves

    #   this function checks if a given position is found on the board coords is (column, row)
    def foundOnBoard(self, coords):
        if coords[0] < 0 or coords[0] > 7 or coords[1] < 0 or coords[1] > 7:
            return False
                                                                                 
        return True

    #   Given position of a piece it would update the board stat list and move the piece to the given position 
    def movePiece(self,pieceCoords, toCoords):
        #   pieceCoords and toCoords in the form (x,y) == (column,row):
        fromColor = self.boardState[pieceCoords[1]][pieceCoords[0]][0]
        pieceState = self.boardState[pieceCoords[1]][pieceCoords[0]][1]
        self.boardState[toCoords[1]][toCoords[0]] = (fromColor, pieceState)
        self.removePiece(pieceCoords) #removes piece after movement
        self.makeKing(toCoords)

        
    # if row is 0 or 7 make piece king by updating boardState
    def makeKing(self, coords):
        #   coords in form (x,y) == (column,row)
        if self.boardState[coords[1]][coords[0]][1] != None:
            if (coords[1] == 0 and self.boardState[coords[1]][coords[0]][0] == black) or (coords[1] == 7 and self.boardState[coords[1]][coords[0]][0] == red):
                self.boardState[coords[1]][coords[0]] = (self.boardState[coords[1]][coords[0]][0],pieceState("king"))

                
    # updates board stat list to remove a piece at the given position               
    def removePiece(self, pieceCoords):
        self.boardState[pieceCoords[1]][pieceCoords[0]] = (empty, pieceState(None))


