import sys
import qrcode
from dotenv import load_dotenv
import logging.config
from pathlib import Path
import os

# Load environment variables
load_dotenv()

# Environment Variables for Configuration
DATA_URL = os.getenv('QR_DATA_URL', 'https://github.com/kaw393939')
QR_DIRECTORY = os.getenv('QR_CODE_DIR', 'qr_codes')  # Directory for saving QR code
QR_FILENAME = os.getenv('QR_CODE_FILENAME', 'MyQRCode2.png')  # Filename for the QR code
FILL_COLOR = os.getenv('FILL_COLOR', 'red')  # Fill color for the QR code
BACK_COLOR = os.getenv('BACK_COLOR', 'white')  # Background color for the QR code

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),  # Log to stdout
            # If you still want to log to a file, you can add a FileHandler here as well
            # logging.FileHandler('logs/myapp.log'),  # Example for logging to a file
        ]
    )


def create_directory(path: Path):
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        exit(1)

def generate_qr_code(data, path, fill_color='red', back_color='white'):
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        with path.open('wb') as qr_file:
            img.save(qr_file)
        logging.info(f"QR code successfully saved to {path}")

    except Exception as e:
        logging.error(f"An error occurred while generating or saving the QR code: {e}")

def main():
    # Initial logging setup attempt
    setup_logging()
    
    # Create the full path for the QR code file
    qr_code_full_path = Path.cwd() / QR_DIRECTORY / QR_FILENAME
    
    # Ensure the QR code directory exists
    create_directory(qr_code_full_path.parent)
    
    # Generate and save the QR code
    generate_qr_code(DATA_URL, qr_code_full_path, FILL_COLOR, BACK_COLOR)

if __name__ == "__main__":
    main()
