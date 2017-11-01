#!/usr/bin/env python3

#import random

class GameCell:
    def __init__(self):
        self.symbol = "-"
        self.mutable = True

    def isMutable(self):
        return self.mutable

    def getSymbol(self):
        return self.symbol

    def setSymbol(self,sym):
        self.symbol = sym
        return

    def setMutable(self,val):
        self.mutable = val
        return

    def __str__(self):
        return( self.symbol )


class SmBox:
    def __init__(self):
        self.box = [ [ GameCell() for i in range(3) ] for j in range(3) ]
        return

    def getGameCellValue(self,col,row):
        return( self.box[col][row].getSymbol() )

    def setGameCellValue(self,col,row,val):
        self.box[col][row].setSymbol(val)
        return

    def isGameCellMutable(self,x,y):
        return( self.box[x][y].isMutable() )

    def setGameCellMutability(self,col,row,m):
        self.box[col][row].setMutable(m)
        return

    def getUnusedValues(self,blankCellValue,possibleValueList, debugIt = False):
        resultList = possibleValueList[:]
        for row in range(3):
            for col in range(3):
                if( blankCellValue != self.getGameCellValue(col,row) ):
                    if( True == debugIt ):
                        print( "DEBUG: getUnusedValues:",col,row,resultList, self.getGameCellValue(col,row) )
                    resultList.remove( self.getGameCellValue(col,row) )
        return resultList



class LgBox:
    def __init__(self):
        self.box = [ [ SmBox() for i in range(3) ] for j in range(3) ]
        return

    def getCellValue(self,col,row):
        smBoxCol = col//3 
        smBoxRow = row//3 
        localCol = col%3
        localRow = row%3
        result = self.box[smBoxCol][smBoxRow].getGameCellValue(localCol, localRow )
        return result

    def setMutableCell(self,col,row,val):
        smBoxCol = col//3 
        smBoxRow = row//3 
        localCol = col%3
        localRow = row%3
        if( self.box[smBoxCol][smBoxRow].isGameCellMutable( localCol, localRow ) ):
            self.box[smBoxCol][smBoxRow].setGameCellValue(localCol, localRow, val )
        return

    def setImmutableGameBoard(self,ary):
        boardSize = 9
        for row in range(boardSize):
            for col in range(boardSize):
                smBoxX = col//3 
                smBoxY = row//3 
                bgBoxX = col%3
                bgBoxY = row%3
                print( "board[", smBoxX, "][", smBoxY, "][", bgBoxX, "][", bgBoxY, "] is:", ary[row*9+col] )

                self.box[smBoxX][smBoxY].setGameCellValue(bgBoxX, bgBoxY, ary[row*9+col])
                if( ary[row*9+col] != "-" ):
                    mutability = False
                else:
                    mutability = True
                self.box[smBoxX][smBoxY].setGameCellMutability( bgBoxX, bgBoxY, mutability )
        return

    def getGameBoardAsString(self,includeMutability=False):
        if( includeMutability ):
            boardRowDivider = "+--------------------------+--------------------------+--------------------------+\n"
        else:
            boardRowDivider = "+--------+--------+--------+\n"
        boardSize = 9
        boardString = "\n"
        for row in range(boardSize):
            if( 0 == row%3 ):
                boardString += boardRowDivider
            for col in range(boardSize):
                smBoxX = col%3
                smBoxY = row%3
                bgBoxX = col//3
                bgBoxY = row//3

                if( 0 == smBoxX ):
                    boardString += "!  "
                boardString += self.box[bgBoxX][bgBoxY].getGameCellValue(smBoxX, smBoxY)
                #print( "DEBUG getGameBoardAsString: BOARD[", smBoxX, "][", smBoxY, "][", bgBoxX, "][", bgBoxY, "] is:", self.box[smBoxX][smBoxY].getGameCellValue(bgBoxX, bgBoxY) )
                if( includeMutability ):
                    boardString += " : "
                    boardString += ( "F", "T")[ self.box[smBoxX][smBoxY].isGameCellMutable(bgBoxX, bgBoxY) ]
                boardString += " "
            boardString += "!\n"
        boardString += boardRowDivider
        boardString += "\n"
        return boardString 

    def getUnusedColumnValues(self,colNum,blankCellValue,possibleValueList, debugIt = False):
        resultList = possibleValueList[:]
        bgBoxCol = colNum // 3
        smBoxCol = colNum % 3
        for row in range(9):
            bgBoxRow = row // 3
            smBoxRow = row % 3
            if( True == debugIt ):
                print( "DEBUG getUnusedColumnValues: colNum:", colNum, "bgBoxRow:", bgBoxRow, "smBoxRow:", smBoxRow, "row:", row
                     , "bgBoxCol:", bgBoxCol, "smBoxCol:", smBoxCol
                     , self.box[bgBoxCol][bgBoxRow].getGameCellValue(smBoxCol,smBoxRow) )
            if( "-" != self.box[bgBoxCol][bgBoxRow].getGameCellValue(smBoxCol,smBoxRow) ):
                if( True == debugIt ):
                    print( "DEBUG getUnusedColumnValues: resultList:"
                         , bgBoxCol, bgBoxRow, smBoxCol, smBoxRow, resultList
                         , self.box[bgBoxCol][bgBoxRow].getGameCellValue(smBoxCol,smBoxRow))
                resultList.remove( self.box[bgBoxCol][bgBoxRow].getGameCellValue(smBoxCol,smBoxRow) )

        return resultList

    def getUnusedRowValues(self,rowNum,blankCellValue,possibleValueList, debugIt = False):
        resultList = possibleValueList[:]
        bigBoxRow = rowNum // 3
        smBoxRow = rowNum % 3
        for col in range(9):
            bigBoxCol = col // 3
            smBoxCol = col % 3
            if( True == debugIt ):
                print( "DEBUG getUnusedRowValues: rowNum:", rowNum, "bigBoxRow:", bigBoxRow, "smBoxRow:", smBoxRow, "col:", col
                     , "bigBoxCol:", bigBoxCol, "smBoxCol:", smBoxCol
                     , self.box[bigBoxCol][bigBoxRow].getGameCellValue(smBoxCol,smBoxRow) )
            if( "-" != self.box[bigBoxCol][bigBoxRow].getGameCellValue(smBoxCol,smBoxRow) ):
                if( True == debugIt ):
                    print( "DEBUG getUnusedRowValues: resultList:"
                         , bigBoxCol, bigBoxRow, smBoxCol, smBoxRow, resultList
                         , self.box[bigBoxCol][bigBoxRow].getGameCellValue(smBoxCol,smBoxRow))
                resultList.remove( self.box[bigBoxCol][bigBoxRow].getGameCellValue(smBoxCol,smBoxRow) )

        return resultList



