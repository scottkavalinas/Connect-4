# -*- coding: utf-8 -*-
"""connect_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mwqXBobMSi5pNdwduxiYWBCvziLeFmRt
"""

# connect 2, a simple and scaled down version of connect 4 played on a 2x3 board

class board():

  def __init__(self):
    self.colA = [0,0]
    self.colB = [0,0]
    self.colC = [0,0]
    self.errorMSG = 'Illegal move'
    self.gameBoard = []
    self.gameBoard.append(self.colA)
    self.gameBoard.append(self.colB)
    self.gameBoard.append(self.colC)
    self.playable = False

  def isPlayable(self,column):
    move = 0
    if column == 'a':
      move = 0
    if column == 'b':
      move = 1
    if column == 'c':
      move = 2
    
    if 0 in self.gameBoard[move]:
      self.playable = True
      return self.playable
    else:
      self.playable = False
      return self.playable

  def insert(self,column,PTM):
    move = 0
    if not self.playable:
      print(self.errorMSG)
      return
    if column == 'a':
      move = 0
    if column == 'b':
      move = 1
    if column == 'c':
      move = 2

    if self.playable and self.gameBoard[move][0] == 0:
      if PTM == 'r':
        self.gameBoard[move][0]='r'
        return
      else:
        self.gameBoard[move][0] = 'y'
        return
    elif self.playable:
      if PTM == 'r':
        self.gameBoard[move][1]='r'
        return      
      else:
        self.gameBoard[move][1]='y'
        return
  
  def is_won(self):
    if self.colA[0] == self.colA[1] and self.colA[0] != 0:
      if self.colA[0] == 'r':
        print('Player 1 wins!')
      else:
        print('Player 2 wins!')
      return True
    if self.colB[0] == self.colB[1] and self.colB[0] != 0:
      if self.colB[0] == 'r':
        print('Player 1 wins!')
      else:
        print('Player 2 wins!')
      return True
    if self.colC[0] == self.colC[1] and self.colC[0] != 0:
      if self.colC[0] == 'r':
        print('Player 1 wins!')
      else:
        print('Player 2 wins!')
      return True
    else:
      return False

    

  def showBoard(self):
    print('_________')
    print('|'+str(self.gameBoard[0][1])+'|'+'|'+str(self.gameBoard[1][1])+'|'+'|'+str(self.gameBoard[2][1])+'|')
    print('|'+str(self.gameBoard[0][0])+'|'+'|'+str(self.gameBoard[1][0])+'|'+'|'+str(self.gameBoard[2][0])+'|')
    print('_________')

game = board()
  p1 = 'r'
  p2 = 'y'
  game.showBoard()

  while not game.is_won():
    
    p1_Input = input('Player, 1 make a legal move:')
    game.isPlayable(p1_Input)
    game.insert(p1_Input,p1)
    game.showBoard()

    if game.is_won():
      print('Game Over')
      break
    else:
      p2_Input = input('Player, 2 make a legal move:')
      game.isPlayable(p2_Input)
      game.insert(p2_Input,p2)
      game.showBoard()
