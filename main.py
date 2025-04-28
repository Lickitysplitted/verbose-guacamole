import logging
import sys
from pathlib import Path
import json

from utils import setup_logging, get_video_files, check_ffmpeg
from detection import detect_black_bars
from report import generate_report


def main():
    """Main function to run the detection script."""
    config = json.load(open('config.json'))

    setup_logging(config)
    logger = logging.getLogger(__name__)

    if not check_ffmpeg():
        logger.error("ffmpeg is not installed or not in PATH.")
        sys.exit(1)

    input_path = Path(config.get("input_path", "input"))
    video_files = get_video_files(input_path)

    results = []
    for video in video_files:
        try:
            result = detect_black_bars(video, config)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to process {video}: {e}")

    generate_report(results, config)


if __name__ == "__main__":
    main()
