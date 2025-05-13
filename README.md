## WHO IS CURRENTLY WORKING ON IT?
Giovanni

## Setup

```bash
git clone https://github.com/Amirhossein-2020/statues-game.git
cd statues-game
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## New additions

- Changed YOLO version from YOLO8 to YOLO11-pose, which adds a set of keypoints to every detected person.

- New movement detection, which considers both score and keypoints. Keypoints distance is measured by euclidean distance between current frame and freezed frame, as it's done in the "score" method.

-  Added a short interval at the beginning of the "frozen" phase. This is made for giving people a short time to react to the phase change.

- Added a waiting time of 3 seconds after START button is pressed.

## TODO:

- Player Identifier

- Music and sound effects

- Eliminations to be shown on screen

- End Phase when every player is eliminated





