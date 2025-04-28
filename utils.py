import logging
import shutil
from pathlib import Path


def setup_logging(config):
    """
    Setup logging configuration.
    """
    log_dir = Path(config.get("log_directory", "logs"))
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=log_dir / "error.log",
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def check_ffmpeg():
    """
    Check if ffmpeg is installed.
    """
    return shutil.which("ffmpeg") is not None


def get_video_files(input_path):
    """
    Get list of video files from a path.
    """
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv']

    if input_path.is_file():
        return [input_path] if input_path.suffix.lower() in video_extensions else []

    return [f for f in input_path.rglob('*') if f.suffix.lower() in video_extensions]
