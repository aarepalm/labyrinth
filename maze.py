import pygame
import sys
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
import random

# Initialize pygame
pygame.init()

# Constants
TILE_SIZE = 20  # Set smaller tile size for larger mazes
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont('Arial', 24)

# Function to draw the maze
def draw_maze(screen, maze, goal_pos):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            color = WHITE if maze[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    # Draw the goal position marked with 'F'
    goal_text = font.render('F', True, BLUE)
    screen.blit(goal_text, (goal_pos[0] * TILE_SIZE + TILE_SIZE // 4, goal_pos[1] * TILE_SIZE + TILE_SIZE // 6))

# Function to draw the player
def draw_player(screen, player_pos):
    pygame.draw.rect(screen, RED, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Generate a maze with walls 1 tile thick and corridors 1 tile wide
def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]

    # Create a maze using the Depth-First Search (DFS) algorithm
    def carve_passages(x, y):
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 1 <= nx < width-1 and 1 <= ny < height-1 and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy // 2][x + dx // 2] = 0
                carve_passages(nx, ny)

    # Start carving passages from the top-left corner
    maze[1][1] = 0
    carve_passages(1, 1)

    # Set the goal position to be the bottom-right corner
    maze[height-3][width-3] = 0
    return maze

# Function to show the time in a popup window
def show_popup(time_taken):
    pygame.display.quit()
    pygame.quit()
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Congratulations!", f"You've reached the goal!\nTime taken: {time_taken:.2f} seconds")
    root.destroy()
    sys.exit()

# Function to get maze dimensions using tkinter input
def get_maze_size():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    width = simpledialog.askinteger("Maze Width", "Enter maze width (number of tiles):", minvalue=5, maxvalue=30)
    height = simpledialog.askinteger("Maze Height", "Enter maze height (number of tiles):", minvalue=5, maxvalue=30)
    root.destroy()
    return width, height

# Main game loop
def main():
    # Get maze size from user input
    width, height = get_maze_size()
    if not width or not height:
        print("Invalid maze size. Exiting the game.")
        sys.exit()

    # Generate the maze
    maze = generate_maze(width, height)

    # Character and goal positions
    player_pos = [1, 1]
    goal_pos = [width - 3, height - 3]

    # Resize screen based on maze size
    screen_width = width * TILE_SIZE
    screen_height = height * TILE_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Game")

    clock = pygame.time.Clock()
    start_time = time.time()  # Start the timer
    running = True

    while running:
        screen.fill(BLACK)
        draw_maze(screen, maze, goal_pos)
        draw_player(screen, player_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Move the player based on arrow keys
                if event.key == pygame.K_UP and maze[player_pos[1] - 1][player_pos[0]] == 0:
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and maze[player_pos[1] + 1][player_pos[0]] == 0:
                    player_pos[1] += 1
                elif event.key == pygame.K_LEFT and maze[player_pos[1]][player_pos[0] - 1] == 0:
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and maze[player_pos[1]][player_pos[0] + 1] == 0:
                    player_pos[0] += 1

        # Check if player has reached the goal
        if player_pos == goal_pos:
            end_time = time.time()  # End the timer
            time_taken = end_time - start_time
            show_popup(time_taken)
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

