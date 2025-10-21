import argparse
import logging.config
import os
import sys
from datetime import datetime
from pathlib import Path

import qrcode  # type: ignore[import-untyped]
import validators
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment Variables for Configuration
# Directory for saving QR code
QR_DIRECTORY = os.getenv("QR_CODE_DIR", "qr_codes")
FILL_COLOR = os.getenv("FILL_COLOR", "red")  # Fill color for the QR code
# Background color for the QR code
BACK_COLOR = os.getenv("BACK_COLOR", "white")


def setup_logging() -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def create_directory(path: Path) -> None:
    """Create directory if it doesn't exist."""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        sys.exit(1)


def is_valid_url(url: str) -> bool:
    """Validate if the provided URL is valid."""
    if validators.url(url):
        return True
    else:
        logging.error(f"Invalid URL provided: {url}")
        return False


def generate_qr_code(
    data: str, path: Path, fill_color: str = "red", back_color: str = "white"
) -> None:
    """Generate QR code and save to specified path."""
    if not is_valid_url(data):
        return  # Exit the function if the URL is not valid

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        with path.open("wb") as qr_file:
            img.save(qr_file)
        logging.info(f"QR code successfully saved to {path}")

    except Exception as e:
        error_msg = f"Error generating or saving QR code: {e}"
        logging.error(error_msg)


def main() -> None:
    """Main function to generate QR code."""
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Generate a QR code.")
    parser.add_argument(
        "--url",
        help="The URL to encode in the QR code",
        default="https://github.com/kaw393939",
    )
    args = parser.parse_args()

    # Initial logging setup
    setup_logging()

    # Generate a timestamped filename for the QR code
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    qr_filename = f"QRCode_{timestamp}.png"

    # Create the full path for the QR code file
    qr_code_full_path = Path.cwd() / QR_DIRECTORY / qr_filename

    # Ensure the QR code directory exists
    create_directory(Path.cwd() / QR_DIRECTORY)

    # Generate and save the QR code
    generate_qr_code(args.url, qr_code_full_path, FILL_COLOR, BACK_COLOR)


if __name__ == "__main__":
    main()
