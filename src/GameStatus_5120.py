# -*- coding: utf-8 -*-


class GameStatus:


  def __init__(self, board_state, turn_O):

    self.board_state = board_state
    self.turn_O = turn_O
    self.oldScores = 0

    self.winner = ""

  # Determines if the game is in a terminal state
  # For boards larger than 3x3 we count a full board as terminal
  def is_terminal(self):
    # Check winning combinations for 3x3 board
    if len(self.board_state[0]) == 3:
      # Horizontal wins
      for row in self.board_state:
        if row[0] == row[1] == row[2] != 0:
          # Set winner
          self.winner = "O" if row[0] == 1 else "X"
          return True
        
      # Vertical wins
      for col in range(3):
        if self.board_state[0][col] == self.board_state[1][col] == self.board_state[2][col] != 0:
          self.winner = "O" if self.board_state[0][col] == 1 else "X"
          return True
        
      # Diagonal wins
      if self.board_state[0][0] == self.board_state[1][1] == self.board_state[2][2] != 0:
        self.winner = "O" if self.board_state[1][1] == 1 else "X"
        return True
      if self.board_state[0][2] == self.board_state[1][1] == self.board_state[2][0] != 0:
        self.winner = "O" if self.board_state[1][1] == 1 else "X"
        return True

    # Check if a board of ANY size is full
    for row in self.board_state:
      for col in row:
        if col == 0:
          return False
    # If board is full returns true
    return True

  def get_scores(self, terminal):
    """
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)
        
        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        
        """        
    rows = len(self.board_state)
    cols = len(self.board_state[0])
    scores = 0
    check_point = 3 if terminal else 2
    
      

  def get_negamax_scores(self, terminal):
    """
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1)
        """
    rows = len(self.board_state)
    cols = len(self.board_state[0])
    scores = 0
    check_point = 3 if terminal else 2
      
  # Returns all the open moves for a given board
  def get_moves(self):
    moves = []
    for row_index, row in enumerate(self.board_state):
      for col_index, col in enumerate(row):
        if self.board_state[row_index][col_index] == 0:
          moves.append([row_index, col_index])
    return moves

  # Creates a new board for minimax and negamax function nodes
  def get_new_state(self, move):
    new_board_state = self.board_state.copy()
    x, y = move[0], move[1]
    new_board_state[x,y] = 1 if self.turn_O else -1
    return GameStatus(new_board_state, not self.turn_O)