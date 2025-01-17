import os
import sys
import requests

from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL

from catalog_reader import read_catalogue
from metadata_scraper import fetch_video_metadata, save_metadata_to_json
from utils import get_file_size, collections

DOWNLOAD_FOLDER = "downloads/"

def download_video(video_url, filename=None, size_limit_mb=None, skip_download=False):
    """
    Download a TikTok video and save its metadata.
    Args:
        video_url (str): URL of the TikTok video.
        size_limit_mb (float): Optional size limit in MB.
    """
    try:
        video_id = video_url.split('/video/')[-1].split('?')[0]
        print("----{}----".format(video_id))

        if filename is None:
            filename = "catalog.json"
        elif filename == " " or filename == "":
            filename = "test.json"

        output_folder = DOWNLOAD_FOLDER + filename.split(".")[0] + "/"
        # Ensure the downloads folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        meta_filename = output_folder + filename
        # Set up yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(output_folder,  f'{video_id}.%(ext)s'),
            'format': 'best',
            'quiet': True
        }

        with YoutubeDL(ydl_opts) as ydl:
            # Extract video information
            info = ydl.extract_info(video_url, download=False)
            video_size_mb = info['filesize'] / (1024 * 1024) if info.get('filesize') else 0

            print(f"Video size: {video_size_mb:.2f} MB")
            if (size_limit_mb and video_size_mb > size_limit_mb) or skip_download:
                if skip_download:
                    print("Light config: Skipping download.")
                else:
                    print("Size limit exceeded. Skipping video download.")
                # Save metadata only
                metadata = fetch_video_metadata(video_url, ydl.sanitize_info(info))
                save_metadata_to_json(metadata, output_file=meta_filename)
                return

            # Download the video
            print("Downloading video...")
            ydl.download([video_url])
            print("/nDownload complete.")

            # Save metadata
            metadata = fetch_video_metadata(video_url,  ydl.sanitize_info(info), video_id)
            save_metadata_to_json(metadata, output_file=meta_filename)

            return metadata

    except Exception as e:
        print(f"Error downloading video: {e}")

def scrape_collection_links(collection_url):
    """
    Extract video links from a TikTok collection using yt-dlp.
    
    Args:
        collection_url (str): URL of the TikTok collection page
    
    Returns:
        list: Unique video links from the collection
    """
    try:
        # Set up yt-dlp options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # Only extract info, don't download
        }

        # Use YoutubeDL to extract playlist/collection information
        with YoutubeDL(ydl_opts) as ydl:
            # Extract collection information
            info = ydl.extract_info(collection_url, download=False)
            
            # Handle different possible structures
            if 'entries' in info:
                # Extract video URLs from the collection
                video_links = [entry['url'] for entry in info['entries'] if entry.get('url')]
            else:
                # Fallback if no entries found
                video_links = []

        # Remove duplicates while preserving order
        unique_video_links = list(dict.fromkeys(video_links))
        
        print(f"Found {len(unique_video_links)} unique videos in the collection.")
        return unique_video_links

    except Exception as e:
        print(f"Error extracting collection links: {e}")
        return []

def download_collection(collection_url, filename=None, collection_size_limit=500, video_size_limit_mb=None, skip_download=False):
    """
    Download all videos from a TikTok collection.
    """
    video_links = scrape_collection_links(collection_url)
    print(f"--{"New Collection"}----")
    print(f"Found {len(video_links)} videos in the collection.")
    curr_size = 0
    for link in video_links:
        try:
            if collection_size_limit > curr_size:
                adjusted_size_limit = min(collection_size_limit - curr_size, video_size_limit_mb)
                metadata = download_video(link, filename=filename, size_limit_mb=adjusted_size_limit, skip_download=skip_download)
            else:
                metadata = download_video(link, filename=filename, size_limit_mb=video_size_limit_mb, skip_download=True)
            curr_size += metadata["size_mb"]
            print("Current collection size: {}/{}".format(curr_size, collection_size_limit))
        except Exception as e:
            print(f"Failed to download {link}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 4:
        print("Usage: python tiktok_downloader.py [video] <URL>")
        sys.exit(1)

    mode = sys.argv[1]
    url = sys.argv[2]
    filename = sys.argv[3]

    print(f"Arguments: {mode} {url} {filename}")

    if url in collections.keys():
        url = collections[url]


    # Ensure the downloads folder exists
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    if mode == "video":
        download_video(url, size_limit_mb=50, skip_download=False)  # Example size limit: 50MB
    elif mode == "collection":
        filename = sys.argv[3]
        download_collection(url, collection_size_limit=500, video_size_limit_mb=50, filename=filename, skip_download=False)
    elif mode == "sdvideo":
        filename = sys.argv[3]
        download_video(url, size_limit_mb=50, filename=filename, skip_download=True)  # Example size limit: 50MB
    elif mode == "sdcollection":
        filename = sys.argv[3]
        download_collection(url, collection_size_limit=500, video_size_limit_mb=50, filename=filename, skip_download=True)
    elif mode == "list":
        filename = sys.argv[3]
        read_catalogue(filename=filename)

    else:
        print("Invalid mode. Use ['video', collection, sdvideo, sdcollection, list].")
