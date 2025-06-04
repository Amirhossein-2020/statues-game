## Setup

```bash
git clone https://github.com/Amirhossein-2020/statues-game.git
cd statues-game
pipenv install -r requirements.txt
pipenv shell
=======
```

## Pensieri a caso:

- Fare il check all'inizio del gioco quando tutti i giocatori sono in posizione, rifare il check solo quando il numero dei giocatori diventa diverso dal numero che sono all'inizio.
- Cambiare yolo face con haar cascade (molto più leggero)

## Baba Jaga game
It is a real-time computer vision game inspired by "Red Light, Green Light". Players move during the "green light" (moving phase) and must freeze during the "red light" (frozen phase). If a player moves during the frozen state, they are eliminated. The game uses webcam input, pose detection, and face recognition to track players and enforce rules.

### Screenshot of gameplay(:))

### Tech Stack:

- OpenCV | 4.11.0.86  
Used for capturing video frames, image preprocessing, visual annotations, and fullscreen rendering.

- YOLOv11-pose | 8.3.126  
Performs keypoint detection to track player movement across frames. Used to determine if a player moved during the frozen phase.

- YOLOv11-face | 8.3.126  
Detects and extracts player faces from webcam frames to be passed into the recognition pipeline.

- DeepFace | 0.0.93  
Performs face recognition. Identifies players and assigns persistent IDs across game sessions.

- pygame (planned)  
To be used for music and sound effect playback during game events (start, freeze, elimination, etc).


### Additional features
- music and visual effects
- player database is auto-updated with new faces
- unrecognized players are saved and assigned temporary IDs
- game window runs in fullscreen mode.
