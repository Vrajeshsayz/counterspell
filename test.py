import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Humanoid Movement, Punching, Kicking, and AI Interaction")

# Load the background images
background_home = pygame.image.load("images/Home.png")
background_home = pygame.transform.scale(background_home, (WIDTH, HEIGHT))

background_game = pygame.image.load("images/character.png")
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))

background_info = pygame.image.load("images/info.png")
background_info = pygame.transform.scale(background_info, (WIDTH, HEIGHT))

background_fight = pygame.image.load("images/fight.png")
background_fight = pygame.transform.scale(background_fight, (WIDTH, HEIGHT))

# Load winning and losing backgrounds
background_win = pygame.image.load("images/win.png")
background_win = pygame.transform.scale(background_win, (WIDTH, HEIGHT))

background_lose = pygame.image.load("images/lose.png")
background_lose = pygame.transform.scale(background_lose, (WIDTH, HEIGHT))

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)  # Color for the AI character
BLACK = (0, 0, 0)    # Color for text

# Button class
class Button:
    def __init__(self, text, pos, size):
        self.text = text
        self.pos = pos
        self.size = size
        self.font = pygame.font.Font(None, 74)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.active = False  # Track if the button is active

    def draw(self, surface):
        color = GREEN if self.active else WHITE  # Change color based on active state
        pygame.draw.rect(surface, color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Create buttons
play_button = Button("Play", (400, 300), (200, 50))
info_button = Button("Info", (400, 400), (200, 50))
fight_button = Button("Fight", (750, 500), (200, 50))
back_button_game = Button("Back", (50, 500), (200, 50))

# Create buttons for the play screen
superPunch_button = Button("Super Punch", (25, 300), (350, 50))
superKick_button = Button("Super Kick", (300, 400), (350, 50))
superSpeed_button = Button("Super Speed", (650, 300), (350, 50))

# Create buttons for win and lose screens
play_again_button = Button("Play Again", (400, 300), (200, 50))

# Character properties
x, y = WIDTH // 2, HEIGHT // 2
normal_height = 100  # Height of the standing character
crouch_height = 50   # Height of the crouching character
movement_speed = 2   # Fixed movement speed
gravity = 1
jump_strength = -15
ground = HEIGHT - normal_height  # ground level

# Health
player_health = 500
ai_health = 500

# Punching, crouching, and kicking state
is_punching = False
is_crouching = False
is_kicking = False
kick_duration = 10  # Number of frames the kick lasts
kick_counter = 0    # Frame counter for the kick
punch_duration = 10  # Number of frames the punch lasts
punch_counter = 0    # Frame counter for the punch

# AI character properties
ai_x, ai_y = random.randint(0, WIDTH - 40), random.randint(0, HEIGHT - 140)
ai_velocity_x = 0 # AI movement logic
ai_speed = 1
ai_direction = random.choice([-1, 1])  # Randomly choose direction

# Function to reset the game
def reset_game():
    global player_health, ai_health, x, y, is_punching, is_crouching, is_kicking
    player_health = 500
    ai_health = 500
    x, y = WIDTH // 2, HEIGHT // 2
    is_punching = False
    is_crouching = False
    is_kicking = False

# Function to draw the win screen
def draw_win_screen():
    screen.blit(background_win, (0, 0))
    play_again_button.draw(screen)

# Function to draw the lose screen
def draw_lose_screen():
    screen.blit(background_lose, (0, 0))
    play_again_button.draw(screen)

# Main game loop
running = True
game_state = "home"  # Possible states: home, game, win, lose
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == "win" and play_again_button.is_hovered(mouse_pos):
                reset_game()
                game_state = "game"
            elif game_state == "lose" and play_again_button.is_hovered(mouse_pos):
                reset_game()
                game_state = "game"
            elif game_state == "home":
                if play_button.is_hovered(mouse_pos):
                    game_state = "game"
                elif info_button.is_hovered(mouse_pos):
                    game_state = "info"

    if game_state == "game":
        # Game logic here
        # Check for win/lose conditions
        if player_health <= 0:
            game_state = "lose"
        elif ai_health <= 0:
            game_state = "win"

        # Drawing the game screen
        screen.blit(background_fight, (0, 0))
        # Draw player and AI characters, health bars, etc.

    elif game_state == "win":
        draw_win_screen()
    elif game_state == "lose":
        draw_lose_screen()

    # Draw buttons
    if game_state == "home":
        play_button.draw(screen)
        info_button.draw(screen)
    elif game_state == "game":
        fight_button.draw(screen)

    pygame.display.update()

# Quit Pygame
pygame.quit()