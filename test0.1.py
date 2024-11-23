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

bg_image = pygame.image.load('images/fight.png')  # Ensure this image is in the same directory

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
play_again_button = Button("Play Again", (400, 300), (200, 50))

# Create buttons for the play screen
superPunch_button = Button("Super Punch", (25, 300), (350, 50))
superKick_button = Button("Super Kick", (300, 400), (350, 50))
superSpeed_button = Button("Super Speed", (650, 300), (350, 50))

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
ai_velocity_x = 0
ai_velocity_y = 0
ai_on_ground = True
ai_is_punching = False
ai_is_kicking = False
ai_punch_counter = 0
ai_kick_counter = 0

# Main loop
clock = pygame.time.Clock()
on_ground = True
velocity_y = 0  # Initialize player vertical velocity # Set up font for labels
font = pygame.font.Font(None, 36)

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

# Function to draw the fight screen
def draw_fight_screen():
    if game_state == "game":
        # Game logic here
        global x, y, player_health, ai_health, is_punching, is_kicking, kick_counter, punch_counter
        global ai_x, ai_y, ai_is_punching, ai_is_kicking, ai_punch_counter, ai_kick_counter, is_crouching
        global on_ground, velocity_y, ai_on_ground, ai_velocity_y, ai_velocity_x  # Declare these as global

        screen.blit(background_fight, (0, 0))

    # Get the keys pressed
        keys = pygame.key.get_pressed()

    # Horizontal movement for the player
        if keys[pygame.K_a]:  # Move left
            x -= movement_speed
        if keys[pygame.K_d]:  # Move right
            x += movement_speed

    # Jumping
        if keys[pygame.K_w] and on_ground and not is_crouching:  # Jump
            velocity_y = jump_strength
            on_ground = False

    # Crouching
        if keys[pygame.K_s]:  # Crouch
            is_crouching = True
        else:
            is_crouching = False

    # Punching
        if keys[pygame.K_p] and not is_punching:  # Punch
            is_punching = True
            punch_counter = punch_duration

    # Kicking
        if keys[pygame.K_k] and not is_kicking:  # Kick
            is_kicking = True
            kick_counter = kick_duration

    # Apply gravity
        if not on_ground:
            velocity_y += gravity

     # Update vertical position
        y += velocity_y

    # Ground collision for player
        if y >= ground:
            y = ground
            velocity_y = 0
            on_ground = True

    # Prevent the character from moving off-screen
        if x < 0:
            x = 0
        if x > WIDTH - 40:  # Width of the character
            x = WIDTH - 40

    # Update punch state
        if is_punching:
            punch_counter -= 1
            if punch_counter <= 0:
                is_punching = False

    # Update kick state
        if is_kicking:
            kick_counter -= 1
            if kick_counter <= 0:
                is_kicking = False

    # AI movement and attack logic
        ai_velocity_x = 0
        if ai_on_ground:
            if random.random() < 0.02:  # Randomly decide to move left or right
                ai_velocity_x = random.choice([-1, 1]) * 2  # AI speed

    # Update AI position
        ai_x += ai_velocity_x

    # AI decision to attack
    attack_range = 100  # Define the attack range
    if abs(ai_x - x) < attack_range:  # If the player is within the attack range
        if not ai_is_punching and not ai_is_kicking:  # Ensure AI is not already attacking
            if random.random() < 0.05:  # Random chance to attack
                if random.random() < 0.5:  # 50% chance to punch
                    ai_is_punching = True
                    ai_punch_counter = punch_duration
                else:  # 50% chance to kick
                    ai_is_kicking = True
                    ai_kick_counter = kick_duration

    # Apply gravity for AI
    ai_velocity_y += gravity

    # Update AI position
    ai_y += ai_velocity_y

    # Ground collision for AI
    if ai_y >= ground:
        ai_y = ground
        ai_velocity_y = 0
        ai_on_ground = True

    # Update AI punch state
    if ai_is_punching:
        ai_punch_counter -= 1
        if ai_punch_counter <= 0:
            ai_is_punching = False

    # Update AI kick state
    if ai_is_kicking:
        ai_kick_counter -= 1
        if ai_kick_counter <= 0:
            ai_is_kicking = False

    if is_punching and (abs(x - ai_x) < 40) and (abs(y - ai_y) < 100):
        ai_health -= 0.5
        is_punching = False  # Reset player punch

    if is_kicking and abs(x - ai_x) < 40 and abs(y - ai_y) < 100:  # Player kicks AI
        ai_health -= 1
        is_kicking = False  # Reset player kick

    if ai_is_punching and abs(ai_x - x) < 40 and abs(ai_y - y) < 100:  # AI punches player
        player_health -= 5
        ai_is_punching = False  # Reset AI punch

    if ai_is_kicking and abs(ai_x - x) < 40 and abs(ai_y - y) < 100:  # AI kicks player
        player_health -= 5
        ai_is_kicking = False  # Reset AI kick

    # Fill the screen with white
    screen.blit(background_fight, (0, 0))
    # Draw the humanoid character (player)
    head_radius = 15
    body_width = 20
    body_height = normal_height if not is_crouching else crouch_height

    # Draw player head
    pygame.draw.circle(screen, BLUE, (int(x + body_width // 2), int(y - body_height - head_radius)), head_radius)

    # Draw player body
    pygame.draw.rect(screen, BLUE, (x + body_width // 2 - body_width // 2, y - body_height, body_width, body_height))

    # Draw player arms
    arm_length = 40
    if is_punching:
        # Punching position
        pygame.draw.line(screen, BLUE, (x + body_width // 2, y - (body_height // 2 + head_radius)),
                         (x + body_width // 2 + arm_length * 1.5, y - (body_height // 2 + head_radius)), 5)
    else:
        # Normal arms position
        pygame.draw.line(screen, BLUE, (x + body_width // 2 - arm_length, y - (body_height // 2 + head_radius)),
                         (x + body_width // 2 + arm_length, y - (body_height // 2 + head_radius)), 5)

    # Draw player legs
    leg_length = 100
    if is_kicking:
        # Kicking position (extend the right leg)
        pygame.draw.line(screen, BLUE, (x + body_width // 2, y),
                         (x + body_width // 2 + 30, y - 30), 5)  # Right leg extended for kick
    else:
        # Normal legs position
        pygame.draw.line(screen, BLUE, (x + body_width // 2, y),
                         (x + body_width // 10, y + leg_length), 5)  # Left leg
        pygame.draw.line(screen, BLUE, (x + body_width // 2, y),
                         (x + body_width // 10 + body_width, y + leg_length), 5)  # Right leg

    # Draw the AI character
    ai_head_radius = 15
    ai_body_width = 20
    ai_body_height = normal_height

    # Draw AI head
    pygame.draw.circle(screen, GREEN, (int(ai_x + ai_body_width // 2), int(ai_y - ai_body_height - ai_head_radius)), ai_head_radius)

    # Draw AI body
    pygame.draw.rect(screen, GREEN, (ai_x + ai_body_width // 2 - ai_body_width // 2, ai_y - ai_body_height, ai_body_width, ai_body_height))

    # Draw AI arms
    ai_arm_length = 40
    if ai_is_punching:
        # Punching position
        pygame.draw.line(screen, GREEN, (ai_x + ai_body_width // 2, ai_y - (ai_body_height // 2 + ai_head_radius)),
                         (ai_x + ai_body_width // 2 + ai_arm_length * 1.5, ai_y - (ai_body_height // 2 + ai_head_radius)), 5)
    else:
        # Normal arms position
        pygame.draw.line(screen, GREEN, (ai_x + ai_body_width // 2 - ai_arm_length, ai_y - (ai_body_height // 2 + ai_head_radius)),
                         (ai_x + ai_body_width // 2 + ai_arm_length, ai_y - (ai_body_height // 2 + ai_head_radius)), 5)

    # Draw AI legs
    ai_leg_length = 100
    if ai_is_kicking:
        # K icking position (extend the right leg)
        pygame.draw.line(screen, GREEN, (ai_x + ai_body_width // 2, ai_y),
                         (ai_x + ai_body_width // 2 + 30, ai_y - 30), 5)  # Right leg extended for kick
    else:
        # Normal legs position
        pygame.draw.line(screen, GREEN, (ai_x + ai_body_width // 2, ai_y),
                         (ai_x + ai_body_width // 10, ai_y + ai_leg_length), 5)  # Left leg
        pygame.draw.line(screen, GREEN, (ai_x + ai_body_width // 2, ai_y),
                         (ai_x + ai_body_width // 10 + ai_body_width, ai_y + ai_leg_length), 5)  # Right leg

    # Draw health bars
    player_health_bar_length = 50
    ai_health_bar_length = 50
    player_health_ratio = player_health / 100
    ai_health_ratio = ai_health / 100

    # Player health bar in the top left corner
    pygame.draw.rect(screen, BLACK, (10, 10, player_health_bar_length, 10))
    pygame.draw.rect(screen, GREEN, (10, 10, player_health_bar_length * player_health_ratio, 10))
    player_health_label = font.render("Player Health", True, BLACK)
    screen.blit(player_health_label, (30, 25))

    # AI health bar in the top right corner
    pygame.draw.rect(screen, BLACK, (WIDTH - 310, 10, ai_health_bar_length, 10))
    pygame.draw.rect(screen, GREEN, (WIDTH - 310, 10, ai_health_bar_length * ai_health_ratio, 10))
    ai_health_label = font.render("AI Health", True, BLACK)
    screen.blit(ai_health_label, (WIDTH - 310, 25))

    if player_health <= 0:
        print("Game Over! The computer has defeated you.")
        pygame.quit()
        sys.exit()
    if ai_health <= 0:
        print("You have defeated the computer!")
        # Check for win/lose conditions
    if player_health <= 0:
        game_state = "lose"
    elif ai_health <= 0:
        game_state = "win"
def draw_info_screen():
    screen.blit(background_info, (0, 0))
    font = pygame.font.Font(None, 74)
    back_button_info = Button("Back", (700, 510), (200, 50))
    back_button_info.draw(screen)
    return back_button_info
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

# Main loop
current_screen = "home"
back_button_info = None

running = True
game_state = "home"
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
            # Draw buttons
        if game_state == "home":
            play_button.draw(screen)
            info_button.draw(screen)
        elif game_state == "game":
            fight_button.draw(screen)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the current screen
    if current_screen == "home":
        draw_home_screen()
    elif current_screen == "game":
        draw_game_screen()
    elif current_screen == "info":
        # Assuming draw_info_screen() is defined elsewhere
        back_button_info = draw_info_screen()
    elif current_screen == "fight":
        draw_fight_screen()  # Draw the fight screen
    elif game_state == "win":
        draw_win_screen()
    elif game_state == "lose":
        draw_lose_screen()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()