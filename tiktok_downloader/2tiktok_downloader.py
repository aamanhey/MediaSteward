import os
import sys
import requests
from bs4 import BeautifulSoup
import yt_dlp

def download_video(video_url, output_dir):
    """
    Download a single TikTok video using yt-dlp.
    """
    print(f"Downloading video: {video_url}")
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'best'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def scrape_collection_links(collection_url):
    """
    Scrape video links from a TikTok collection page.
    """
    print(f"Scraping collection: {collection_url}")
    response = requests.get(collection_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Replace this selector with actual logic for TikTok collection pages
    video_links = [a['href'] for a in soup.find_all('a') if '/video/' in a['href']]
    return list(set(video_links))  # Remove duplicates

def download_collection(collection_url, output_dir):
    """
    Download all videos from a TikTok collection.
    """
    video_links = scrape_collection_links(collection_url)
    print(f"Found {len(video_links)} videos in the collection.")
    for link in video_links:
        try:
            download_video(link, output_dir)
        except Exception as e:
            print(f"Failed to download {link}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python tiktok_downloader.py [video|collection] <URL>")
        sys.exit(1)

    mode = sys.argv[1]
    url = sys.argv[2]
    output_directory = "./tiktok_downloads"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if mode == "video":
        download_video(url, output_directory)
    elif mode == "collection":
        download_collection(url, output_directory)
    else:
        print("Invalid mode. Use 'video' or 'collection'.")