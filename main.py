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

    tracker = HandTracker()

    fruits = []
    bombs = []

    score = 0

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        frame = tracker.find_hands(frame, draw=False)
        fingertip = tracker.get_landmark(frame)

        # RANDOMLY SPAWN
        if random.random() < 0.05:  # ~5% chance each frame
            fruits.append(Fruit(screen_width, screen_height))

        if random.random() < 0.02:  # ~1% chance each frame (less frequent)
            bombs.append(Bomb(screen_width, screen_height))

        # Move & check fruits
        for fruit in fruits[:]:  # safe iteration while removing
            fruit.move()
            if fruit.is_off_screen():
                fruits.remove(fruit)
            else:
                cv2.circle(
                    frame, fruit.position(), fruit.radius, (0, 255, 0), cv2.FILLED
                )

                if fingertip:
                    distance = math.hypot(
                        fruit.x - fingertip[0], fruit.y - fingertip[1]
                    )
                    if distance < fruit.radius:
                        fruits.remove(fruit)
                        score += 1

        # Move & check bombs
        for bomb in bombs[:]:
            bomb.move()
            if bomb.is_off_screen():
                bombs.remove(bomb)
            else:
                cv2.circle(frame, bomb.position(), bomb.radius, (0, 0, 0), cv2.FILLED)

                if fingertip:
                    distance = math.hypot(bomb.x - fingertip[0], bomb.y - fingertip[1])
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

        # Draw fingertip
        if fingertip:
            cv2.circle(frame, fingertip, 10, (0, 0, 255), cv2.FILLED)

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
