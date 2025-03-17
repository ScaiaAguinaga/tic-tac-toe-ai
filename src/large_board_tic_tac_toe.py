"""
PLEASE READ THE COMMENTS BELOW AND THE HOMEWORK DESCRIPTION VERY CAREFULLY BEFORE YOU START CODING

 The file where you will need to create the GUI which should include (i) drawing the grid, (ii) call your Minimax/Negamax functions
 at each step of the game, (iii) allowing the controls on the GUI to be managed (e.g., setting board size, using 
                                                                                 Minimax or Negamax, and other options)
 In the example below, grid creation is supported using pygame which you can use. You are free to use any other 
 library to create better looking GUI with more control. In the __init__ function, GRID_SIZE (Line number 36) is the variable that
 sets the size of the grid. Once you have the Minimax code written in multiAgents.py file, it is recommended to test
 your algorithm (with alpha-beta pruning) on a 3x3 GRID_SIZE to see if the computer always tries for a draw and does 
 not let you win the game. Here is a video tutorial for using pygame to create grids http://youtu.be/mdTeqiWyFnc
 
 
 PLEASE CAREFULLY SEE THE PORTIONS OF THE CODE/FUNCTIONS WHERE IT INDICATES "YOUR CODE BELOW" TO COMPLETE THE SECTIONS
 
"""
import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random

mode = "player_vs_ai" 

