# Balloon Popper – Real-Time Hand-Tracking Game

## Introduction
Balloon Popper is a Python game inspired by Fruit Ninja. Instead of using a mouse or finger on a touchscreen, you control the game with hand gestures captured by your webcam. The project combines MediaPipe's hand-tracking and gesture recognition with the Pygame framework and OpenCV to create a fast-paced, gesture-controlled balloon-popping experience. The game spawns balloons of different types and speeds; you "slice" them by waving your hand through the air while the camera tracks your finger tips.

The original README only provided a one-sentence description, leaving out crucial information such as installation steps and gameplay mechanics. This document aims to fill that gap by explaining how the game works, how to install it and how to play it. It also highlights how the project leverages MediaPipe's hand-tracking pipeline, which infers 21 3D landmarks per hand and can track multiple hands in real time.

## Features
* **Real-time hand tracking and gesture control.** The game uses MediaPipe's high-fidelity hand and finger tracking to detect hand poses from webcam frames. A "peace" sign pauses the game, a thumbs-up resumes it and an open palm (five fingers visible) restarts it.
* **Multiple balloon types with unique effects.** Balloons spawn randomly and come in several varieties:
   * Normal balloons – standard targets worth one point.
   * Golden balloons – reward bonus points when popped.
   * Penalty balloons – reduce your score when hit.
   * Bombs – cause an immediate life loss; avoid them!
   * Dead Eye balloons – trigger a slow-motion "Dead Eye" mode, making it easier to build combos.
   * Heart balloons – add an extra life.
* **Dynamic difficulty scaling.** As your score increases, balloons spawn faster and move more quickly, keeping gameplay challenging. Combo bonuses reward multiple pops in quick succession.
* **High-score persistence.** Your best score is stored in `highscore.txt` so you can compete against yourself.
* **Cross-platform (macOS/Linux).** The game has been tested on macOS and Linux. It should also work on Windows with minor adjustments to the webcam initialization.

## Installation
Follow these steps to set up Balloon Popper on your machine:

1. **Install Python 3.8 or higher.** A recent version of Python is required. You can check your version with `python --version`.
2. **Clone or download this repository.** Download the ZIP archive from GitHub or clone via `git clone`.
3. **Create a virtual environment** (optional but recommended).
```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
4. **Install dependencies.** The `requirements.txt` file lists the necessary packages (e.g. `opencv-python`, `pygame`, `mediapipe`). Run:
```bash
   pip install -r requirements.txt
```
5. **Ensure the gesture model is available.** The repository includes `gesture_recognizer.task`, a pre-trained MediaPipe model used by the `HandTracker` class. Do not delete or rename this file.

## Usage
Once the dependencies are installed:
```bash
python3 main.py
```

The game window will open and initialize your webcam. Position your hands in view of the camera and start slicing balloons. Here are the controls and gameplay mechanics:

| Gesture | Action |
|---------|--------|
| Peace sign (index and middle fingers up) | Pause the game |
| Thumbs up | Resume the game |
| Open palm / High five | Restart when paused or after game over |

### Playing the game
* **Slicing balloons.** Move your index finger through a balloon on the screen. The game tracks up to two hands, drawing a short trail to visualize your slicing motion. Each pop increases your score based on the balloon type.
* **Avoid bombs.** Bombs end a life instantly. When all lives are gone, the game enters a "game over" state. You can restart with an open palm gesture.
* **Build combos.** Popping balloons quickly one after another yields combo bonuses. Slow motion Dead Eye mode helps string together long combos.
* **Keep an eye on lives.** You start with three lives and can earn more by popping heart balloons. Your current score and personal best are displayed at the top of the screen.

### Adjusting settings
The default screen size is 1280×720 pixels. To change the resolution or adjust spawn rates, edit the constants in `main.py` (for example `screen_width`, `screen_height`, `MAX_BALLOONS` and the `weights` list). You can also customize balloon behaviours in `game_objects.py` or tweak gesture thresholds in `hand_tracker.py`.

## Repository Structure
* `main.py` – Runs the game loop. Initializes Pygame, handles webcam capture via OpenCV, manages game state, spawns balloons and processes gesture events.
* `hand_tracker.py` – Wrapper around MediaPipe's hand and gesture recognition. It loads the `gesture_recognizer.task` model, detects hands in each frame and returns gesture names as well as fingertip positions.
* `game_objects.py` – Defines the `Balloon` class with position, movement and balloon type properties.
* `utils.py` – Helper functions (e.g. drawing, audio, additional utilities). You can extend this file to add features like sound effects or UI widgets.
* `gesture_recognizer.task` – Pre-trained MediaPipe model used by the hand tracker.
* `highscore.txt` – Stores your personal best score. If the file does not exist, it will be created automatically.
* `requirements.txt` – List of Python dependencies.

## How It Works
At its core, Balloon Popper continuously captures frames from your webcam, flips them horizontally (like a mirror) and feeds them to the HandTracker. The HandTracker uses MediaPipe to detect hand landmarks and gestures. MediaPipe's pipeline combines a palm detector and a hand landmark model to infer 21 landmark coordinates per hand, allowing robust real-time tracking on commodity hardware. The recognized gesture is mapped to a game command (pause/resume/restart). Meanwhile, balloons are spawned with weighted random selection, move upward and bounce horizontally. Whenever a fingertip trajectory intersects a balloon, the game awards or deducts points based on its type and plays a popping animation. Difficulty increases as your score grows, creating an engaging arcade-style challenge.

## Contributing & Improvements
Pull requests are welcome! Potential enhancements include:
* Adding sound effects and background music.
* Implementing a graphical start menu and pause overlay.
* Including more gestures or custom gesture training using MediaPipe's API.
* Packaging the application with PyInstaller to create standalone executables.

If you find issues or have ideas for new features, feel free to open an issue or submit a PR.

## Acknowledgements
This project relies heavily on MediaPipe for robust hand and finger tracking, which infers 21 landmarks per hand and runs in real time on consumer hardware, and on Pygame for rendering and game logic. Inspiration comes from Fruit Ninja, but the code and assets in this repository are original. Thanks to Google for providing MediaPipe and to the open-source community for maintaining the supporting libraries.
