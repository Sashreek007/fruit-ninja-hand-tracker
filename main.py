import cv2
import random
import math
from hand_tracker import HandTracker


def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()

    # Fruit properties
    fruit_pos = [random.randint(100, 500), 0]
    fruit_radius = 30
    fruit_speed = 5

    # Bomb properties
    bomb_pos = [random.randint(100, 500), 0]
    bomb_radius = 30
    bomb_speed = 5

    # Score
    score = 0

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        frame = tracker.find_hands(frame, draw=False)

        fingertip = tracker.get_landmark(frame)
        if fingertip:
            cv2.circle(frame, fingertip, 10, (0, 0, 255), cv2.FILLED)

            # Check fruit collision
            distance = math.hypot(
                fruit_pos[0] - fingertip[0], fruit_pos[1] - fingertip[1]
            )
            if distance < fruit_radius:
                fruit_pos = [random.randint(100, 500), 0]
                score += 1

            # Check bomb collision
            bomb_distance = math.hypot(
                bomb_pos[0] - fingertip[0], bomb_pos[1] - fingertip[1]
            )
            if bomb_distance < bomb_radius:
                cv2.putText(
                    frame,
                    "GAME OVER!",
                    (200, 300),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 0, 255),
                    4,
                )
                cv2.imshow("Fruit Ninja - Game Over", frame)
                cv2.waitKey(2000)
                break

        # Move fruit
        fruit_pos[1] += fruit_speed
        if fruit_pos[1] > frame.shape[0]:
            fruit_pos = [random.randint(100, 500), 0]

        # Move bomb
        bomb_pos[1] += bomb_speed
        if bomb_pos[1] > frame.shape[0]:
            bomb_pos = [random.randint(100, 500), 0]

        # Draw fruit
        cv2.circle(frame, tuple(fruit_pos), fruit_radius, (0, 255, 0), cv2.FILLED)

        # Draw bomb (black circle)
        cv2.circle(frame, tuple(bomb_pos), bomb_radius, (0, 0, 0), cv2.FILLED)

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

        cv2.imshow("Fruit Ninja - Bombs!", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