class RandomBoardTicTacToe:
    def __init__(self, size = (600, 600)):
        self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Grid Size
        self.GRID_SIZE = 4
        self. OFFSET = 5

        self.CIRCLE_COLOR = (140, 146, 172)
        self.CROSS_COLOR = (140, 146, 172)

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = self.size[0]/self.GRID_SIZE - self.OFFSET
        self.HEIGHT = self.size[1]/self.GRID_SIZE - self.OFFSET

        # This sets the margin between each cell
        self.MARGIN = 5
        
        # Initialize game variables
        self.human_symbol = "X"  # Default human symbol
        self.game_mode = "player_vs_ai"  # Default game mode
        self.algorithm = "minimax"  # Default algorithm
        
        # Grid position variables
        self.grid_top = 0
        self.grid_size = 0
        self.cell_size = 0

        # Initialize tracking variables
        self.last_winner = "########"
        self.human_score = 0
        self.computer_score = 0

        # Initialize pygame
        pygame.init()
        self.game_reset()

    def draw_game(self):
        # Create a 2 dimensional array using the column and row variables
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe Large Board")
        self.screen.fill(self.WHITE)
        
        # Draw border around the entire game area
        pygame.draw.rect(self.screen, self.BLACK, [0, 0, self.width, self.height], 2)
        
        # Draw title area
        title_font = pygame.font.SysFont('Arial', 24, bold=True)
        title = title_font.render("Tic-Tac-Toe large board", True, self.BLACK)
        self.screen.blit(title, (20, 20))
        
        # Draw options area
        font = pygame.font.SysFont('Arial', 18)
        
        # Player symbol selection
        symbol_text = font.render("Select human player symbol", True, self.BLACK)
        self.screen.blit(symbol_text, (20, 60))
        
        # Draw radio buttons for symbol selection
        pygame.draw.circle(self.screen, self.BLACK, (30, 90), 8, 1)
        o_text = font.render("Nought (O)", True, self.BLACK)
        self.screen.blit(o_text, (45, 85))
        
        pygame.draw.circle(self.screen, self.BLACK, (30, 120), 8, 1)
        x_text = font.render("Cross (X)", True, self.BLACK)
        self.screen.blit(x_text, (45, 115))
        
        # Fill the selected option
        if self.human_symbol == "O":
            pygame.draw.circle(self.screen, self.BLACK, (30, 90), 4)
        else:
            pygame.draw.circle(self.screen, self.BLACK, (30, 120), 4)
        
        # Board size selection
        size_text = font.render("Board size:", True, self.BLACK)
        self.screen.blit(size_text, (320, 60))
        
        # Draw dropdown-like box for board size
        pygame.draw.rect(self.screen, self.BLACK, [430, 60, 60, 25], 1)
        size_value = font.render(f"{self.GRID_SIZE}x{self.GRID_SIZE}", True, self.BLACK)
        self.screen.blit(size_value, (440, 60))
        pygame.draw.polygon(self.screen, self.BLACK, [(480, 65), (490, 65), (485, 75)])
        
        # Game mode options
        pygame.draw.circle(self.screen, self.BLACK, (30, 150), 8, 1)
        human_vs_human = font.render("Human vs human", True, self.BLACK)
        self.screen.blit(human_vs_human, (45, 145))
        
        pygame.draw.circle(self.screen, self.BLACK, (30, 180), 8, 1)
        human_vs_computer = font.render("Human vs computer", True, self.BLACK)
        self.screen.blit(human_vs_computer, (45, 175))
        
        # Fill the selected option
        if self.game_mode == "human_vs_human":
            pygame.draw.circle(self.screen, self.BLACK, (30, 150), 4)
        else:
            pygame.draw.circle(self.screen, self.BLACK, (30, 180), 4)
        
        # Winner and scores display
        winner_text = font.render(f"Winner: {self.last_winner}", True, self.BLACK)
        self.screen.blit(winner_text, (300, 100))
        
        scores_text = font.render(f"Scores (Human: {self.human_score}, Computer: {self.computer_score})", True, self.BLACK)
        self.screen.blit(scores_text, (300, 130))
        
        # Start game button
        pygame.draw.rect(self.screen, (65, 105, 225), [370, 180, 100, 30])
        start_text = font.render("Start game", True, self.WHITE)
        self.screen.blit(start_text, (380, 185))
        
        # Draw the grid
        grid_top = 220  # Starting y position for the grid
        grid_size = min(self.width - 40, self.height - grid_top - 20)
        cell_size = grid_size / self.GRID_SIZE
        
        # Update WIDTH and HEIGHT for drawing symbols
        self.WIDTH = cell_size
        self.HEIGHT = cell_size
        
        # Draw grid border
        pygame.draw.rect(self.screen, self.BLACK, [20, grid_top, grid_size, grid_size], 2)
        
        # Draw grid lines
        for i in range(1, self.GRID_SIZE):
            # Horizontal lines
            pygame.draw.line(self.screen, self.BLACK, 
                            (20, grid_top + i * cell_size), 
                            (20 + grid_size, grid_top + i * cell_size), 1)
            # Vertical lines
            pygame.draw.line(self.screen, self.BLACK, 
                            (20 + i * cell_size, grid_top), 
                            (20 + i * cell_size, grid_top + grid_size), 1)
        
        pygame.display.update()
        
        # Store grid position for mouse click detection
        self.grid_top = grid_top
        self.grid_size = grid_size
        self.cell_size = cell_size

    def change_turn(self):

        if(self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")


    def draw_circle(self, row, col):
        # Calculate the position for the circle
        pos_x = 20 + (col + 0.5) * self.cell_size
        pos_y = self.grid_top + (row + 0.5) * self.cell_size
        radius = self.cell_size * 0.4
        
        # Draw the circle
        pygame.draw.circle(self.screen, self.CIRCLE_COLOR, (pos_x, pos_y), radius, 3)
        pygame.display.update()

    def draw_cross(self, row, col):
        # Calculate the position for the cross
        pos_x = 20 + col * self.cell_size
        pos_y = self.grid_top + row * self.cell_size
        margin = self.cell_size * 0.2
        
        # Draw the cross (X)
        pygame.draw.line(self.screen, self.CROSS_COLOR, 
                        (pos_x + margin, pos_y + margin), 
                        (pos_x + self.cell_size - margin, pos_y + self.cell_size - margin), 3)
        pygame.draw.line(self.screen, self.CROSS_COLOR, 
                        (pos_x + self.cell_size - margin, pos_y + margin), 
                        (pos_x + margin, pos_y + self.cell_size - margin), 3)
        pygame.display.update()

    def is_game_over(self):
        # Check if the game has terminated using is_terminal() from GameStatus
        terminal = self.game_state.is_terminal()
        
        if terminal:
            # Display the winner if there is one
            if self.game_state.winner:
                pygame.display.set_caption(f"Game Over! Winner: {self.game_state.winner}")
            else:
                pygame.display.set_caption("Game Over! It's a draw!")
        
        return terminal

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)


    def play_ai(self):
        if hasattr(self, 'algorithm') and self.algorithm == "negamax":
            turn_multiplier = 1 if not self.game_state.turn_O else -1
            score, move = negamax(self.game_state, 4, turn_multiplier)
        else:
            ai_is_o = self.human_symbol == "X"
            maximizing = (self.game_state.turn_O and not ai_is_o) or (not self.game_state.turn_O and ai_is_o)
            score, move = minimax(self.game_state, 4, maximizing)
        
        if move:
            self.move(move)
            
            if self.human_symbol == "O":
                self.draw_cross(move[0], move[1])
            else:
                self.draw_circle(move[0], move[1])
        
        self.change_turn()
        pygame.display.update()
        
        terminal = self.game_state.is_terminal()
        if terminal:
            scores = self.game_state.get_scores(terminal)
            
            # Determine winner based on final board state
            if scores > 0:
                winner = "O"
            elif scores < 0:
                winner = "X"
            else:
                winner = "Draw"
            
            # Update last_winner
            self.last_winner = winner
            
            # Update scores based on who won
            if winner != "Draw":
                if (winner == "O" and self.human_symbol == "O") or (winner == "X" and self.human_symbol == "X"):
                    self.human_score += 1
                    print(f"Human won! Score increased to {self.human_score}")
                else:
                    self.computer_score += 1
                    print(f"Computer won! Score increased to {self.computer_score}")
            
            # Update the display
            font = pygame.font.SysFont('Arial', 18)
            winner_text = font.render(f"Winner: {self.last_winner}", True, self.BLACK)
            self.screen.fill(self.WHITE, (300, 100, 200, 25))
            self.screen.blit(winner_text, (300, 100))
            
            scores_text = font.render(f"Scores (Human: {self.human_score}, Computer: {self.computer_score})", True, self.BLACK)
            self.screen.fill(self.WHITE, (300, 130, 250, 25))
            self.screen.blit(scores_text, (300, 130))
            
            pygame.display.update()



    def game_reset(self):
        self.draw_game()
        
        # Initialize the board with zeros (empty cells)
        board = np.zeros((self.GRID_SIZE, self.GRID_SIZE))
        
        # Create a new game state with the initialized board
        self.game_state = GameStatus(board, True)  # True means O's turn
        
        pygame.display.set_caption("Tic Tac Toe - O's turn")
        pygame.display.update()

    def play_game(self, mode="player_vs_ai"):
        self.game_mode = "human_vs_human" if mode == "human_vs_human" else "player_vs_ai"
        self.draw_game()  # Draw the initial game state with options
        
        done = False
        clock = pygame.time.Clock()
        game_started = False

        while not done:
            for event in pygame.event.get():
                # Check if user wants to exit
                if event.type == pygame.QUIT:
                    done = True
                
                # Handle mouse clicks
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    
                    if not game_started:
                        # Check if start game button clicked
                        if 370 <= pos[0] <= 470 and 180 <= pos[1] <= 210:
                            game_started = True
                            self.game_reset()
                            continue
                        
                        # Check if O symbol selected
                        if 22 <= pos[0] <= 38 and 82 <= pos[1] <= 98:
                            self.human_symbol = "O"
                            self.draw_game()
                        
                        # Check if X symbol selected
                        if 22 <= pos[0] <= 38 and 112 <= pos[1] <= 128:
                            self.human_symbol = "X"
                            self.draw_game()
                        
                        # Check if human vs human selected
                        if 22 <= pos[0] <= 38 and 142 <= pos[1] <= 158:
                            self.game_mode = "human_vs_human"
                            mode = "human_vs_human"
                            self.draw_game()
                        
                        # Check if human vs computer selected
                        if 22 <= pos[0] <= 38 and 172 <= pos[1] <= 188:
                            self.game_mode = "player_vs_ai"
                            mode = "player_vs_ai"
                            self.draw_game()
                        
                        # Check if board size dropdown clicked
                        if 430 <= pos[0] <= 490 and 60 <= pos[1] <= 85:
                            # Cycle through board sizes: 3x3 -> 4x4 -> 5x5 -> 3x3
                            if self.GRID_SIZE == 3:
                                self.GRID_SIZE = 4
                            elif self.GRID_SIZE == 4:
                                self.GRID_SIZE = 5
                            else:
                                self.GRID_SIZE = 3
                            self.draw_game()
                    
                    else:
                        # Game has started, handle grid clicks
                        if 20 <= pos[0] <= 20 + self.grid_size and self.grid_top <= pos[1] <= self.grid_top + self.grid_size:
                            # Convert click to grid coordinates
                            col = int((pos[0] - 20) // self.cell_size)
                            row = int((pos[1] - self.grid_top) // self.cell_size)
                            
                            # Check if the cell is empty
                            if 0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE:
                                if self.game_state.board_state[row, col] == 0:
                                    # Make the move
                                    move = [row, col]
                                    self.move(move)
                                    
                                    # Draw the human player's symbol
                                    if self.human_symbol == "O":
                                        self.draw_circle(row, col)
                                    else:
                                        self.draw_cross(row, col)
                                    
                                    # Check if game is over after human move
                                    if self.is_game_over():
                                        pygame.time.wait(2000)  # Wait for 2 seconds
                                        self.game_reset()
                                        game_started = False
                                    elif mode == "player_vs_ai":
                                        self.play_ai()
                                        if self.is_game_over():
                                            pygame.time.wait(2000)  # Wait for 2 seconds
                                            self.game_reset()
                                            game_started = False
                                    elif mode == "human_vs_human":
                                        # Toggle turn
                                        self.game_state.turn_O = not self.game_state.turn_O
                                        self.change_turn()
            
            # Update the screen
            pygame.display.update()
        
        # Limit to 60 frames per second
        clock.tick(60)
    
    pygame.quit()

# Initialize and start the game
tictactoegame = RandomBoardTicTacToe()
tictactoegame.play_game()
