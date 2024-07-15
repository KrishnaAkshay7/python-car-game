import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the game window
pygame.display.set_caption("Car Game")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Define fonts
font = pygame.font.SysFont(None, 50)

# Define car dimensions
car_width = 175
car_height = 200

# Load car image
car_image_path = os.path.join('D:', 'car.png')
car_img = pygame.image.load(car_image_path).convert_alpha()
car_img = pygame.transform.scale(car_img, (car_width, car_height))

# Load traffic cone image
cone_image_path = os.path.join('D:', 'traffic_cone.png')
cone_img = pygame.image.load(cone_image_path).convert_alpha()
cone_img = pygame.transform.scale(cone_img, (50, 50))  # Resize the cone image as needed

# Load lane line image
lane_line_path = os.path.join('D:', 'lane_line.png')
lane_line_img = pygame.image.load(lane_line_path).convert_alpha()
lane_line_img = pygame.transform.scale(lane_line_img, (60, screen_height))  # Resize the lane line image

# Set clock
clock = pygame.time.Clock()

# Define functions
def display_score(score):
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, (10, 10))

def display_car(x, y):
    screen.blit(car_img, (x, y))

def generate_obstacle():
    obstacle_width = 60
    obstacle_height = 60
    obstacle_x = random.randint(0, screen_width - obstacle_width)
    obstacle_y = -obstacle_height
    obstacle_speed = random.randint(3, 6)
    return {
        'x': obstacle_x,
        'y': obstacle_y,
        'width': obstacle_width,
        'height': obstacle_height,
        'speed': obstacle_speed
    }

def game_loop():
    # Initialize game variables
    x = (screen_width - car_width) // 2
    y = screen_height - car_height
    car_speed = 5
    score = 0
    obstacles = []

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x -= car_speed
                if event.key == pygame.K_RIGHT:
                    x += car_speed

        # Generate new obstacle
        if len(obstacles) < 5:  # Adjust the number of obstacles as needed
            obstacles.append(generate_obstacle())

        # Move obstacles vertically
        for obstacle in obstacles:
            obstacle['y'] += obstacle['speed']

            # Check for collision
            if y < obstacle['y'] + obstacle['height']:
                if x > obstacle['x'] and x < obstacle['x'] + obstacle['width'] or x + car_width > obstacle['x'] and x + car_width < obstacle['x'] + obstacle['width']:
                    game_exit = True

            # Remove obstacles that have gone off screen
            if obstacle['y'] > screen_height:
                obstacles.remove(obstacle)
                score += 1

        # Fill screen with background color
        screen.fill(black)

        # Display lane lines
        for i in range(0, screen_width, 100):  # Adjust spacing between lane lines (100 in this case)
            screen.blit(lane_line_img, (i, 0))

        # Display car
        display_car(x, y)

        # Display obstacles as traffic cones
        for obstacle in obstacles:
            screen.blit(cone_img, (obstacle['x'], obstacle['y']))

        # Display score
        display_score(score)

        # Update the screen
        pygame.display.update()

        # Set the frame rate
        clock.tick(60)

    # Quit Pygame
    pygame.quit()

# Start the game loop
game_loop()
