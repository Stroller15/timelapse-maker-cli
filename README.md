
# Timelapse Maker CLI

**Timelapse Maker** is a Python-based tool to create stunning camera timelapses. It supports desktop PCs, Raspberry Pis, and MacBooks, providing a simple setup process and flexible customization options.

---

## Requirements
- Python >= 3.8  
- Git  
- macOS or Linux (Windows support is experimental)  
- [Homebrew](https://brew.sh/) (for macOS users)

---

## Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Infatoshi/timelapse-maker
cd timelapse-maker
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install Dependencies

#### For Linux
```bash
sudo apt install ffmpeg fswebcam
```

#### For macOS
```bash
pip install opencv-python numpy
brew install ffmpeg
```

#### For Windows
1. Open Command Prompt (`Win + R`, then type `cmd`).  
2. Navigate to the project folder:  
   ```bash
   cd C:\User\Desktop\python-projs\timelapse-maker
   ```
3. Activate the virtual environment and install dependencies:  
   ```bash
   .venv\Scripts\activate.bat
   pip install opencv-python
   ```

---

## Usage

### Capture a Timelapse
Run the following command to capture frames for the timelapse:
```bash
python capture_timelapse.py --hours 12 --interval 15
```
- `--hours`: Duration of the timelapse capture.  
- `--interval`: Time (in seconds) between each frame. A shorter interval makes the timelapse smoother.

### Create the Timelapse Video
After capturing frames, convert them into a video:
```bash
python create_timelapse.py
```
- **Note**: This script uses a custom FFmpeg command and is supported on macOS and Linux.

### Configure the Camera
If you have multiple cameras (including virtual ones), adjust the camera index in the script:
- Default: `device=0`  
- Increment the value (e.g., `device=1`, `device=2`, etc.) until the correct camera is used.  

Captured frames are stored in the `timelapse_images` directory for review.

---

## Using `add_clock.py`
- This script overlays a clock on your timelapse frames.
- Requires `opencv-python`. Install it manually:
  ```bash
  pip install opencv-python
  ```
- **Note**: Installation on Raspberry Pi might throw errors. This dependency is excluded from the default setup to ensure smooth installation.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

Feel free to suggest further improvements or report issues! 🚀
