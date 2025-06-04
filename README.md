## Setup

```bash
git clone https://github.com/Amirhossein-2020/statues-game.git
cd statues-game
pipenv install -r requirements.txt
pipenv shell
=======
```

## REQUIRED python 3.10!

## Baba Jaga game
It is a real-time computer vision game inspired by "Red Light, Green Light". Players move during the "green light" (moving phase) and must freeze during the "red light" (frozen phase). If a player moves during the frozen state, they are eliminated. The game uses webcam input, pose detection, and face recognition to track players and identify them.

To run the game, just type

```bash
python main.py 
```

on command-line, being sure to be on the right folder

### Main Tech Stack:

- OpenCV 
Used for capturing video frames, image preprocessing, visual annotations, and fullscreen rendering.

- YOLOv11-pose   
Performs keypoint detection to track player movement across frames. Used to determine if a player moved during the frozen phase.

- YOLOv11-face   
Detects and extracts player faces from webcam frames to be passed into the recognition pipeline.

- DeepFace   
Performs face recognition. Identifies players and assigns persistent IDs across game sessions.

- pygame 
To be used for music and sound effect playback during game events (start, freeze, elimination, etc).

### Folders

#### lib

Containing all the classes we use

#### example

Some old tests with threads, not part of the game

#### database

Speaks for itself
