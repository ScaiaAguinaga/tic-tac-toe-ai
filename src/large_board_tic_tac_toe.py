import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random

mode = "player_vs_ai"

class RandomBoardTicTacToe:
    def __init__(self):
        
        #this determines window size
        self.width = 600
        self.height = 700
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic-Tac-Toe Large Board")
        
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        #grid size
        self.GRID_SIZE = 4
        self.OFFSET = 5

        #this determines color of the circle and cross
        self.CIRCLE_COLOR = (0, 0, 255)
        self.CROSS_COLOR = (255, 0, 0)

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = (self.size[0] * 0.9) / self.GRID_SIZE - self.OFFSET
        self.HEIGHT = (self.size[1] - 200) / self.GRID_SIZE - self.OFFSET

        #This sets the margin between each cell
        self.MARGIN = 5
        
        self.dropdown_open = False
        self.dropdown_options = [3, 4, 5]
        
        self.player_symbol = "O"
        self.game_mode = "player_vs_ai"
        self.use_minimax = True
        
        self.human_score = 0
        self.computer_score = 0
        self.winner = None

        self.controls_height = 200
        
        #this resets/initializes the board
        pygame.init()
        self.game_reset()

    #this draws the game
    def draw_game(self):
        # Create a 2 dimensional array using the column and row variables
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic-Tac-Toe Large Board")
        self.screen.fill(self.BLACK)
        # Draw the Grid

        pygame.draw.rect(self.screen, self.WHITE, (0, 0, self.width, self.controls_height))
        pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.controls_height), 2)
        
        font_title = pygame.font.SysFont("Times New Roman", 32)
        font = pygame.font.SysFont("Times New Roman", 22)
        
        #title
        title_text = font_title.render("Tic-Tac-Toe Large Board", True, self.BLACK)
        self.screen.blit(title_text, (20, 10))
        

        options = [
            ["Select human player", 20, 50, None],
            ["Nought (O)", 45, 75, self.player_symbol == "O"],
            ["Cross (X)", 45, 100, self.player_symbol == "X"],
            ["Algorithm:", 220, 50, None],
            ["Minimax", 235, 75, self.use_minimax],
            ["Negamax", 235, 100, not self.use_minimax],
            ["Human vs human", 45, 125, self.game_mode == "human_vs_human"],
            ["Human vs computer", 45, 150, self.game_mode == "player_vs_ai"]
        ]
        
        for i, (text, x, y, condition) in enumerate(options):
            
            if condition is not None:
                radio_x = x - 15 if x > 50 else 30
                if condition:
                    pygame.draw.circle(self.screen, self.BLUE, (radio_x, y + 13), 6)
                else:
                    pygame.draw.circle(self.screen, self.BLUE, (radio_x, y + 13), 6, 1)
            
            label = font.render(text, True, self.BLACK)
            self.screen.blit(label, (x, y))
        
        #board size pick
        size_text = font.render("Board size:", True, self.BLACK)
        self.screen.blit(size_text, (380, 50))
        
        #dropdown box
        pygame.draw.rect(self.screen, (220, 220, 220), (380, 75, 80, 30))
        pygame.draw.rect(self.screen, self.BLACK, (380, 75, 80, 30), 1)
        size_value = font.render(f"{self.GRID_SIZE}x{self.GRID_SIZE}", True, (255, 0, 0))
        self.screen.blit(size_value, (386, 80))
        
        # arrow
        pygame.draw.polygon(self.screen, self.BLUE, [(430, 85), (440, 85), (435, 95)])
        
        # draws dropdown options
        if self.dropdown_open:
            for i, size in enumerate(self.dropdown_options):
                option_y = 105 + i * 30
                pygame.draw.rect(self.screen, (220, 220, 220), (380, option_y, 80, 30))
                pygame.draw.rect(self.screen, self.BLACK, (380, option_y, 80, 30), 1)
                option_text = font.render(f"{size}x{size}", True, self.BLACK)
                self.screen.blit(option_text, (386, option_y + 5))
        
        #inits game status
        status_items = [
            [f"Winner: {self.winner if self.winner else 'None'}", 230, 135],
            [f"Scores (H: {self.human_score}, C: {self.computer_score})", 230, 160]
        ]
        
        for text, x, y in status_items:
            status = font.render(text, True, self.BLACK)
            self.screen.blit(status, (x, y))
        
        # start button
        pygame.draw.rect(self.screen, self.BLUE, (430, 160, 120, 30))
        start_text = font.render("Start game", True, self.WHITE)
        self.screen.blit(start_text, (440, 165))
        
        #creates the game grid
        grid_width = self.GRID_SIZE * (self.WIDTH + self.MARGIN) - self.MARGIN
        left_margin = (self.width - grid_width) / 2
        
        #creates cells
        for row in range(self.GRID_SIZE):
            for column in range(self.GRID_SIZE):
                pygame.draw.rect(self.screen, self.WHITE,
                               [(self.MARGIN + self.WIDTH) * column + self.MARGIN + left_margin,
                                (self.MARGIN + self.HEIGHT) * row + self.MARGIN + self.controls_height,
                                self.WIDTH,
                                self.HEIGHT])
                pygame.draw.rect(self.screen, self.BLACK,
                               [(self.MARGIN + self.WIDTH) * column + self.MARGIN + left_margin,
                                (self.MARGIN + self.HEIGHT) * row + self.MARGIN + self.controls_height,
                                self.WIDTH,
                                self.HEIGHT], 1)
        
        # Draw grid border
        pygame.draw.rect(self.screen, self.BLACK, 
                        (left_margin, 
                         self.controls_height + self.MARGIN, 
                         grid_width,
                         self.GRID_SIZE * (self.HEIGHT + self.MARGIN) - self.MARGIN), 2)

    #this changes the turn back and forth between O and X
    def change_turn(self):

        if(self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")


    def draw_circle(self, x, y):
        grid_width = self.GRID_SIZE * (self.WIDTH + self.MARGIN) - self.MARGIN
        left_margin = (self.width - grid_width) / 2
        
        center = ((self.MARGIN + self.WIDTH) * x + self.WIDTH/2 + self.MARGIN + left_margin,
                  (self.MARGIN + self.HEIGHT) * y + self.HEIGHT/2 + self.MARGIN + self.controls_height)
        radius = min(self.WIDTH, self.HEIGHT)/2 - self.MARGIN
        pygame.draw.circle(self.screen, self.CIRCLE_COLOR, center, radius, 3)

    def draw_cross(self, x, y):
        grid_width = self.GRID_SIZE * (self.WIDTH + self.MARGIN) - self.MARGIN
        left_margin = (self.width - grid_width) / 2
        
        start_x = (self.MARGIN + self.WIDTH) * x + self.MARGIN * 2 + left_margin
        start_y = (self.MARGIN + self.HEIGHT) * y + self.MARGIN * 2 + self.controls_height
        end_x = start_x + self.WIDTH - self.MARGIN * 2
        end_y = start_y + self.HEIGHT - self.MARGIN * 2
        
        pygame.draw.line(self.screen, self.CROSS_COLOR, 
                        (start_x, start_y), (end_x, end_y), 3)
        pygame.draw.line(self.screen, self.CROSS_COLOR,
                        (start_x, end_y), (end_x, start_y), 3)

    #this checks if there is a winner or a draw. key for later when giving message
    def is_game_over(self):
        terminal = self.game_state.is_terminal()
        
        if not terminal:
            for row in range(self.GRID_SIZE):
                if all(self.game_state.board_state[row][col] == 1 for col in range(self.GRID_SIZE)):
                    self.winner = "O"
                    if self.player_symbol == "O":
                        self.human_score += 1
                    else:
                        self.computer_score += 1
                    self.draw_game()
                    return True
                elif all(self.game_state.board_state[row][col] == -1 for col in range(self.GRID_SIZE)):
                    self.winner = "X"
                    if self.player_symbol == "X":
                        self.human_score += 1
                    else:
                        self.computer_score += 1
                    self.draw_game()
                    return True
            
            for col in range(self.GRID_SIZE):
                if all(self.game_state.board_state[row][col] == 1 for row in range(self.GRID_SIZE)):
                    self.winner = "O"
                    if self.player_symbol == "O":
                        self.human_score += 1
                    else:
                        self.computer_score += 1
                    self.draw_game()
                    return True
                elif all(self.game_state.board_state[row][col] == -1 for row in range(self.GRID_SIZE)):
                    self.winner = "X"
                    if self.player_symbol == "X":
                        self.human_score += 1
                    else:
                        self.computer_score += 1
                    self.draw_game()
                    return True
            
            if all(self.game_state.board_state[i][i] == 1 for i in range(self.GRID_SIZE)):
                self.winner = "O"
                if self.player_symbol == "O":
                    self.human_score += 1
                else:
                    self.computer_score += 1
                self.draw_game()
                return True
            elif all(self.game_state.board_state[i][i] == -1 for i in range(self.GRID_SIZE)):
                self.winner = "X"
                if self.player_symbol == "X":
                    self.human_score += 1
                else:
                    self.computer_score += 1
                self.draw_game()
                return True
            
            if all(self.game_state.board_state[i][self.GRID_SIZE - 1 - i] == 1 for i in range(self.GRID_SIZE)):
                self.winner = "O"
                if self.player_symbol == "O":
                    self.human_score += 1
                else:
                    self.computer_score += 1
                self.draw_game()
                return True
            elif all(self.game_state.board_state[i][self.GRID_SIZE - 1 - i] == -1 for i in range(self.GRID_SIZE)):
                self.winner = "X"
                if self.player_symbol == "X":
                    self.human_score += 1
                else:
                    self.computer_score += 1
                self.draw_game()
                return True
        
        if terminal:
            scores = self.game_state.get_scores(terminal)
            

            if isinstance(scores, (list, tuple)):
                if scores[0] > scores[1]:
                    self.winner = "O"
                    if self.player_symbol == "O":
                        self.human_score += 1
                    else:
                        self.computer_score += 1
                elif scores[1] > scores[0]:
                    self.winner = "X"
                    if self.player_symbol == "X":
                        self.human_score += 1
                    else:
                        self.computer_score += 1
                else:
                    self.winner = "Draw"
            else:
                if scores > 0:
                    self.winner = "O"
                    if self.player_symbol == "O":
                        self.human_score += 1
                    else:
                        self.computer_score += 1
                elif scores < 0:
                    self.winner = "X"
                    if self.player_symbol == "X":
                        self.human_score += 1
                    else:
                        self.computer_score += 1
                else:
                    self.winner = "Draw"
            
            self.draw_game()
            return True
            
        if all(self.game_state.board_state[row][col] != 0 for row in range(self.GRID_SIZE) for col in range(self.GRID_SIZE)):
            self.winner = "Draw"
            self.draw_game()
            return True
            
        return False

    def move(self, move):
        x, y = move
        new_board_state = self.game_state.board_state.copy()
        
        if self.game_state.turn_O:
            new_board_state[y][x] = 1
        else:
            new_board_state[y][x] = -1
        
        self.game_state = GameStatus(new_board_state, not self.game_state.turn_O)

    def play_ai(self):
        current_game_state = GameStatus(self.board_state.copy(), not (self.player_symbol == "O"))

        for move in current_game_state.get_moves():
            test_state = current_game_state.get_new_state(move)
            if test_state.is_terminal() and test_state.winner == self.player_symbol:
                row, col = move
                self.board_state[row][col] = -1 if self.player_symbol == "O" else 1
                self.game_state = GameStatus(self.board_state.copy(), not self.game_state.turn_O)
                self.draw_game()

                return (col, row)
        depth = 6 if self.GRID_SIZE == 3 else 8 if self.GRID_SIZE == 4 else 6
    
        if self.use_minimax:
            print(f"Using Minimax algorithm with depth {depth}")
            _, best_move = minimax(current_game_state, depth, current_game_state.turn_O)
        else:
            print(f"Using Negamax algorithm with depth {depth}")
            turn_multiplier = 1 if current_game_state.turn_O else -1
            _, best_move = negamax(current_game_state, depth, turn_multiplier)
    
        if best_move is not None:
            row, col = best_move 

            if self.player_symbol == "O":  
                self.board_state[row][col] = -1
                self.draw_cross(col, row)  
            else:  
                self.board_state[row][col] = 1
                self.draw_circle(col, row)  
            
            # Update the game state with the new board
            self.game_state = GameStatus(self.board_state.copy(), not self.game_state.turn_O)
            
            pygame.display.update()

            if self.is_game_over():
                self.draw_game()
                pygame.time.delay(2000)
                return None

   

    def game_reset(self):
        self.winner = None
        
        board_zeros = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        
        self.game_state = GameStatus(board_zeros, True)
        
        grid_area_width = self.width * 0.9
        grid_area_height = self.height - self.controls_height - 20
        
        cell_size_from_width = grid_area_width / self.GRID_SIZE - self.MARGIN
        cell_size_from_height = grid_area_height / self.GRID_SIZE - self.MARGIN
        cell_size = min(cell_size_from_width, cell_size_from_height)
        
        self.WIDTH = cell_size
        self.HEIGHT = cell_size
        
        self.draw_game()
        
        pygame.display.update()

    def play_game(self, mode="player_vs_ai"):
        done = False
        clock = pygame.time.Clock()
        
        self.board_state = np.zeros((self.GRID_SIZE, self.GRID_SIZE))
        self.game_state = GameStatus(self.board_state.copy(), True)
        
        player_symbol = self.player_symbol
        ai_symbol = "X" if player_symbol == "O" else "O"
        
        current_turn = "O"
        
        self.draw_game()
        pygame.display.set_caption(f"Tic Tac Toe - {current_turn}'s turn")
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    
                    if pos[1] > self.controls_height:
                        grid_width = self.GRID_SIZE * (self.WIDTH + self.MARGIN) - self.MARGIN
                        left_margin = (self.width - grid_width) / 2
                        
                        grid_x = pos[0] - left_margin
                        grid_y = pos[1] - self.controls_height
                        
                        column = int(grid_x // (self.WIDTH + self.MARGIN))
                        row = int(grid_y // (self.HEIGHT + self.MARGIN))
                        
                        if (0 <= row < self.GRID_SIZE and 0 <= column < self.GRID_SIZE and 
                            self.board_state[row][column] == 0):
                            
                            self.board_state[row][column] = 1 if current_turn == "O" else -1
                            if current_turn == "O":
                                self.draw_circle(column, row)
                            else:
                                self.draw_cross(column, row)
                            
                            self.game_state = GameStatus(self.board_state.copy(), not self.game_state.turn_O)
                            
                            pygame.display.update()
                            
                            if self.is_game_over():
                                self.draw_game()
                                if self.winner == "Draw":
                                    pygame.display.set_caption("Game Over! It's a Draw!")
                                else:
                                    pygame.display.set_caption(f"Game Over! {self.winner} wins!")
                                pygame.time.delay(2000)
                                done = True
                                break
                                
                            
                            current_turn = "X" if current_turn == "O" else "O"
                            pygame.display.set_caption(f"Tic Tac Toe - {current_turn}'s turn")
                            
                            if mode == "player_vs_ai" and current_turn == ai_symbol:
                                pygame.time.delay(500)
                                self.play_ai()
                                
                                if self.is_game_over():
                                    self.draw_game()
                                    if self.winner == "Draw":
                                        pygame.display.set_caption("Game Over! It's a Draw!")
                                    else:
                                        pygame.display.set_caption(f"Game Over! {self.winner} wins!")
                                    pygame.time.delay(2000)
                                    return  # Return from the function completely instead of just breaking
                                
                                current_turn = "X" if current_turn == "O" else "O"
                                pygame.display.set_caption(f"Tic Tac Toe - {current_turn}'s turn")
            
            pygame.display.update()
            clock.tick(60)
    
    
if __name__ == "__main__":
    tictactoegame = RandomBoardTicTacToe()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[1] < tictactoegame.controls_height:
                    if 380 <= pos[0] <= 460 and 75 <= pos[1] <= 105:
                        tictactoegame.dropdown_open = not tictactoegame.dropdown_open
                        tictactoegame.draw_game()
                    
                    elif tictactoegame.dropdown_open and 380 <= pos[0] <= 460:
                        for i, size in enumerate(tictactoegame.dropdown_options):
                            option_y = 105 + i * 30
                            if option_y <= pos[1] <= option_y + 30:
                                tictactoegame.GRID_SIZE = size
                                tictactoegame.game_reset()
                                tictactoegame.dropdown_open = False
                                break
                    
                    elif 20 <= pos[0] <= 45:
                        if 80 <= pos[1] <= 95:
                            tictactoegame.player_symbol = "O"
                            tictactoegame.draw_game()
                        elif 105 <= pos[1] <= 120:
                            tictactoegame.player_symbol = "X"
                            tictactoegame.draw_game()
                        elif 130 <= pos[1] <= 145:
                            tictactoegame.game_mode = "human_vs_human"
                            tictactoegame.draw_game()
                        elif 155 <= pos[1] <= 170:
                            tictactoegame.game_mode = "player_vs_ai"
                            tictactoegame.draw_game()
                    
                    elif 190 <= pos[0] <= 215:
                        if  80 <= pos[1] <= 95:
                            
                            tictactoegame.use_minimax = True
                            tictactoegame.draw_game()
                        elif 105 <= pos[1] <= 120:
                            
                            tictactoegame.use_minimax = False
                            tictactoegame.draw_game()
                    
                    
                    elif 430 <= pos[0] <= 550 and 160 <= pos[1] <= 190:
                        tictactoegame.play_game(tictactoegame.game_mode)
                elif 220 <= pos[0] <= 245:
                    if 75 <= pos[1] <= 95:
                        tictactoegame.use_minimax = True
                        tictactoegame.draw_game()
                        print("Selected Minimax algorithm from multiAgents.py")
                    elif 100 <= pos[1] <= 120:
                        tictactoegame.use_minimax = False
                        tictactoegame.draw_game()
                        print("Selected Negamax algorithm from multiAgents.py")
        
        
        pygame.display.update()
            
    pygame.quit()