def analyzeBoard(bdOld, bdNew, debugIt):
    for theRow in range(9):
        for theCol in range(9):
            if( True == debugIt ):
                print( "DEBUG analyzeBoard: theCol:", theCol, " theRow:", theRow )
            if( "-" == bdOld.getCellValue(theCol,theRow) ):
                theSmBoxRow = theRow//3
                theSmBoxCol = theCol//3
                sb = set( bdOld.box[theSmBoxCol][theSmBoxRow].getUnusedValues("-",["1","2","3","4","5","6","7","8","9"], debugIt) )
                sr = set( bdOld.getUnusedRowValues(theRow,"-",["1","2","3","4","5","6","7","8","9"], debugIt) )
                sc = set( bdOld.getUnusedColumnValues(theCol,"-",["1","2","3","4","5","6","7","8","9"], debugIt) )
                if( True == debugIt ):
                    print( "box:",theSmBoxCol,theSmBoxRow,sb )
                    print( "col:",theCol,sc )
                    print( "row:",theRow,sr )
    
                sf = ( sb & sr & sc )
                if( True == debugIt ):
                    if( 1 == len(sf) ):
                        postfix = "<=========="
                    else:
                        postfix = ""
                    if( True == debugIt ):
                        print( "matched:",sf, len(sf), theCol, theRow, bdOld.getCellValue(theCol,theRow) , postfix )
                        print( "." )
                if( 1 == len(sf) ):
                    newVal = sf.pop()
                    sf.add( newVal )
                    bdNew.setMutableCell(theCol,theRow,newVal)
            else:
                bdNew.setMutableCell( theCol, theRow, bdOld.getCellValue(theCol,theRow) )

def main():
    lb = LgBox()
    lbNew1 = LgBox()
    lbNew2 = LgBox()
    lbNew3 = LgBox()
    lbNew4 = LgBox()
    lbNew5 = LgBox()
    lbNew6 = LgBox()
    lbNew7 = LgBox()
    lbNew8 = LgBox()
    lbNew9 = LgBox()
    lbNew10 = LgBox()
    
    # Verified this board is solved correctly (compared to the solution at https://www.sudoku-solutions.com/)
    lb.setImmutableGameBoard([
    "5","3","-","-","7","-","-","-","-",
    "6","-","-","1","9","5","-","-","-",
    "-","9","8","-","-","-","-","6","-",
    "8","-","-","-","6","-","-","-","3",
    "4","-","-","8","-","3","-","-","1",
    "7","-","-","-","2","-","-","-","6",
    "-","6","-","-","-","-","2","8","-",
    "-","-","-","4","1","9","-","-","5",
    "-","-","-","-","8","-","-","7","9"
    ])
    gameBoardBefore = lb.getGameBoardAsString()
    
    print( "Game Board 0:", gameBoardBefore )
    analyzeBoard(lb, lbNew1, False)
    print( "Game Board 1:", lbNew1.getGameBoardAsString() )
    analyzeBoard(lbNew1, lbNew2, False)
    print( "Game Board 2:", lbNew2.getGameBoardAsString() )
    analyzeBoard(lbNew2, lbNew3, False)
    print( "Game Board 3:", lbNew3.getGameBoardAsString() )
    analyzeBoard(lbNew3, lbNew4, False)
    print( "Game Board 4:", lbNew4.getGameBoardAsString() )
    analyzeBoard(lbNew4, lbNew5, False)
    print( "Game Board 5:", lbNew5.getGameBoardAsString() )
    analyzeBoard(lbNew5, lbNew6, False)
    print( "Game Board 6:", lbNew6.getGameBoardAsString() )
    analyzeBoard(lbNew6, lbNew7, False)
    print( "Game Board 7:", lbNew7.getGameBoardAsString() )
    analyzeBoard(lbNew7, lbNew8, False)
    print( "Game Board 8:", lbNew8.getGameBoardAsString() )
    analyzeBoard(lbNew8, lbNew9, False)
    print( "Game Board 9:", lbNew9.getGameBoardAsString() )
    analyzeBoard(lbNew9, lbNew10, False)
    print( "Game Board 10:", lbNew10.getGameBoardAsString() )
    
    goldenSolution = [
    "5","3","4","6","7","8","9","1","2",
    "6","7","2","1","9","5","3","4","8",
    "1","9","8","3","4","2","5","6","7",
    "8","5","9","7","6","1","4","2","3",
    "4","2","6","8","5","3","7","9","1",
    "7","1","3","9","2","4","8","5","6",
    "9","6","1","5","3","7","2","8","4",
    "2","8","7","4","1","9","6","3","5",
    "3","4","5","2","8","6","1","7","9"
    ]

    return


main()

