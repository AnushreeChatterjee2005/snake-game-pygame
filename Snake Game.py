"""
Snake Eater - Modern Visual Edition
Made with PyGame
"""

import pygame, sys, time, random
import math

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Eater - Neon Edition')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B) - Modern Neon/Cyberpunk Theme
bg_dark = pygame.Color(15, 15, 35)  # Deep space blue
bg_accent = pygame.Color(25, 25, 55)  # Slightly lighter for gradient
grid_color = pygame.Color(40, 40, 80)  # Subtle grid lines

# Snake gradient colors (head to tail)
snake_head = pygame.Color(0, 255, 200)  # Bright cyan
snake_mid = pygame.Color(100, 200, 255)  # Sky blue
snake_tail = pygame.Color(150, 100, 255)  # Purple
snake_border = pygame.Color(255, 255, 255)  # White border

# Food colors
food_color = pygame.Color(255, 50, 100)  # Hot pink/red
food_glow = pygame.Color(255, 100, 150)  # Lighter pink for glow
food_border = pygame.Color(255, 200, 220)  # Very light pink

# UI colors
text_primary = pygame.Color(255, 255, 255)  # White
text_accent = pygame.Color(0, 255, 200)  # Cyan
text_shadow = pygame.Color(0, 0, 0)  # Black for shadows
game_over_color = pygame.Color(255, 80, 80)  # Bright red


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0
food_pulse = 0  # For food animation


# Helper function to draw gradient background
def draw_gradient_background():
    for y in range(frame_size_y):
        # Create gradient from bg_dark to bg_accent
        ratio = y / frame_size_y
        r = int(bg_dark.r + (bg_accent.r - bg_dark.r) * ratio)
        g = int(bg_dark.g + (bg_accent.g - bg_dark.g) * ratio)
        b = int(bg_dark.b + (bg_accent.b - bg_dark.b) * ratio)
        pygame.draw.line(game_window, (r, g, b), (0, y), (frame_size_x, y))


# Helper function to draw grid
def draw_grid():
    for x in range(0, frame_size_x, 20):
        pygame.draw.line(game_window, grid_color, (x, 0), (x, frame_size_y), 1)
    for y in range(0, frame_size_y, 20):
        pygame.draw.line(game_window, grid_color, (0, y), (frame_size_x, y), 1)


# Helper function to get gradient color for snake
def get_snake_color(index, total_length):
    if total_length == 1:
        return snake_head
    
    # Calculate position ratio (0 = head, 1 = tail)
    ratio = index / max(1, total_length - 1)
    
    if ratio < 0.5:
        # Transition from head to mid
        local_ratio = ratio * 2
        r = int(snake_head.r + (snake_mid.r - snake_head.r) * local_ratio)
        g = int(snake_head.g + (snake_mid.g - snake_head.g) * local_ratio)
        b = int(snake_head.b + (snake_mid.b - snake_head.b) * local_ratio)
    else:
        # Transition from mid to tail
        local_ratio = (ratio - 0.5) * 2
        r = int(snake_mid.r + (snake_tail.r - snake_mid.r) * local_ratio)
        g = int(snake_mid.g + (snake_tail.g - snake_mid.g) * local_ratio)
        b = int(snake_mid.b + (snake_tail.b - snake_mid.b) * local_ratio)
    
    return pygame.Color(r, g, b)


# Game Over
def game_over():
    # Draw gradient background
    draw_gradient_background()
    draw_grid()
    
    # Main game over text with shadow
    my_font = pygame.font.SysFont('arial black', 90)
    
    # Shadow
    shadow_surface = my_font.render('GAME OVER', True, text_shadow)
    shadow_rect = shadow_surface.get_rect()
    shadow_rect.midtop = (frame_size_x/2 + 4, frame_size_y/4 + 4)
    game_window.blit(shadow_surface, shadow_rect)
    
    # Main text
    game_over_surface = my_font.render('GAME OVER', True, game_over_color)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.blit(game_over_surface, game_over_rect)
    
    show_score(0, text_accent, 'arial', 30)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score with enhanced styling
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    
    # Shadow
    shadow_surface = score_font.render('SCORE: ' + str(score), True, text_shadow)
    shadow_rect = shadow_surface.get_rect()
    
    # Main text
    score_surface = score_font.render('SCORE: ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    
    if choice == 1:
        shadow_rect.midtop = (frame_size_x/10 + 2, 17)
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        shadow_rect.midtop = (frame_size_x/2 + 2, frame_size_y/1.25 + 2)
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    
    game_window.blit(shadow_surface, shadow_rect)
    game_window.blit(score_surface, score_rect)


# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    # Update food pulse animation
    food_pulse = (food_pulse + 0.15) % (2 * math.pi)

    # GFX - Draw gradient background
    draw_gradient_background()
    draw_grid()
    
    # Draw snake with gradient and borders
    for index, pos in enumerate(snake_body):
        # Get gradient color based on position
        segment_color = get_snake_color(index, len(snake_body))
        
        # Draw glow effect (larger, semi-transparent rectangle)
        glow_surface = pygame.Surface((14, 14), pygame.SRCALPHA)
        glow_color = (*segment_color[:3], 100)  # Semi-transparent
        pygame.draw.rect(glow_surface, glow_color, (0, 0, 14, 14), border_radius=3)
        game_window.blit(glow_surface, (pos[0] - 2, pos[1] - 2))
        
        # Draw main body with rounded corners
        pygame.draw.rect(game_window, segment_color, pygame.Rect(pos[0], pos[1], 10, 10), border_radius=2)
        
        # Draw border
        pygame.draw.rect(game_window, snake_border, pygame.Rect(pos[0], pos[1], 10, 10), 1, border_radius=2)

    # Draw food with pulsing glow effect
    pulse_size = int(2 + abs(math.sin(food_pulse)) * 3)
    
    # Outer glow
    glow_surface = pygame.Surface((10 + pulse_size * 2, 10 + pulse_size * 2), pygame.SRCALPHA)
    glow_alpha = int(100 + abs(math.sin(food_pulse)) * 100)
    glow_color = (*food_glow[:3], glow_alpha)
    pygame.draw.rect(glow_surface, glow_color, (0, 0, 10 + pulse_size * 2, 10 + pulse_size * 2), border_radius=5)
    game_window.blit(glow_surface, (food_pos[0] - pulse_size, food_pos[1] - pulse_size))
    
    # Main food
    pygame.draw.rect(game_window, food_color, pygame.Rect(food_pos[0], food_pos[1], 10, 10), border_radius=2)
    
    # Food border
    pygame.draw.rect(game_window, food_border, pygame.Rect(food_pos[0], food_pos[1], 10, 10), 2, border_radius=2)

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, text_primary, 'arial', 24)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)