import subprocess
import logging


def detect_black_bars(video_path, config):
    """
    Detect black bars in a video using ffmpeg cropdetect.

    Args:
        video_path (Path): Path to the video file.
        config (dict): Configuration options.

    Returns:
        dict: Detection result.
    """
    logger = logging.getLogger(__name__)

    command = [
        "ffmpeg",
        "-ss", "150",
        "-i", str(video_path),
        "-vf", "cropdetect=24:16:0",
        "-frames:v", str(config.get("sample_frames", 100)),
        "-f", "null", "-"
    ]

    process = subprocess.run(
        command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output = process.stderr

    crop_lines = [line for line in output.split('\n') if 'crop=' in line]

    if not crop_lines:
        raise RuntimeError("No crop data detected.")

    last_crop = crop_lines[-1].split('crop=')[1].split()[0]

    width, height, x, y = map(int, last_crop.split(':'))

    # Simplified detection logic
    has_letterboxing = y > 0
    has_pillarboxing = x > 0

    resolution = f"{config.get('video_width', 'Unknown')}x{config.get('video_height', 'Unknown')}"

    return {
        "file_path": str(video_path),
        "resolution": resolution,
        "has_letterboxing": has_letterboxing,
        "has_pillarboxing": has_pillarboxing,
        "detected_borders": {"top": y, "bottom": y, "left": x, "right": x},
        "suggested_crop": last_crop,
        "aspect_ratio": f"{width}:{height}",
        "notes": ""
    }
