import cv2
import math
import random
import pygame
import sys
import time
import os
import platform
from hand_tracker import HandTracker
from game_objects import Balloon

# --------------------------
# Pygame setup
# --------------------------
pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Balloon Popper 🎈 - Heart + Auto Life FIX")
clock = pygame.time.Clock()

# --------------------------
# HandTracker & webcam
# --------------------------
model_path = os.path.join(os.getcwd(), "gesture_recognizer.task")

if platform.system() == "Windows":
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
else:
    cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

tracker = HandTracker(model_path)

# --------------------------
# High Score system
# --------------------------
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        content = f.read().strip()
        personal_best = int(content) if content else 0
else:
    personal_best = 0

# --------------------------
# Game state
# --------------------------
balloons = []
score = 0
lives = 3
paused = False
game_over = False

bonus_life_threshold = 0  # ✅ NEW: track auto-life milestones

hit_times = []
trails = []
MAX_TRAIL_LENGTH = 5
MAX_HANDS = 2
colors = [(255, 0, 0), (0, 255, 255)]

pause_counter = 0
resume_counter = 0
restart_timer = 0.0
PAUSE_FRAMES = 1
RESUME_FRAMES = 10
RESTART_SECONDS = 3.0

dead_eye_active = False
dead_eye_timer = 0.0

frame_count = 0
MAX_BALLOONS = 8

