import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Home Screen")

# Load the background images
background_home = pygame.image.load("images/Home.png")
background_home = pygame.transform.scale(background_home, (WIDTH, HEIGHT))

background_game = pygame.image.load("images/character.png")
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))

background_info = pygame.image.load("images/info.png")
background_info = pygame.transform.scale(background_info, (WIDTH, HEIGHT))

background_fight = pygame.image.load("images/fight.png")
background_fight = pygame.transform.scale(background_fight, (WIDTH, HEIGHT))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

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

# Create buttons for the game screen
fight_button = Button("Fight", (750, 500), (200, 50))
back_button_game = Button("Back", (50, 500), (200, 50))

# Create buttons for the play screen
superPunch_button = Button("Super Punch", (25, 300), (350, 50))
superKick_button = Button("Super Kick", (300, 400), (350, 50))
superSpeed_button = Button("Super Speed", (650, 300), (350, 50))

# Variables to keep track of the active actions
active_action = None

# Function to draw the home screen
def draw_home_screen():
    screen.blit(background_home, (0, 0))
    play_button.draw(screen)
    info_button.draw(screen)

# Function to draw the game screen
def draw_game_screen():
    screen.blit(background_game, (0, 0))
    superPunch_button.draw(screen)
    superKick_button.draw(screen)
    superSpeed_button.draw(screen)
    fight_button.draw(screen)  # Draw the fight button
    back_button_game.draw(screen)

    # Display the active action
    font = pygame.font.Font(None, 50)
    action_text = f"Active Action: {active_action}" if active_action else "No Action Selected"
    text_surface = font.render(action_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(text_surface, text_rect)

# Function to draw the info screen
def draw_info_screen():
    screen.blit(background_info, (0, 0))
    font = pygame.font.Font(None, 74)
    back_button_info = Button("Back", (700, 510), (200, 50))
    back_button_info.draw(screen)
    return back_button_info

# Function to draw the fight screen
def draw_fight_screen():
    screen.blit(background_fight, (0, 0))
    font = pygame.font.Font(None, 74)
    # You can add fight-related elements here

# Main loop
current_screen = "home"
back_button_info = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "home":
                if play_button.is_hovered(event.pos):
                    current_screen = "game"
                elif info_button.is_hovered(event.pos):
                    current_screen = "info"
            elif current_screen == "game":
                if superPunch_button.is_hovered(event.pos):
                    active_action = "Super Punch"
                    superPunch_button.active = True
                    superKick_button.active = False
                    superSpeed_button.active = False
                elif superKick_button.is_hovered(event.pos):
                    active_action = "Super Kick"
                    superPunch_button.active = False
                    superKick_button.active = True
                    superSpeed_button.active = False
                elif superSpeed_button.is_hovered(event.pos):
                    active_action = "Super Speed"
                    superPunch_button.active = False
                    superKick_button.active = False
                    superSpeed_button.active = True
                elif fight_button.is_hovered(event.pos):
                    current_screen = "fight"  # Switch to fight screen
                elif back_button_game.is_hovered(event.pos):
                    current_screen = "home"
            elif current_screen == "info":
                if back_button_info.is_hovered(event.pos):
                    current_screen = "home"
            elif current_screen == "fight":
                # Logic for fight screen can be added here
                pass

    # Clear the screen
    screen.fill(BLACK)

    # Draw the current screen
    if current_screen == "home":
        draw_home_screen()
    elif current_screen == "game":
        draw_game_screen()
    elif current_screen == "info":
        back_button_info = draw_info_screen()
    elif current_screen == "fight":
        draw_fight_screen()  # Draw the fight screen

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()