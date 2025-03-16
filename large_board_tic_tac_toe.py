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

mode = "player_vs_ai" # default mode for playing the game (player vs AI)

class RandomBoardTicTacToe:
    def __init__(self, size=(800, 800)):
        self.size = self.width, self.height = size
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (65, 105, 225)
        self.CIRCLE_COLOR = (140, 146, 172)
        self.CROSS_COLOR = (140, 146, 172)

        self.GRID_SIZE = 4
        self.OFFSET = 5
        self.WIDTH = (self.size[0] - 100)/self.GRID_SIZE - self.OFFSET
        self.HEIGHT = (self.size[1] - 300)/self.GRID_SIZE - self.OFFSET
        self.MARGIN = 5

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic-Tac-Toe Large Board")
        
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        
        self.radio_buttons = {
            'nought': pygame.Rect(40, 80, 20, 20),
            'cross': pygame.Rect(40, 120, 20, 20),
            'hvh': pygame.Rect(40, 180, 20, 20),
            'hvc': pygame.Rect(40, 220, 20, 20)
        }
        
        self.start_button = pygame.Rect(self.width - 200, 150, 150, 50)
        self.size_dropdown = pygame.Rect(self.width - 200, 80, 100, 40)
        
        self.human_symbol = 'X'
        self.computer_symbol = 'O'
        self.game_mode = "player_vs_ai"
        self.human_score = 0
        self.computer_score = 0
        self.winner = None
        
        self.game_reset()

    def draw_game(self):
        self.screen.fill(self.BLACK)
        
        title = self.title_font.render("Tic-Tac-Toe large board", True, self.WHITE)
        self.screen.blit(title, (40, 20))
        
        symbol_text = self.font.render("Select human player symbol", True, self.WHITE)
        self.screen.blit(symbol_text, (40, 60))
        
        for button, rect in self.radio_buttons.items():
            pygame.draw.circle(self.screen, self.WHITE, rect.center, 10, 1)
            if (button == 'nought' and self.human_symbol == 'O') or \
               (button == 'cross' and self.human_symbol == 'X') or \
               (button == 'hvh' and self.game_mode == "player_vs_player") or \
               (button == 'hvc' and self.game_mode == "player_vs_ai"):
                pygame.draw.circle(self.screen, self.WHITE, rect.center, 6)
            
            label_text = ""
            if button == 'nought': 
                label_text = "Nought (O)"
                y_pos = 80
            elif button == 'cross': 
                label_text = "Cross (X)"
                y_pos = 120
            elif button == 'hvh': 
                label_text = "Human vs human"
                y_pos = 180
            elif button == 'hvc': 
                label_text = "Human vs computer"
                y_pos = 220
            
            label = self.font.render(label_text, True, self.WHITE)
            self.screen.blit(label, (70, y_pos - 5))
        
        size_text = self.font.render(f"Board size: {self.GRID_SIZE}x{self.GRID_SIZE}", True, self.WHITE)
        self.screen.blit(size_text, (self.width - 250, 80))
        
        pygame.draw.rect(self.screen, self.BLUE, self.start_button)
        start_text = self.font.render("Start game", True, self.WHITE)
        self.screen.blit(start_text, (self.start_button.centerx - start_text.get_width()//2,
                                    self.start_button.centery - start_text.get_height()//2))
        
        score_text = self.font.render(f"Scores (Human: {self.human_score}, Computer: {self.computer_score})",
                                    True, self.WHITE)
        self.screen.blit(score_text, (40, 260))

        board_size_pixels = self.GRID_SIZE * self.WIDTH
        board_start_x = (self.width - board_size_pixels) // 2
        board_start_y = 300

        for i in range(self.GRID_SIZE + 1):
            pygame.draw.line(self.screen, self.WHITE,
                           (board_start_x + i * self.WIDTH, board_start_y),
                           (board_start_x + i * self.WIDTH, board_start_y + board_size_pixels), 2)
            pygame.draw.line(self.screen, self.WHITE,
                           (board_start_x, board_start_y + i * self.HEIGHT),
                           (board_start_x + board_size_pixels, board_start_y + i * self.HEIGHT), 2)

        pygame.display.update()

    def change_turn(self):

        if(self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")


    def draw_circle(self, x, y):
        # Draw circle for noughts player
        center_x = (self.MARGIN + self.WIDTH) * x + self.MARGIN + self.WIDTH//2
        center_y = (self.MARGIN + self.HEIGHT) * y + self.MARGIN + self.HEIGHT//2 + 250
        radius = min(self.WIDTH, self.HEIGHT)//3
        pygame.draw.circle(self.screen, self.CIRCLE_COLOR, (center_x, center_y), radius, 3)

    def draw_cross(self, x, y):
        # Draw cross for crosses player
        start_x = (self.MARGIN + self.WIDTH) * x + self.MARGIN
        start_y = (self.MARGIN + self.HEIGHT) * y + self.MARGIN + 250
        end_x = start_x + self.WIDTH
        end_y = start_y + self.HEIGHT
        
        pygame.draw.line(self.screen, self.CROSS_COLOR,
                        (start_x + 20, start_y + 20),
                        (end_x - 20, end_y - 20), 3)
        pygame.draw.line(self.screen, self.CROSS_COLOR,
                        (end_x - 20, start_y + 20),
                        (start_x + 20, end_y - 20), 3)

    def is_game_over(self):
        # Check if game is terminal using GameStatus
        return self.game_state.is_terminal()

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)


    def play_ai(self):
        # Call minimax/negamax and make AI move
        if self.game_mode == "player_vs_ai":
            score, move = minimax(self.game_state, 4)  # Using minimax by default
            if move:
                self.move(move)
                x, y = move
                self.draw_circle(x, y) if self.computer_symbol == 'O' else self.draw_cross(x, y)
        
        self.change_turn()
        pygame.display.update()
        
        terminal = self.game_state.is_terminal()
        if terminal:
            scores = self.game_state.get_scores(terminal)



    def game_reset(self):
        self.draw_game()
        """
        YOUR CODE HERE TO RESET THE BOARD TO VALUE 0 FOR ALL CELLS AND CREATE A NEW GAME STATE WITH NEWLY INITIALIZED
        BOARD STATE
        """
        
        pygame.display.update()

    def play_game(self, mode="player_vs_ai"):
        self.game_mode = mode
        self.game_reset()
        pygame.display.update()

if __name__ == "__main__":
    tictactoegame = RandomBoardTicTacToe()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        tictactoegame.draw_game()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button, rect in tictactoegame.radio_buttons.items():
                    if rect.collidepoint(pos):
                        if button == 'nought':
                            tictactoegame.human_symbol = 'O'
                            tictactoegame.computer_symbol = 'X'
                        elif button == 'cross':
                            tictactoegame.human_symbol = 'X'
                            tictactoegame.computer_symbol = 'O'
                        elif button == 'hvh':
                            tictactoegame.game_mode = "player_vs_player"
                        elif button == 'hvc':
                            tictactoegame.game_mode = "player_vs_ai"
                
                if tictactoegame.start_button.collidepoint(pos):
                    tictactoegame.play_game(tictactoegame.game_mode)
                
                column = pos[0] // (tictactoegame.WIDTH + tictactoegame.MARGIN)
                row = (pos[1] - 300) // (tictactoegame.HEIGHT + tictactoegame.MARGIN)
                
                if (0 <= row < tictactoegame.GRID_SIZE and 
                    0 <= column < tictactoegame.GRID_SIZE):
                    if not tictactoegame.is_game_over():
                        tictactoegame.move((row, column))
                        if tictactoegame.human_symbol == 'X':
                            tictactoegame.draw_cross(column, row)
                        else:
                            tictactoegame.draw_circle(column, row)
                        
                        if not tictactoegame.is_game_over():
                            tictactoegame.play_ai()
        
        pygame.display.update()
        clock.tick(60)