running = True
while running:
    dt = clock.tick(30) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_count += 1

    tracker.find_hands(frame)
    if frame_count % 3 == 0:
        tracker.find_gesture(frame)

    fingertips = tracker.get_handed_fingertips()
    gesture = tracker.get_gesture()

    if gesture == "Victory":
        pause_counter += 1
        resume_counter = 0
        restart_timer = 0
    elif gesture == "Thumb_Up":
        resume_counter += 1
        pause_counter = 0
        restart_timer = 0
    elif gesture == "Open_Palm":
        if paused or game_over:
            restart_timer += dt
        else:
            restart_timer = 0
        pause_counter = 0
        resume_counter = 0
    else:
        pause_counter = 0
        resume_counter = 0
        restart_timer = 0

    if pause_counter >= PAUSE_FRAMES and not game_over:
        paused = True
    if resume_counter >= RESUME_FRAMES and not game_over:
        paused = False

    if restart_timer >= RESTART_SECONDS and (paused or game_over):
        if score > personal_best:
            personal_best = score
            with open("highscore.txt", "w") as f:
                f.write(str(personal_best))
        paused = False
        game_over = False
        balloons.clear()
        score = 0
        lives = 3
        bonus_life_threshold = 0  # ✅ Reset tracker!
        hit_times.clear()
        trails = [[] for _ in trails]
        pause_counter = 0
        resume_counter = 0
        restart_timer = 0
        dead_eye_active = False
        dead_eye_timer = 0.0
        print("✅ Game restarted!")

    while len(trails) < MAX_HANDS:
        trails.append([])

    for i in range(MAX_HANDS):
        if fingertips[i]:
            trails[i].append(fingertips[i])
            if len(trails[i]) > MAX_TRAIL_LENGTH:
                trails[i].pop(0)
        else:
            trails[i].clear()

    spawn_rate = 0.05 + min(score * 0.0005, 0.03)
    speed_multiplier = 1.0 + min(score * 0.0025, 0.5)

    weights = [
        56,  # normal
        10,  # golden
        20 + min(score // 10, 10),  # penalty
        10 + min(score // 20, 10),  # bomb
        4,  # dead_eye
        1,  # heart
    ]
    total = sum(weights)
    r = random.uniform(0, total)

    if random.random() < spawn_rate and len(balloons) < MAX_BALLOONS:
        if r < weights[0]:
            balloons.append(Balloon(screen_width, screen_height, "normal"))
        elif r < weights[0] + weights[1]:
            balloons.append(Balloon(screen_width, screen_height, "golden"))
        elif r < weights[0] + weights[1] + weights[2]:
            balloons.append(Balloon(screen_width, screen_height, "penalty"))
        elif r < weights[0] + weights[1] + weights[2] + weights[3]:
            bomb = Balloon(screen_width, screen_height, "bomb")
            bomb.speed *= 1.2
            balloons.append(bomb)
        elif r < weights[0] + weights[1] + weights[2] + weights[3] + weights[4]:
            balloons.append(Balloon(screen_width, screen_height, "dead_eye"))
        else:
            balloons.append(Balloon(screen_width, screen_height, "heart"))

    if not paused and not game_over:
        to_remove = []
        for balloon in balloons:
            if not dead_eye_active:
                balloon.move(speed_multiplier, score)
            if balloon.is_off_screen():
                to_remove.append(balloon)
                if balloon.type not in ["bomb", "dead_eye", "penalty", "heart"]:
                    lives -= 1
                    if lives <= 0:
                        lives = 0
                        game_over = True
                        restart_timer = 0
            else:
                for trail in trails:
                    for point in trail:
                        if (
                            math.hypot(balloon.x - point[0], balloon.y - point[1])
                            < balloon.radius
                        ):
                            to_remove.append(balloon)
                            if balloon.type == "normal":
                                score += 1
                            elif balloon.type == "golden":
                                score += 5
                            elif balloon.type == "penalty":
                                score -= 3
                                if score < 0:
                                    score = 0
                                if score == 0:
                                    game_over = True
                                    restart_timer = 0
                            elif balloon.type == "bomb":
                                game_over = True
                                restart_timer = 0
                            elif balloon.type == "dead_eye":
                                dead_eye_active = True
                                dead_eye_timer = 5.0
                            elif balloon.type == "heart":
                                lives += 1
                            hit_times.append(time.time())
                            break
                    else:
                        continue
                    break
        for b in to_remove:
            if b in balloons:
                balloons.remove(b)

    # ✅ Auto +1 life every 75 score milestone
    if score >= (bonus_life_threshold + 1) * 75:
        lives += 1
        bonus_life_threshold += 1

    hit_times = [t for t in hit_times if time.time() - t < 0.5]
    if len(hit_times) >= 3:
        score += 2
        hit_times.clear()

    if dead_eye_active:
        dead_eye_timer -= dt
        if dead_eye_timer <= 0:
            dead_eye_active = False

    screen.fill((255, 140, 0) if dead_eye_active else (135, 206, 235))

    for balloon in balloons:
        if balloon.type == "normal":
            color = (0, 255, 0)
        elif balloon.type == "golden":
            color = (255, 215, 0)
        elif balloon.type == "penalty":
            color = (128, 0, 128)
        elif balloon.type == "bomb":
            color = (0, 0, 0)
        elif balloon.type == "dead_eye":
            color = (255, 69, 0)
        elif balloon.type == "heart":
            color = (255, 20, 147)
        else:
            color = (255, 255, 255)
        pygame.draw.circle(screen, color, balloon.position(), balloon.radius)

    for i, trail in enumerate(trails):
        for j in range(1, len(trail)):
            pt1, pt2 = trail[j - 1], trail[j]
            alpha = 1.0 - (j / len(trail))
            color = colors[i % len(colors)]
            color = (
                int(color[0] * alpha),
                int(color[1] * alpha),
                int(color[2] * alpha),
            )
            pygame.draw.line(screen, color, pt1, pt2, 3)
    for i, trail in enumerate(trails):
        if trail:
            pygame.draw.circle(screen, colors[i % len(colors)], trail[-1], 10)

    font = pygame.font.SysFont(None, 50)
    score_text = font.render(
        f"Score: {score} | Lives: {lives} | Best: {personal_best}",
        True,
        (255, 255, 255),
    )
    screen.blit(score_text, (10, 10))

    font_big = pygame.font.SysFont(None, 80)
    restart_seconds_left = max(0, int(RESTART_SECONDS - restart_timer) + 1)

    if paused:
        pause_text = font_big.render(
            "PAUSED - Hold Open Palm to Restart", True, (255, 255, 0)
        )
        screen.blit(pause_text, (screen_width // 2 - 350, screen_height // 2 - 80))
        if restart_timer > 0:
            timer_text = font_big.render(
                f"Restarting in: {restart_seconds_left}", True, (255, 255, 0)
            )
            screen.blit(timer_text, (screen_width // 2 - 100, screen_height // 2))

    if game_over:
        over_text = font_big.render(
            "GAME OVER - Hold Open Palm to Restart", True, (255, 0, 0)
        )
        screen.blit(over_text, (screen_width // 2 - 400, screen_height // 2 - 80))
        if restart_timer > 0:
            timer_text = font_big.render(
                f"Restarting in: {restart_seconds_left}", True, (255, 0, 0)
            )
            screen.blit(timer_text, (screen_width // 2 - 100, screen_height // 2))

    if dead_eye_active:
        dead_eye_overlay = font_big.render(
            f"DEAD EYE: {int(dead_eye_timer) + 1}", True, (0, 0, 0)
        )
        screen.blit(dead_eye_overlay, (screen_width // 2 - 150, 50))

    pygame.display.flip()

if score > personal_best:
    with open("highscore.txt", "w") as f:
        f.write(str(score))

cap.release()
pygame.quit()
sys.exit()
