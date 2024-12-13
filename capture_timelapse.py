import argparse
from dataclasses import dataclass
from pathlib import Path
import platform
import time
import subprocess
import sys


@dataclass
class Resolution:
    width: int
    height: int


def capture_timelapse_opencv(
    duration: float,
    interval: int,
    output_dir: Path,
    device: int = 1,
    resolution: Resolution = None,
):
    try:
        import cv2
    except ImportError:
        print("OpenCV (cv2) is not installed. Please install it with 'pip install opencv-python'")
        sys.exit(1)

    # Initialize camera
    cap = cv2.VideoCapture(device)

    if not cap.isOpened():
        print(f"Error: Could not open camera {device}")
        sys.exit(1)

    # Set resolution if specified
    if resolution:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution.height)

    # Get actual camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Camera resolution: {width}x{height}")

    num_frames = int(duration // interval)
    start_time = time.time()

    try:
        for i in range(1, num_frames + 1):
            ret, frame = cap.read()

            if not ret:
                print(f"Error capturing frame {i}")
                continue

            filename = output_dir / f"frame_{i:04d}.jpg"

            try:
                cv2.imwrite(str(filename), frame)
                print(f"Captured frame {i}/{num_frames}")
            except Exception as e:
                print(f"Error saving frame {i}: {e}")

            # Adjust sleep to account for capture and processing time
            elapsed = time.time() - start_time
            expected_time = (i * interval)
            
            if elapsed < expected_time:
                time.sleep(max(0, expected_time - elapsed))

    except KeyboardInterrupt:
        print("\nCapture interrupted by user")
    finally:
        # Release the camera
        cap.release()
        print("Timelapse capture completed.")


def capture_timelapse_linux(
    duration: float,
    interval: int,
    output_dir: Path,
    resolution: Resolution = None,
    device: int = 0,
):
    num_frames = int(duration // interval)
    start_time = time.time()

    for i in range(1, num_frames + 1):
        filename = f"{output_dir}/frame_{i:04d}.jpg"

        # Capture the image using fswebcam
        try:
            result = subprocess.run(
                ["fswebcam", "-r", "1920x1080", "--no-banner", filename], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode != 0:
                print(f"Error capturing frame {i}: {result.stderr}")
                continue

            print(f"Captured frame {i}/{num_frames}")

        except FileNotFoundError:
            print("fswebcam not found. Please install it with 'sudo apt-get install fswebcam'")
            sys.exit(1)

        # Adjust sleep to account for capture time
        elapsed = time.time() - start_time
        expected_time = (i * interval)
        
        if elapsed < expected_time:
            time.sleep(max(0, expected_time - elapsed))

    print("Timelapse capture completed.")


def main():
    parser = argparse.ArgumentParser(
        description="Capture timelapse images using OpenCV or fswebcam."
    )
    parser.add_argument(
        "--hours",
        "-H",
        type=float,
        required=True,
        help="Duration of timelapse in hours",
    )
    parser.add_argument(
        "--interval",
        "-i",
        type=int,
        required=True,
        help="Interval between frames in seconds",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="timelapse_images",
        help="Where to save the frames",
    )
    parser.add_argument("--width", type=int, help="Custom width for capture")
    parser.add_argument("--height", type=int, help="Custom height for capture")
    parser.add_argument("--device", type=int, default=0, help="Camera device number")

    args = parser.parse_args()

    duration = 3600 * args.hours  # Total duration in seconds

    resolution = None
    if args.width and args.height:
        resolution = Resolution(args.width, args.height)

    mapping = {
        "Linux": capture_timelapse_linux,
        "Darwin": capture_timelapse_opencv,
        "Windows": capture_timelapse_opencv,
    }

    os_type = platform.system()
    try:
        capture_timelapse = mapping[os_type]
    except KeyError:
        parser.error(f"Unsupported OS: {os_type}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    capture_timelapse(
        duration=duration,
        interval=args.interval,
        output_dir=output_dir,
        resolution=resolution,
        device=args.device,
    )


if __name__ == "__main__":
    main()