from pytube import YouTube
from pytube.exceptions import PytubeError, VideoUnavailable, RegexMatchError
import os
import argparse
import sys # Added for parse_cli_args to take args list

def on_progress(stream, chunk, bytes_remaining):
    """Callback function to display download progress."""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Downloading... {percentage:.2f}% complete", end='\r')

def get_video_info(url):
    """
    Fetches video information (title and available streams) from a YouTube URL.

    Args:
        url: The YouTube video URL.

    Returns:
        A dictionary containing the video title and a list of stream information,
        or None if an error occurs.
    """
    print("Fetching video information...")
    try:
        yt = YouTube(url)
        video_title = yt.title
        
        streams_info = []
        for stream in yt.streams:
            streams_info.append({
                'resolution': stream.resolution,
                'extension': stream.mime_type.split('/')[-1] if stream.mime_type else None, # Extract extension from mime_type
                'itag': stream.itag,
                'type': stream.type,
                'abr': stream.abr if stream.type == 'audio' else None # average bitrate for audio
            })
        print("Video information fetched successfully.")
        return {
            'title': video_title,
            'streams': streams_info
        }
    except VideoUnavailable:
        print("Error: The video is unavailable. It might be private, deleted, or region restricted.")
        return None
    except RegexMatchError:
        print("Error: Could not parse video information. Please check the URL format and ensure it's a valid YouTube video URL.")
        return None
    except PytubeError as e:
        print(f"Pytube error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching video info: {e}")
        return None

def select_stream(streams_info):
    """
    Prompts the user to select a stream from a list and returns its itag.
    """
    if not streams_info:
        print("No streams available for selection.")
        return None

    print("\nProcessing available streams...")
    print("Available Streams:")
    for i, stream in enumerate(streams_info):
        if stream['type'] == 'video':
            print(f"  {i+1}: Resolution: {stream.get('resolution')}, Type: video/{stream.get('extension')}, ITAG: {stream.get('itag')}")
        elif stream['type'] == 'audio':
            print(f"  {i+1}: Bitrate: {stream.get('abr')}, Type: audio/{stream.get('extension')}, ITAG: {stream.get('itag')}")
        else:
            print(f"  {i+1}: Type: {stream.get('type')}/{stream.get('extension')}, Resolution: {stream.get('resolution')}, ITAG: {stream.get('itag')}")


    while True:
        try:
            choice = input("Enter the number of the stream you want to download: ")
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(streams_info):
                return streams_info[choice_index]['itag']
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(streams_info)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred during selection: {e}")
            return None

def download_video(url, stream_itag, output_path="."):
    """
    Downloads a specific video stream using its itag.
    """
    try:
        print(f"\nPreparing to download stream itag: {stream_itag}...")
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.get_by_itag(stream_itag)
        
        if not stream:
            print(f"Error: Could not find stream with itag {stream_itag}. It might no longer be available.")
            return

        print(f"Starting download of '{yt.title}'...")
        # Ensure the output directory exists
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
                print(f"Created download directory: {os.path.abspath(output_path)}")
            except (OSError, PermissionError) as e:
                print(f"Error creating directory {output_path}: {e}")
                return
            
        filepath = stream.download(output_path=output_path)
        print(f"\nDownload complete!") # Newline after progress bar
        print(f"Video downloaded successfully to: {os.path.abspath(filepath)}")

    except VideoUnavailable:
        print("Error: The video is unavailable for download. It might have been removed or become private.")
    except RegexMatchError:
        print("Error: Could not parse video information for download. Please check the URL.")
    except PytubeError as e:
        print(f"\nPytube error during download: {e}") # Newline after progress bar if error occurs mid-download
    except (IOError, OSError, PermissionError) as e:
        print(f"\nFile system error during download: {e}") # Newline after progress bar
    except Exception as e:
        print(f"\nAn unexpected error occurred during download: {e}") # Newline after progress bar
    finally:
        # Unregister callback, though with current structure yt object is local. Good practice.
        if 'yt' in locals() and yt:
            yt.unregister_on_progress_callback(on_progress)

def parse_cli_args(args=None):
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Download YouTube videos.")
    parser.add_argument("url", help="The YouTube video URL.")
    parser.add_argument("-o", "--output", default=".", help="The output directory for the downloaded video. Defaults to the current directory.")
    # If args is None, argparse uses sys.argv[1:]
    # Otherwise, it uses the provided list (useful for testing)
    return parser.parse_args(args)

def main():
    # Pass sys.argv[1:] to parse_cli_args for normal execution
    # parse_cli_args can also be called with a specific list for testing
    args = parse_cli_args(sys.argv[1:]) 
    
    video_url = args.url
    download_directory = args.output

    video_info = get_video_info(video_url)
    
    if video_info:
        print(f"\nTitle: {video_info['title']}")
        
        if video_info['streams']:
            chosen_itag = select_stream(video_info['streams'])
            
            if chosen_itag:
                download_video(video_url, chosen_itag, output_path=download_directory)
            else:
                print("No stream selected for download or selection failed.")
        else:
            print("No downloadable streams found for this video.")
    else:
        print("Could not fetch video information for the provided URL. Please check the URL and try again.")

if __name__ == "__main__":
    main()
