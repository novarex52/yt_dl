# Command-Line YouTube Downloader

## Description

This is a Python script that allows you to download YouTube videos from your command line. You can specify the YouTube video URL and choose from available video streams to download.

## Prerequisites

*   Python 3.x
*   pip (Python package installer)

## Installation

1.  **Clone the repository or download the script.** (Assuming it's in a repo, otherwise, just "Ensure you have the `downloader.py` script.")
2.  **Install required libraries:**
    The script relies on the following Python libraries: `pytube`, `requests`, and `BeautifulSoup4`. If you haven't installed them globally (as was done during development), you can install them using pip:
    ```bash
    pip install pytube requests beautifulsoup4
    ```

## Usage

Run the script from your terminal using the `python` interpreter:

```bash
python downloader.py <YOUTUBE_VIDEO_URL> [options]
```

**Arguments:**

*   `<YOUTUBE_VIDEO_URL>`: (Required) The full URL of the YouTube video you want to download.
*   `-o <OUTPUT_PATH>`, `--output <OUTPUT_PATH>`: (Optional) The directory where you want to save the downloaded video. If not specified, the video will be saved in the same directory as the script.

**Interactive Stream Selection:**

After providing the URL, the script will fetch available video streams (different resolutions and file types). It will then present you with a numbered list of these streams, and you'll be prompted to enter the number corresponding to your desired quality.

## Example Usage

```bash
# Download a video to the current directory
python downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Download a video to a specific directory (e.g., /path/to/your/videos)
python downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o "/path/to/your/videos"
```

## Running Tests

Unit tests are provided in `test_downloader.py`. To run them:

1.  Navigate to the `youtube_downloader` directory (or the directory containing `downloader.py` and `test_downloader.py`).
2.  Run the following command:

    ```bash
    python -m unittest test_downloader.py
    ```
    Alternatively, if `test_downloader.py` is directly executable:
    ```bash
    python test_downloader.py
    ```
