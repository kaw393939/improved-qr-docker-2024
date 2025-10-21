"""Tests for main.py QR code functionality."""
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

import main


class TestQRCodeGeneration:
    """Test cases for QR code generation functionality."""

    def test_is_valid_url_with_valid_url(self):
        """Test URL validation with a valid URL."""
        assert main.is_valid_url("https://github.com/kaw393939") is True

    def test_is_valid_url_with_invalid_url(self):
        """Test URL validation with an invalid URL."""
        with patch("main.logging.error") as mock_logger:
            assert main.is_valid_url("not-a-valid-url") is False
            mock_logger.assert_called_once()

    def test_create_directory_success(self):
        """Test successful directory creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir) / "test_qr_codes"
            main.create_directory(test_path)
            assert test_path.exists()
            assert test_path.is_dir()

    def test_create_directory_failure(self):
        """Test directory creation failure."""
        with patch("pathlib.Path.mkdir") as mock_mkdir:
            mock_mkdir.side_effect = PermissionError("Access denied")
            with patch("main.logging.error") as mock_logger:
                with pytest.raises(SystemExit):
                    main.create_directory(Path("/invalid/path"))
                mock_logger.assert_called_once()

    @patch("main.qrcode.QRCode")
    @patch("main.is_valid_url")
    def test_generate_qr_code_success(self, mock_is_valid, mock_qr_class):
        """Test successful QR code generation."""
        # Setup mocks
        mock_is_valid.return_value = True
        mock_qr = MagicMock()
        mock_qr_class.return_value = mock_qr
        mock_img = MagicMock()
        mock_qr.make_image.return_value = mock_img

        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir) / "test.png"

            # Call the function
            main.generate_qr_code(
                "https://example.com", test_path, "red", "white"
            )

            # Verify calls
            mock_qr.add_data.assert_called_once_with("https://example.com")
            mock_qr.make.assert_called_once_with(fit=True)
            mock_qr.make_image.assert_called_once_with(
                fill_color="red", back_color="white"
            )

    @patch("main.is_valid_url")
    def test_generate_qr_code_invalid_url(self, mock_is_valid):
        """Test QR code generation with invalid URL."""
        mock_is_valid.return_value = False

        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir) / "test.png"

            # This should return early without creating a file
            main.generate_qr_code("invalid-url", test_path)

            assert not test_path.exists()

    @patch("main.qrcode.QRCode")
    @patch("main.is_valid_url")
    def test_generate_qr_code_exception(self, mock_is_valid, mock_qr_class):
        """Test QR code generation with exception."""
        mock_is_valid.return_value = True
        mock_qr_class.side_effect = Exception("QR code creation failed")

        with patch("main.logging.error") as mock_logger:
            with tempfile.TemporaryDirectory() as temp_dir:
                test_path = Path(temp_dir) / "test.png"

                main.generate_qr_code("https://example.com", test_path)

                mock_logger.assert_called_once()

    @patch("main.setup_logging")
    @patch("main.create_directory")
    @patch("main.generate_qr_code")
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_function(
        self,
        mock_parse_args,
        mock_generate,
        mock_create_dir,
        mock_setup_logging,
    ):
        """Test the main function."""
        # Setup mock arguments
        mock_args = MagicMock()
        mock_args.url = "https://example.com"
        mock_parse_args.return_value = mock_args

        # Call main function
        main.main()

        # Verify function calls
        mock_setup_logging.assert_called_once()
        mock_create_dir.assert_called_once()
        mock_generate.assert_called_once()


class TestEnvironmentVariables:
    """Test cases for environment variable handling."""

    def test_default_environment_values(self):
        """Test that default values are used when env vars are not set."""
        # Clear environment variables
        with patch.dict(os.environ, {}, clear=True):
            # Reload the module to get fresh environment values
            import importlib

            importlib.reload(main)

            assert main.QR_DIRECTORY == "qr_codes"
            assert main.FILL_COLOR == "red"
            assert main.BACK_COLOR == "white"

    def test_custom_environment_values(self):
        """Test that custom environment values are used."""
        env_vars = {
            "QR_CODE_DIR": "custom_qr_codes",
            "FILL_COLOR": "blue",
            "BACK_COLOR": "black",
        }

        with patch.dict(os.environ, env_vars):
            import importlib

            importlib.reload(main)

            assert main.QR_DIRECTORY == "custom_qr_codes"
            assert main.FILL_COLOR == "blue"
            assert main.BACK_COLOR == "black"
