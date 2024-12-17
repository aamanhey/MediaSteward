# TikTok Video Downloader and Cataloguer

This project is a Python-based TikTok video downloader that runs inside a Docker container. It allows you to download TikTok videos and collections to your computer while managing the files and metadata. The program is designed for ease of use and future expandability.

## Features

    Download TikTok Videos:
        Provide a direct link to a TikTok video or a collection.
        Videos are downloaded into a local folder (downloads) on your computer.

    Isolated Docker Environment:
        The program runs inside a Docker container, so you don’t need to install dependencies on your local machine.

    Simple Command-Line Interface:
        Easy to use commands for downloading videos.

    Future Features (Planned):
        Extract and store metadata (e.g., author, date, video size, tags) in a JSON catalog.
        Manage storage limits for collections, stopping downloads when limits are reached but continuing to collect metadata.

## Project Structure

tiktok_downloader/
│
├── Dockerfile                # Docker configuration file
├── requirements.txt          # Python dependencies
├── tiktok_downloader.py      # Main Python script to download videos
└── downloads/                # Local folder where videos are saved

## Requirements

    Docker must be installed on your computer.
        Download and install Docker here: https://www.docker.com/

    Basic familiarity with running Docker commands from the terminal.

## Setup Instructions
1. Clone the Project

First, clone this repository to your local machine:

git clone <repository-url>
cd tiktok_downloader

2. Build the Docker Image

Use the following command to build the Docker image:

docker build -t tiktok_downloader .

    tiktok_downloader: This is the name of the Docker image.

3. Run the Program
To Download a Single TikTok Video:

Run the following command:

docker run --rm -v "$(pwd)/downloads:/app/tiktok_downloads" tiktok_downloader video "<video-url>"

Replace <video-url> with the TikTok video link, for example:

docker run --rm -v "$(pwd)/downloads:/app/tiktok_downloads" tiktok_downloader video "https://www.tiktok.com/@janro_2109/video/7445809155136326917?lang=en"

4. View Your Downloads

After running the command:

    Videos will be saved in the downloads/ folder in the project directory.

    Planned Features (Next Steps)

    Video Metadata Collection:
        Extract video details like:
            Author name
            Video creation date
            Video length
            File size
            Video tags (if available)
        Save this metadata as a JSON file in the downloads folder.

    Video Size Limits:
        Allow users to set a size limit (e.g., 500MB for a collection).
        If the size limit is exceeded:
            Stop downloading large video files.
            Continue to scrape and save metadata for the remaining videos instead.

    Video Catalog:
        Maintain a catalog.json file that organizes metadata for all downloaded videos.

## Commands
Build the project
docker build -t tiktok_downloader .

Get the metadata for a collection without downloading the videos.
docker run --rm -v "$(pwd)/downloads:/app/downloads" tiktok_downloader sdcollection "https://www.tiktok.com/@adrianmanhey/collection/Clips-7350903529052425006" "skim_clips.json"

Download a TikTok collection and save the metadata.
docker run --rm -v "$(pwd)/downloads:/app/downloads" tiktok_downloader sdcollection "https://www.tiktok.com/@adrianmanhey/collection/Clips-7350903529052425006" "clips.json"

Read a TikTok collection from JSON.
docker run --rm -v "$(pwd)/downloads:/app/downloads" tiktok_downloader list " " "skim_clips/skim_clips.json"

Step 6: Build and Run the Web Server

    Build the Docker image:

docker build -t file_streamer .

    Run the container:

docker run --rm -p 5000:5000 -v "$(pwd)/downloads:/app/downloads" tiktok_downloader media_streamer/server.py

docker run --rm -v "$(pwd)/downloads:/app/downloads" tiktok_downloader list  " "

docker run --rm -v "$(pwd)/downloads:/app/downloads" -v "$(pwd)/catalog.json:/app/catalog.json" tiktok_downloader video "https://www.tiktok.com/@janro_2109/video/7445809155136326917"

docker run --rm -v "$(pwd)/downloads:/app/downloads" tiktok_downloader collection "https://www.tiktok.com/@adrianmanhey/collection/Los%20Angeles-7327482342845483819?lang=en"

docker run --rm -v "$(pwd)/downloads:/app/downloads" tiktok_downloader collection https://www.tiktok.com/@adrianmanhey/collection/

## Collections
- https://www.tiktok.com/@adrianmanhey/collection/Los%20Angeles-7327482342845483819?lang=en
- https://www.tiktok.com/@adrianmanhey/collection/Clips-7350903529052425006?is_from_webapp=1&sender_device=pc
- https://www.tiktok.com/@adrianmanhey/collection/UP-7287386486037662507?lang=en
- https://www.tiktok.com/@adrianmanhey/collection/Brain-7247113726611180334?lang=en

## Resources
- https://pypi.org/project/yt-dlp/#output-template

def load_collection_metadata(collection_path, collection_name):
    """Load metadata from collection.json in the selected collection folder."""
    metadata_file = os.path.join(collection_path, f"{collection_name}.json")
    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
            return json.load(f).get("videos", [])
    return []