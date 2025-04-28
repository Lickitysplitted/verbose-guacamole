import json
from pathlib import Path
import logging


def generate_report(results, config):
    """
    Generate a JSON report from detection results.

    Args:
        results (list): List of detection dictionaries.
        config (dict): Configuration options.
    """
    logger = logging.getLogger(__name__)

    output_dir = Path(config.get("output_directory", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "black_bar_report.json"

    try:
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=4)
        logger.info(f"Report generated at {report_path}")
    except Exception as e:
        logger.error(f"Failed to write report: {e}")
