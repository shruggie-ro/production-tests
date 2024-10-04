import pygame
import random
import time

import signal

pygame.init()

infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
fullscreen = True


initial_image = pygame.image.load("logo.png")
initial_image_width, initial_image_height = initial_image.get_size()


scale_factor = height / initial_image_height  
new_initial_width = int(initial_image_width * scale_factor)
new_initial_height = height  
scaled_initial_image = pygame.transform.scale(initial_image, (new_initial_width, new_initial_height))


images = [pygame.image.load(f"image{i}.jpeg") for i in range(1, 10)]


scaled_images = []
for image in images:
    image_width, image_height = image.get_size()
    scale_factor = height / image_height  
    new_width = int(image_width * scale_factor)
    new_height = height  
    scaled_image = pygame.transform.scale(image, (new_width, new_height))
    scaled_images.append(scaled_image)

def fade_in_image(image, duration=0.3):
    """Fade in the image with a smooth transition."""
    faded_image = image.convert_alpha()

    steps = 10
    for step in range(steps + 1):
        alpha = int(255 * (step / steps))  # Calculate alpha value based on step
        faded_image.set_alpha(alpha)
        display_image(faded_image, height // 2)

def display_image(scaled_image, y_offset):
    """Display the given scaled image and position it with a vertical offset."""
    screen.fill((0, 0, 0))  # Clear the screen with a black background

    width, height = screen.get_size()
    
    rect = scaled_image.get_rect(center=(width // 2, y_offset))

    screen.blit(scaled_image, rect)
    pygame.display.flip()  

def scroll_images():
    start_time = time.time()
    images_order = random.sample(scaled_images, len(scaled_images))  
    y_position = height/2 
    current_image_index = 0
    scroll_duration = 5  
    scroll_speed = height 
    final_image = None

    while time.time() - start_time < scroll_duration:
        current_image = images_order[current_image_index]
        
        
        display_image(current_image, y_position)
        time.sleep(0.03)

        
        elapsed_time = time.time() - start_time
        if elapsed_time >= scroll_duration:
            break

        current_image_index = (current_image_index + 1) % len(images_order)  

        final_image = current_image

    display_image(final_image, height // 2)
    return final_image

running = True
scrolling_started = False

def SigHandler(SIG, FRM):
    global running, scrolling_started

    if (SIG == signal.SIGTERM):
        running = False
    if (SIG == signal.SIGUSR1):
        scrolling_started = True

def main():
    global screen, width, height, fullscreen, running, scrolling_started

    print("Press Enter to start scrolling, ESC to toggle fullscreen.")

    fade_in_image(scaled_initial_image, duration=1)

    signal.signal(signal.SIGTERM, SigHandler)
    signal.signal(signal.SIGUSR1, SigHandler)

    while running:
        if (not scrolling_started):
            time.sleep(0.1)
            continue

        scrolling_started = False

        final_image = scroll_images()
        display_image(final_image, height // 2)

        time.sleep(0.1)

    pygame.quit()

if __name__ == "__main__":
    main()
