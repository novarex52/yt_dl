import unittest
import sys
from unittest.mock import patch, MagicMock
# Assuming your main script is youtube_downloader/downloader.py
# and it's in the same directory or PYTHONPATH is set up correctly.
import downloader 

class TestGetVideoInfo(unittest.TestCase):
    # Test URLs
    VALID_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Rick Astley - Never Gonna Give You Up
    INVALID_URL_FORMAT = "this is not a valid youtube url"
    # For unavailable video, it's hard to find a permanently unavailable one.
    # Pytube's VideoUnavailable exception is caught and downloader.get_video_info returns None.
    # We can use a URL that is likely to be private or quickly taken down, or simulate the exception.
    # A more robust test would mock the YouTube object to raise VideoUnavailable.
    UNAVAILABLE_VIDEO_URL = "https://www.youtube.com/watch?v=hopefullyinvalidvideo" # Placeholder

    @patch('builtins.print') # Suppress print statements during test
    def test_valid_url_fetches_info(self, mock_print):
        """Test that a valid YouTube URL fetches video information."""
        video_info = downloader.get_video_info(self.VALID_URL)
        self.assertIsNotNone(video_info, "Video info should not be None for a valid URL.")
        self.assertIn('title', video_info, "Video info should contain a 'title'.")
        self.assertIsInstance(video_info['title'], str, "Title should be a string.")
        self.assertIn('streams', video_info, "Video info should contain 'streams'.")
        self.assertIsInstance(video_info['streams'], list, "Streams should be a list.")
        if video_info['streams'] is not None: # Streams can be None if fetching fails after title
            self.assertTrue(len(video_info['streams']) > 0, "Streams list should not be empty for a valid video.")

    @patch('builtins.print') # Suppress print statements
    def test_invalid_url_format_returns_none(self, mock_print):
        """Test that an invalidly formatted URL returns None."""
        # This should trigger RegexMatchError in get_video_info
        video_info = downloader.get_video_info(self.INVALID_URL_FORMAT)
        self.assertIsNone(video_info, "Video info should be None for an invalid URL format.")

    @patch('builtins.print')
    @patch('downloader.YouTube') # Mock the YouTube object
    def test_unavailable_video_returns_none(self, MockYouTube, mock_print):
        """Test that an unavailable video URL returns None by mocking VideoUnavailable."""
        # Configure the mock YouTube object to raise VideoUnavailable when instantiated
        mock_yt_instance = MockYouTube.return_value
        # Mock attributes that might be accessed before the exception point, if any.
        # Based on current get_video_info, title and streams are primary.
        mock_yt_instance.title = "Test Title" 
        mock_yt_instance.streams = [] 
        MockYouTube.side_effect = downloader.VideoUnavailable # Raise VideoUnavailable
        
        video_info = downloader.get_video_info("https://www.youtube.com/watch?v=anyvideo")
        self.assertIsNone(video_info, "Video info should be None for an unavailable video.")
        # Check if the specific error message for VideoUnavailable was printed
        mock_print.assert_any_call("Error: The video is unavailable. It might be private, deleted, or region restricted.")


class TestCLIArguments(unittest.TestCase):
    # Test the parse_cli_args function from downloader.py

    def test_url_argument_parsed(self):
        """Test that the URL argument is correctly parsed."""
        test_url = "https_youtube_com_my_video" 
        args = downloader.parse_cli_args([test_url])
        self.assertEqual(args.url, test_url)

    def test_output_argument_parsed(self):
        """Test that the output path argument is correctly parsed."""
        test_url = "https_youtube_com_my_video"
        test_output_path = "custom/path"
        args = downloader.parse_cli_args([test_url, '-o', test_output_path])
        self.assertEqual(args.output, test_output_path)
        
        args_long = downloader.parse_cli_args([test_url, '--output', test_output_path])
        self.assertEqual(args_long.output, test_output_path)

    def test_output_argument_default(self):
        """Test that the output path defaults to '.'."""
        test_url = "https_youtube_com_my_video"
        args = downloader.parse_cli_args([test_url])
        self.assertEqual(args.output, ".")

    @patch('sys.stderr', new_callable=MagicMock) # Suppress argparse error output for this test
    def test_missing_url_argument_exits(self, mock_stderr):
        """Test that argparse exits if the required URL argument is missing."""
        # argparse.ArgumentParser.parse_args() calls sys.exit() on error.
        # We need to catch this SystemExit.
        with self.assertRaises(SystemExit):
            downloader.parse_cli_args([])
        # For a more robust check, you could also assert that parser.error() was called
        # if you mock the ArgumentParser instance itself, but checking SystemExit is common.

if __name__ == '__main__':
    unittest.main()
