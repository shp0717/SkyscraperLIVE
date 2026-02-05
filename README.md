# SkyScraper LIVE

A simulation of Alex Honnold's climb of Taipei 101, inspired by the Netflix live event ["Skyscraper LIVE"](https://www.netflix.com/title/81987107).

## How to Run

### Python Script Edition
1. Ensure you have Python installed on your system, and download the SkyscraperLIVE project files.
2. Install the required libraries using pip:
   ```bash
   pip install pygame pillow
   ```
3. Install FFPMEG:
   1. ```bash
      brew install ffmpeg
      ```
   2. [FFMPEG Download Page](https://ffmpeg.org/download.html)
4. Navigate to the SkyscraperLIVE directory:
   ```bash
   cd SkyscraperLIVE
   ```
5. Run the main script:
   ```bash
   python main.py
   ```
6. Enjoy the simulation!

## Controls

- **`Left/Right Arrow Keys`**: Move left / right
- **`Mouse Left/Right Click`**: Move left / right (on mouse control mode)
- **`Ctrl`**: Slow movement
- **`Shift`**: More slow movement
- **`Home`**: Reset zoom to default
- **`+/-`**: Zoom in / out
- **`Down Arrow Key`**: Hold the building (reduce sway)
- **`Space / Up Arrow Key`**: Jump / Climb the building
- **`Ctrl + M`**: Toggle mouse control mode

## Objective
Climb to the top of Taipei 101 while managing your physical strength and dealing with wind interference. Reach the top to complete the simulation!

## Credits
- Developed by Dylan Chang
- Inspired by Alex Honnold's climb and the Netflix event "Skyscraper LIVE"
- Uses Pygame for graphics and input handling
- Building model based on Taipei 101 structure
- Wind interference modeled for added challenge

Enjoy climbing!

## Version Naming
Now version: [Click here](version.txt)
(Version names follow the format: Alpha/Beta/Release + A.B.C.D)
- A: `0` (Alpha, Beta)
     `1` (Release)
- B: Year
- C: nth day of the year
- D: Revision number of the day

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Inspiration
This simulation is inspired by Alex Honnold's incredible free solo climb of Taipei 101, as featured in the Netflix live event "Skyscraper LIVE". The goal is to provide an engaging experience that captures the thrill and challenge of such a feat.
### [Skyscraper LIVE on Netflix](https://www.netflix.com/title/81987107)
If you climb to the top, you can take a screenshot of your achievement saved as `honnold_selfie.png` in the project directory, which is inspired by Alex Honnold's real-life selfie at the summit!  
> The game will automatically record the live video and save it as "skyscraper-live.mp4" in the project directory.
