import cv2
import math
import random
import pygame
import sys
from hand_tracker import HandTracker

# Initialize Pygame
pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fruit Ninja - Pygame Version")
clock = pygame.time.Clock()

# Initialize HandTracker & webcam
MAX_HANDS = 2
tracker = HandTracker(max_num_hands=MAX_HANDS)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

# Fruits & bombs
from game_objects import Fruit, Bomb  # keep your classes

fruits = []
bombs = []
score = 0

# Trails
trails = []
MAX_TRAIL_LENGTH = 5
colors = [(255, 0, 0), (0, 255, 255)]

running = True
while running:
    # Pygame event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Webcam + MediaPipe
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    tracker.find_hands(frame, draw=False)
    fingertips = tracker.get_landmarks(frame)

    # Keep trails list in sync
    while len(trails) < min(len(fingertips), MAX_HANDS):
        trails.append([])
    for i in range(len(fingertips), len(trails)):
        trails[i].clear()

    # Update trails
    for i, fingertip in enumerate(fingertips[:MAX_HANDS]):
        trails[i].append(fingertip)
        if len(trails[i]) > MAX_TRAIL_LENGTH:
            trails[i].pop(0)

    # Randomly spawn
    if random.random() < 0.05 and len(fruits) < 5:
        fruits.append(Fruit(screen_width, screen_height))
    if random.random() < 0.02 and len(bombs) < 2:
        bombs.append(Bomb(screen_width, screen_height))

    # Pygame background
    screen.fill((135, 206, 235))

    # Draw trails
    for i, trail in enumerate(trails[:MAX_HANDS]):
        for j in range(1, len(trail)):
            pt1 = trail[j - 1]
            pt2 = trail[j]
            alpha = 1.0 - (j / len(trail))
            color = (
                int(colors[i][0] * alpha),
                int(colors[i][1] * alpha),
                int(colors[i][2] * alpha),
            )
            pygame.draw.line(screen, color, pt1, pt2, 3)
    for i, trail in enumerate(trails[:MAX_HANDS]):
        if trail:
            pygame.draw.circle(screen, (255, 0, 0), trail[-1], 10)
    # Fruits logic
    fruits_to_remove = []
    for fruit in fruits:
        fruit.move()
        if fruit.is_off_screen():
            fruits_to_remove.append(fruit)
        else:
            # TEMP: Draw circle. Later: screen.blit(fruit.image, pos)
            pygame.draw.circle(screen, (0, 255, 0), fruit.position(), fruit.radius)

            for trail in trails[:MAX_HANDS]:
                for point in trail:
                    distance = math.hypot(fruit.x - point[0], fruit.y - point[1])
                    if distance < fruit.radius:
                        fruits_to_remove.append(fruit)
                        score += 1
                        break
                else:
                    continue
                break

    for fruit in fruits_to_remove:
        if fruit in fruits:
            fruits.remove(fruit)

    # Bombs logic
    for bomb in bombs[:]:
        bomb.move()
        if bomb.is_off_screen():
            bombs.remove(bomb)
        else:
            # TEMP: Draw circle. Later: screen.blit(bomb.image, pos)
            pygame.draw.circle(screen, (0, 0, 0), bomb.position(), bomb.radius)

            for trail in trails[:MAX_HANDS]:
                for point in trail:
                    distance = math.hypot(bomb.x - point[0], bomb.y - point[1])
                    if distance < bomb.radius:
                        font = pygame.font.SysFont(None, 80)
                        text = font.render("GAME OVER!", True, (255, 0, 0))
                        screen.blit(text, (400, 300))
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        cap.release()
                        pygame.quit()
                        sys.exit()

    # Draw score
    font = pygame.font.SysFont(None, 50)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

cap.release()
pygame.quit()
sys.exit()
