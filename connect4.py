# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 16:21:37 2022

@author: marco
"""
import numpy as np
import pygame
col_count =7
row_count = 6
def create_board():
    board = np.zeros((6,7))
    return board

def dropPiece(board,row,col,piece):
  board[row][col]=piece

def isValidLocation(board,col):
  return board[5][col]==0

def getNextOpenRow(board,col):
  for r in range(row_count):
    if board[r][col]==0:
      return r

def printBoard():
  print(np.flip(board,0))

def winningMove(board,piece):
  for c in range(col_count-3):
    for r in range(row_count):
      if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
        return True
  for c in range(col_count):
    for r in range(row_count-3):
      if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
        return True
  for c in range(col_count):
    for r in range(row_count-3):
      if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
        return True
  for c in range(col_count-3):
    for r in range(3,row_count):
      if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
        return True

def drawBoard(board):
  pass
  
board=create_board()
printBoard()
game_over=False
turn =0

pygame.init()

squaresize=100
width=col_count*squaresize
height=(row_count+1)*squaresize

size=(width,height)

screen=pygame.display.set_mode(size)
while not game_over:
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

    printBoard()
    turn+=1
    turn=turn%2
  