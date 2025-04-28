import json
import logging
import subprocess
import sys
from pathlib import Path

from utils import setup_logging, check_ffmpeg


def crop_videos(report_path, config):
    """
    Crop videos according to suggested crop values in the report.
    Skips cropping if detected borders are all below the threshold.

    Args:
        report_path (Path): Path to the JSON report.
        config (dict): Configuration options.
    """
    logger = logging.getLogger(__name__)

    if not report_path.exists():
        logger.error(f"Report file {report_path} does not exist.")
        return

    with open(report_path, 'r') as f:
        entries = json.load(f)

    cropped_dir = Path(config.get(
        "cropped_output_directory", "cropped_videos"))
    cropped_dir.mkdir(parents=True, exist_ok=True)

    threshold = config.get("crop_threshold", 0)

    for entry in entries:
        borders = entry.get("detected_borders", {})
        top = borders.get("top", 0)
        bottom = borders.get("bottom", 0)
        left = borders.get("left", 0)
        right = borders.get("right", 0)

        # Skip if all borders are below or equal to threshold
        if top <= threshold and bottom <= threshold and left <= threshold and right <= threshold:
            logger.info(
                f"Skipping {entry.get('file_path')} - borders below threshold ({threshold}px)")
            continue

        crop = entry.get("suggested_crop")
        input_file = Path(entry["file_path"])
        output_file = cropped_dir / input_file.name

        command = [
            "ffmpeg",
            "-i", str(input_file),
            "-filter:v", f"crop={crop}",
            "-c:a", "copy",
            str(output_file)
        ]

        try:
            subprocess.run(command, check=True)
            logger.info(f"Cropped {input_file} -> {output_file}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error cropping {input_file}: {e}")


def main():
    """Main function for cropping videos."""
    config = json.load(open('config.json'))
    setup_logging(config)
    logger = logging.getLogger(__name__)

    if not check_ffmpeg():
        logger.error("ffmpeg is not installed or not in PATH.")
        sys.exit(1)

    report_path = Path(config.get("output_directory", "output")
                       ) / "black_bar_report.json"
    crop_videos(report_path, config)


if __name__ == "__main__":
    main()
