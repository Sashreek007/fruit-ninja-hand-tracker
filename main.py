import cv2
import math
import random
from hand_tracker import HandTracker
from game_objects import Fruit, Bomb


def main():
    cap = cv2.VideoCapture(0)

    # Set to desired resolution
    screen_width = 1280
    screen_height = 720
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

    MAX_HANDS = 2
    tracker = HandTracker(max_num_hands=MAX_HANDS)

    fruits = []
    bombs = []

    score = 0
    fruits_to_remove = []

    # for the slice effect
    trails = []
    MAX_TRAIL_LENGTH = 5
    colors = [(255, 0, 0), (0, 255, 255)]

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        frame = tracker.find_hands(frame, draw=False)
        fingertips = tracker.get_landmarks(frame)

        while len(trails) < min(len(fingertips), MAX_HANDS):
            trails.append([])
        for i in range(len(fingertips), len(trails)):
            trails[i].clear()
        # Update trails for each fingertip
        for i, fingertip in enumerate(fingertips[:MAX_HANDS]):
            trails[i].append(fingertip)
            if len(trails[i]) > MAX_TRAIL_LENGTH:
                trails[i].pop(0)
            # Draw fingertip
            cv2.circle(frame, fingertip, 10, (0, 0, 255), cv2.FILLED)

        # Draw all trails with correct colors

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
                cv2.line(frame, pt1, pt2, color, thickness=2)
        # RANDOMLY SPAWN
        if random.random() < 0.05 and len(fruits) < 5:
            fruits.append(Fruit(screen_width, screen_height))
        if random.random() < 0.02 and len(bombs) < 2:
            bombs.append(Bomb(screen_width, screen_height))

        # Move & check fruits
        for fruit in fruits:
            fruit.move()
            if fruit.is_off_screen():
                fruits_to_remove.append(fruit)
            else:
                cv2.circle(
                    frame, fruit.position(), fruit.radius, (0, 255, 0), cv2.FILLED
                )
                for trail in trails[:MAX_HANDS]:
                    for point in trail:
                        distance = math.hypot(fruit.x - point[0], fruit.y - point[1])
                        if distance < fruit.radius:
                            fruits_to_remove.append(fruit)
                            score += 1
                            break
                    else:
                        continue
                    break  # exit both loops once hit

        # ✅ Remove all marked fruits safely AFTER checking everything
        for fruit in fruits_to_remove:
            if fruit in fruits:
                fruits.remove(fruit)

        # Move & check bombs
        for bomb in bombs[:]:
            bomb.move()
            if bomb.is_off_screen():
                bombs.remove(bomb)
            else:
                cv2.circle(frame, bomb.position(), bomb.radius, (0, 0, 0), cv2.FILLED)
                for trail in trails[:MAX_HANDS]:
                    for point in trail:
                        distance = math.hypot(bomb.x - point[0], bomb.y - point[1])
                        if distance < bomb.radius:
                            cv2.putText(
                                frame,
                                "GAME OVER!",
                                (400, 400),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                2,
                                (0, 0, 255),
                                4,
                            )
                            cv2.imshow("Fruit Ninja - Game Over", frame)
                            cv2.waitKey(2000)
                            cap.release()
                            cv2.destroyAllWindows()
                            return

        # ✅ No need to draw fingertip again here — handled above

        # Draw score
        cv2.putText(
            frame,
            f"Score: {score}",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )

        cv2.imshow("Fruit Ninja - Random Spawn", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
