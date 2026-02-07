# _*_ coding: utf-8 _*_
"""
Gaze Cursor Display Script
Displays a red transparent circle at the gaze position in a fullscreen window.
Press ESC to exit.
"""

import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT

from gazefollower import GazeFollower
from screeninfo import get_monitors

# Initialize pygame
pygame.init()

# Get screen size
monitors = get_monitors()
screen_width = monitors[0].width
screen_height = monitors[0].height

# Create fullscreen window
win = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Gaze Cursor")
pygame.mouse.set_visible(False)  # Hide mouse cursor

# Initialize GazeFollower
print("Initializing GazeFollower...")
gf = GazeFollower()

# Preview camera (optional - allows you to see yourself)
print("Starting camera preview. Close the preview window when ready.")
gf.preview(win=win)

# Calibrate the gaze tracker
print("Starting calibration. Please follow the calibration points.")
gf.calibrate(win=win)

# Start sampling gaze data
print("Starting gaze tracking. Press ESC to exit.")
gf.start_sampling()
pygame.time.wait(100)  # Wait for tracker to cache some samples

# Main loop
clock = pygame.time.Clock()
running = True
gaze_x, gaze_y = screen_width // 2, screen_height // 2  # Default to center

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    
    # Get current gaze position
    gaze_info = gf.get_gaze_info()
    if gaze_info and gaze_info.status:
        gaze_x = int(gaze_info.filtered_gaze_coordinates[0])
        gaze_y = int(gaze_info.filtered_gaze_coordinates[1])
        # Clamp to screen bounds
        gaze_x = max(0, min(screen_width, gaze_x))
        gaze_y = max(0, min(screen_height, gaze_y))
    
    # Clear screen with black background
    win.fill((0, 0, 0))
    
    # Draw red transparent circle at gaze position
    # Create a surface for the circle
    circle_surface = pygame.Surface((100, 100))
    circle_surface.fill((0, 0, 0))  # Fill with black
    circle_surface.set_colorkey((0, 0, 0))  # Make black transparent
    # Draw filled circle (red)
    pygame.draw.circle(circle_surface, (255, 0, 0), (50, 50), 50)
    # Set transparency (0 = fully transparent, 255 = fully opaque)
    # 180 = about 70% opaque (semi-transparent)
    circle_surface.set_alpha(180)
    # Blit the transparent circle onto the main window
    win.blit(circle_surface, (gaze_x - 50, gaze_y - 50))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

# Cleanup
print("Stopping gaze tracking...")
pygame.time.wait(100)  # Wait to capture ending samples
gf.stop_sampling()

# Save the gaze data (optional)
try:
    import os
    data_dir = "./data"
    os.makedirs(data_dir, exist_ok=True)
    file_name = "gaze_cursor_session.csv"
    gf.save_data(os.path.join(data_dir, file_name))
    print(f"Gaze data saved to {os.path.join(data_dir, file_name)}")
except Exception as e:
    print(f"Could not save gaze data: {e}")

# Release resources
gf.release()
pygame.quit()
print("Exiting...")

