# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 16:21:37 2022

@author: marco
"""
import numpy as np
import pygame
import sys

BOARD_WIDTH =5 #size board
BOARD_HEIGHT =5 

DIFFICULTY = 2 # predict how many move ahead

SPACESIZE = 100 #size of token in pixel

FPS = 30

WINDOW_WIDTH = 640 #size screen display
WINDOW_HEIGHT = 480

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)


BRIGHTBLUE = (0, 50, 255)
WHITE = (255, 255, 255)

BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

RED = 'red'
BLACK = 'black'
EMPTY = None
HUMAN = 'human'
COMPUTER = 'computer'

def main():
  global FPSCLOCK, DISPLAYSURF, REDPILERECT, BLACKPILERECT, REDTOKENIMG
  global BLACKTOKENIMG, BOARDIMG, HUMANWINNERIMG
  global COMPUTERWINNERIMG, WINNERRECT

  pygame.init()
  FPSCLOCK = pygame.time.Clock()
  DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
  pygame.display.set_caption('Corner Top')

  REDPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
  BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
  REDTOKENIMG = pygame.image.load('token_red.png')
  REDTOKENIMG = pygame.transform.smoothscale(REDTOKENIMG, (SPACESIZE, SPACESIZE))
  BLACKTOKENIMG = pygame.image.load('token_black.png')
  BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (SPACESIZE, SPACESIZE))
  BOARDIMG = pygame.image.load('board.png')
  BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (SPACESIZE, SPACESIZE))

  HUMANWINNERIMG = pygame.image.load('win.png')
  COMPUTERWINNERIMG = pygame.image.load('lose.png')
  WINNERRECT = HUMANWINNERIMG.get_rect()
  WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

  isFirstGame = True

  while True:
    runGame(isFirstGame)
    isFirstGame = False

def runGame(isFirstGame):
  if isFirstGame:
      # Let the computer go first on the first game, so the player
      # can see how the tokens are dragged from the token piles.
      turn = COMPUTER
  else:
      # Randomly choose who goes first.
      if random.randint(0, 1) == 0:
          turn = COMPUTER
      else:
          turn = HUMAN

  # Set up a blank board data structure.
  mainBoard = getNewBoard()

  while True: # main game loop
    if turn == HUMAN:
      # Human player's turn.
      getHumanMove(mainBoard)
      if isWinner(mainBoard, RED):
        winnerImg = HUMANWINNERIMG
        break
      turn = COMPUTER # switch to other player's turn
    else:
      # Computer player's turn.
      column = getComputerMove(mainBoard)
      animateComputerMoving(mainBoard, column)
      makeMove(mainBoard, BLACK, column)
      if isWinner(mainBoard, BLACK):
          winnerImg = COMPUTERWINNERIMG
          break
      turn = HUMAN # switch to other player's turn


  while True:
    # Keep looping until player clicks the mouse or quits.
    drawBoard(mainBoard)
    DISPLAYSURF.blit(winnerImg, WINNERRECT)
    pygame.display.update()
    FPSCLOCK.tick()
    for event in pygame.event.get(): # event handling loop
      if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONUP:
        return

def makeMove(board, player, column):
  lowest = getLowestEmptySpace(board, column)
  if lowest != -1:
    board[column][lowest] = player

def drawBoard(board, extraToken=None):
  DISPLAYSURF.fill(BGCOLOR)

  # draw tokens
  spaceRect = pygame.Rect(0, 0, SPACESIZE, SPACESIZE)
  for x in range(BOARDWIDTH):
    for y in range(BOARDHEIGHT):
      spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
      if board[x][y] == RED:
        DISPLAYSURF.blit(REDTOKENIMG, spaceRect)
      elif board[x][y] == BLACK:
        DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect)

  # draw the extra token
  if extraToken != None:
    if extraToken['color'] == RED:
      DISPLAYSURF.blit(REDTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))
    elif extraToken['color'] == BLACK:
      DISPLAYSURF.blit(BLACKTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))

  # draw board over the tokens
  for x in range(BOARDWIDTH):
    for y in range(BOARDHEIGHT):
      spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
      DISPLAYSURF.blit(BOARDIMG, spaceRect)

  # draw the red and black tokens off to the side
  DISPLAYSURF.blit(REDTOKENIMG, REDPILERECT) # red on the left
  DISPLAYSURF.blit(BLACKTOKENIMG, BLACKPILERECT) # black on the right


def getNewBoard():
  board = []
  for x in range(BOARDWIDTH):
    board.append([EMPTY] * BOARDHEIGHT)
  return board


def dropPiece(board,row,col,piece):
  board[row][col]=piece

def printBoard():
  print(np.flip(board,0))
  
def getPotentialMoves(board, tile, lookAhead):
  if lookAhead == 0 or isBoardFull(board):
    return [0] * BOARDWIDTH

  if tile == RED:
    enemyTile = BLACK
  else:
    enemyTile = RED
  # Figure out the best move to make.
potentialMoves = [0] * BOARDWIDTH
  for firstMove in range(BOARDWIDTH):
    dupeBoard = copy.deepcopy(board)
    if not isValidMove(dupeBoard, firstMove):
      continue
    makeMove(dupeBoard, tile, firstMove)
    if isWinner(dupeBoard, tile):
      # a winning move automatically gets a perfect fitness
      potentialMoves[firstMove] = 1
      break # don't bother calculating other moves
    else:
      # do other player's counter moves and determine best one
      if isBoardFull(dupeBoard):
        potentialMoves[firstMove] = 0
      else:
        for counterMove in range(BOARDWIDTH):
          dupeBoard2 = copy.deepcopy(dupeBoard)
          if not isValidMove(dupeBoard2, counterMove):
            continue
          makeMove(dupeBoard2, enemyTile, counterMove)
          if isWinner(dupeBoard2, enemyTile):
            # a losing move automatically gets the worst fitness
            potentialMoves[firstMove] = -1
            break
        else:
          # do the recursive call to getPotentialMoves()
          results = getPotentialMoves(dupeBoard2, tile, lookAhead - 1)
          potentialMoves[firstMove] += (sum(results) / BOARDWIDTH) / BOARDWIDTH
  return potentialMoves

def isValidLocation(board,col,row):
  if(col==0 and row ==0):
    return True
  elif(col==0 and row ==5):
    return True
  elif(col==5 and row ==0):
    return True
  elif(col==5 and row ==5):
    return True
  elif(board[col-1][row]!=0):
    return True
  elif(board[col][row-1]!=0):
    return True
  elif(board[col+1][row]!=0):
    return True
  elif(board[col][row+1]!=0):
    return True
  else:
    return False
    
  
def winningMove(board,piece):
  # check middle space
    if board[3][3] == piece:
      return True
    else:
      return False

def drawBoard(board):
  for c in range(col_count):
    for r in range(row_count):
      pygame.draw.rect(screen,BLUE,(c*squaresize,r*squaresize+squaresize,squaresize,squaresize))
      pygame.draw.circle(screen,BLACK,(int(c*squaresize+squaresize/2),int(r*squaresize+squaresize+squaresize/2)),radius)


board=create_board()
game_over=False
turn =0

pygame.init()
pygame.display.set_caption('Corner Top')
squaresize=100

width=col_count*squaresize
height=(row_count+1)*squaresize

size=(width,height)

radius = int(squaresize/2 -5)

screen=pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()
while not game_over:
  
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      sys.exit()

    if event.type==pygame.MOUSEBUTTONDOWN:
      continue
    #ask Player 1 input
    if turn==0:
        col = int(input("Player 1 make your selection(0-6):"))
        if isValidLocation(board,col):
          row = getNextOpenRow(board,col)
          dropPiece(board, row, col, 1)
          if winningMove(board,1):
            print("Player 1 Wins!")
            game_over=True
    #ask Player 2 input
    else:
        col = int(input("Player 2 make your selection(0-6):"))
        if isValidLocation(board,col):
          row = getNextOpenRow(board,col)
          dropPiece(board, row, col, 2)
          if winningMove(board,2):
            print("Player 2 Wins!")
            game_over=True

    
    turn+=1
    turn=turn%2
