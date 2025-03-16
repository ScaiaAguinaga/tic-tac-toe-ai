import pygame
import sys

class TicTacToeBoard: #determines board window and cell size
    def __init__(self):
        pygame.init()
        self.WINDOW_SIZE = 600  
        self.BOARD_SIZE = 4  
        self.CELL_SIZE = 80  
        
        # colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (65, 105, 225)  
        
        # This essentialyl creates the display
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("Tic-Tac-Toe Large Board")
        
        # gamestate
        self.board = [['' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.human_symbol = 'X'  
        self.computer_symbol = 'O'
        self.game_mode = "Human vs computer"  
        self.human_score = 0
        self.computer_score = 0
        self.winner = None
        
        
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 36)
        
        
        self.radio_buttons = {
            'nought': pygame.Rect(30, 60, 15, 15),
            'cross': pygame.Rect(30, 90, 15, 15),
            'hvh': pygame.Rect(30, 140, 15, 15),
            'hvc': pygame.Rect(30, 170, 15, 15)
        }
        
        # button to sttart game
        self.start_button = pygame.Rect(self.WINDOW_SIZE - 150, 120, 120, 40)
        
        
        self.size_dropdown = pygame.Rect(self.WINDOW_SIZE - 150, 60, 80, 30)
        self.dropdown_open = False

    def draw_interface(self): #draws interface containing title and selectons
        self.screen.fill(self.WHITE)
        
        
        title = self.title_font.render("Tic-Tac-Toe large board", True, self.BLACK)
        self.screen.blit(title, (20, 20))
        
       
        symbol_text = self.font.render("Select human player symbol", True, self.BLACK)
        self.screen.blit(symbol_text, (50, 30))
        
        
        for button, rect in self.radio_buttons.items():
            pygame.draw.circle(self.screen, self.BLACK, rect.center, 7, 1)
            if (button == 'nought' and self.human_symbol == 'O') or \
               (button == 'cross' and self.human_symbol == 'X') or \
               (button == 'hvh' and self.game_mode == "Human vs human") or \
               (button == 'hvc' and self.game_mode == "Human vs computer"):
                pygame.draw.circle(self.screen, self.BLACK, rect.center, 4)
            
            
            label_text = ""
            if button == 'nought': label_text = "Nought (O)"
            elif button == 'cross': label_text = "Cross (X)"
            elif button == 'hvh': label_text = "Human vs human"
            elif button == 'hvc': label_text = "Human vs computer"
            
            label = self.font.render(label_text, True, self.BLACK)
            self.screen.blit(label, (rect.right + 10, rect.top - 5))
        
        
        size_text = self.font.render("Board size:", True, self.BLACK)
        self.screen.blit(size_text, (self.WINDOW_SIZE - 250, 65))
        pygame.draw.rect(self.screen, self.BLACK, self.size_dropdown, 1)
        size_value = self.font.render(f"{self.BOARD_SIZE}x{self.BOARD_SIZE}", True, self.BLACK)
        self.screen.blit(size_value, (self.size_dropdown.x + 5, self.size_dropdown.y + 5))
        
        
        pygame.draw.rect(self.screen, self.BLUE, self.start_button)
        start_text = self.font.render("Start game", True, self.WHITE)
        self.screen.blit(start_text, (self.start_button.centerx - start_text.get_width()//2,
                                    self.start_button.centery - start_text.get_height()//2))
        
        # scores
        score_text = self.font.render(f"Scores (Human: {self.human_score}, Computer: {self.computer_score})",
                                    True, self.BLACK)
        self.screen.blit(score_text, (20, 200))
        
        
        if self.winner:
            winner_text = self.font.render(f"Winner: {self.winner}", True, self.BLACK)
            self.screen.blit(winner_text, (self.WINDOW_SIZE//2 - winner_text.get_width()//2, 200))
        
        self.draw_board()

    def draw_board(self):
        board_size_pixels = self.BOARD_SIZE * self.CELL_SIZE
        board_start_x = (self.WINDOW_SIZE - board_size_pixels) // 2
        board_start_y = 250  
        
        # creates grid
        for i in range(self.BOARD_SIZE + 1):
            
            pygame.draw.line(self.screen, self.BLACK,
                           (board_start_x + i * self.CELL_SIZE, board_start_y),
                           (board_start_x + i * self.CELL_SIZE, board_start_y + board_size_pixels), 2)
            
            pygame.draw.line(self.screen, self.BLACK,
                           (board_start_x, board_start_y + i * self.CELL_SIZE),
                           (board_start_x + board_size_pixels, board_start_y + i * self.CELL_SIZE), 2)
        
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col]:
                    x = board_start_x + col * self.CELL_SIZE + self.CELL_SIZE // 2
                    y = board_start_y + row * self.CELL_SIZE + self.CELL_SIZE // 2
                    if self.board[row][col] == 'X':
                        self.draw_x(x, y)
                    else:
                        self.draw_o(x, y)
        
        pygame.display.flip()

    def draw_x(self, x, y):
        size = self.CELL_SIZE // 3
        pygame.draw.line(self.screen, self.BLACK,
                        (x - size, y - size),
                        (x + size, y + size), 3)
        pygame.draw.line(self.screen, self.BLACK,
                        (x + size, y - size),
                        (x - size, y + size), 3)

    def draw_o(self, x, y):
        size = self.CELL_SIZE // 3
        pygame.draw.circle(self.screen, self.BLACK,
                         (x, y), size, 3)

    def handle_click(self, pos):
        
        for button, rect in self.radio_buttons.items():
            if rect.collidepoint(pos):
                if button == 'nought':
                    self.human_symbol = 'O'
                    self.computer_symbol = 'X'
                elif button == 'cross':
                    self.human_symbol = 'X'
                    self.computer_symbol = 'O'
                elif button == 'hvh':
                    self.game_mode = "Human vs human"
                elif button == 'hvc':
                    self.game_mode = "Human vs computer"
                return None

        
        if self.start_button.collidepoint(pos):
            self.reset_game()
            return None

        
        if self.size_dropdown.collidepoint(pos):
            self.dropdown_open = not self.dropdown_open
            return None

        
        return self.get_cell_from_mouse(pos)

    def get_cell_from_mouse(self, pos):
        board_size_pixels = self.BOARD_SIZE * self.CELL_SIZE
        board_start_x = (self.WINDOW_SIZE - board_size_pixels) // 2
        board_start_y = 250

        x, y = pos
        if (board_start_x <= x <= board_start_x + board_size_pixels and
            board_start_y <= y <= board_start_y + board_size_pixels):
            row = (y - board_start_y) // self.CELL_SIZE
            col = (x - board_start_x) // self.CELL_SIZE
            if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
                return row, col
        return None

    def reset_game(self):
        self.board = [['' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.winner = None
