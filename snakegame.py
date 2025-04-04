import pygame
import time
import random
import os

# Initialize pygame
pygame.init()

# Function to load sound safely
def load_sound(filename):
    """Load sound file safely, return None if file does not exist."""
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    else:
        return None

# Load sound effects
game_over_sound = load_sound("game_over.wav")
food_eat_sound = load_sound("eat.wav")
background_music = load_sound("background.wav")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLUE = (50, 50, 213)  # Special food color
GRID_COLOR = (50, 50, 50)

# Screen dimensions
WIDTH = 600
HEIGHT = 400

# Snake block size
BLOCK_SIZE = 10

# Speed control
clock = pygame.time.Clock()

# Font style
font = pygame.font.SysFont("bahnschrift", 25)

# Function to draw grid lines for better visibility
def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

# Function to draw the snake
def draw_snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], block_size, block_size], border_radius=5)

# Function to draw food
def draw_food(x, y, color):
    pygame.draw.circle(screen, color, (int(x + BLOCK_SIZE / 2), int(y + BLOCK_SIZE / 2)), BLOCK_SIZE // 2)

# Function to display messages on screen
def display_message(msg, color, position):
    message = font.render(msg, True, color)
    screen.blit(message, position)

# Function to create a fade-out effect when game over
def fade_out():
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(50)

# Main game loop
def game_loop():
    game_over = False
    game_close = False
    
    # Initial position of the snake
    x = WIDTH / 2
    y = HEIGHT / 2
    x_change = 0
    y_change = 0
    
    # Snake properties
    snake_list = []
    length_of_snake = 1
    speed = 10
    
    # Generate initial food positions
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
    
    special_food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    special_food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
    
    # Create game screen
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Removed full-screen mode
    pygame.display.set_caption("Snake Game - Score: 0")
    
    score = 0
    
    # Play background music if available
    if background_music:
        background_music.play(-1)  # Loop indefinitely
    
    while not game_over:
        while game_close:
            fade_out()
            screen.fill(BLACK)
            display_message("Game Over! Press C-Continue or Q-Quit", RED, [WIDTH / 6, HEIGHT / 3])
            pygame.display.update()
            if game_over_sound:
                game_over_sound.play()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_game()
                elif event.key == pygame.K_LEFT:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    x_change = 0
                    y_change = -BLOCK_SIZE
                elif event.key == pygame.K_DOWN:
                    x_change = 0
                    y_change = BLOCK_SIZE
        
        # Check if snake hits boundaries
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True
        
        # Update snake position
        x += x_change
        y += y_change
        
        screen.fill(BLACK)
        draw_grid()
        draw_food(food_x, food_y, RED)
        draw_food(special_food_x, special_food_y, BLUE)
        
        snake_head = [x, y]
        snake_list.append(snake_head)
        
        if len(snake_list) > length_of_snake:
            del snake_list[0]
        
        # Check if snake collides with itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True
        
        draw_snake(BLOCK_SIZE, snake_list)
        pygame.display.update()
        
        # Check if snake eats regular food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            length_of_snake += 1
            speed += 1
            score += 10
            if food_eat_sound:
                food_eat_sound.play()
        
        # Check if snake eats special food
        if x == special_food_x and y == special_food_y:
            special_food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            special_food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            length_of_snake += 2
            speed += 2
            score += 25
            if food_eat_sound:
                food_eat_sound.play()
        
        pygame.display.set_caption(f"Snake Game - Score: {score}")
        clock.tick(speed)
    
    pygame.quit()
    quit()

# Function to pause the game
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False
        display_message("Game Paused. Press P to Resume", WHITE, [WIDTH / 6, HEIGHT / 3])
        pygame.display.update()

game_loop()
