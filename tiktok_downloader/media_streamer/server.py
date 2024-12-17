from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import os
import json
import re

app = Flask(__name__)

BASE_DOWNLOADS_DIR = os.path.join(os.getcwd(), "downloads")

def list_subfolders(directory):
    """List subfolders (collections) in the given directory."""
    return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

def load_collection_metadata(collection_path, collection_name):
    """Load metadata from collection.json in the selected collection folder."""
    metadata_file = os.path.join(collection_path, f"{collection_name}.json")
    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
            return json.load(f).get("videos", [])
    return []

def extract_video_id_from_url(url):
    """Extract video ID from a TikTok URL."""
    match = re.search(r'/video/(\d+)', url)
    return match.group(1) if match else None

def extract_video_id_from_filename(filename):
    """Extract video ID from filename."""
    return os.path.splitext(filename)[0]

@app.route("/", methods=["GET", "POST"])
def index():
    """Display the list of collections (subfolders) in the downloads directory."""
    collections = list_subfolders(BASE_DOWNLOADS_DIR)
    return render_template("collections.html", collections=collections)

@app.route("/collection/<collection_name>", methods=["GET", "POST"])
def view_collection(collection_name):
    """View the table of videos and metadata for a selected collection."""
    collection_path = os.path.join(BASE_DOWNLOADS_DIR, collection_name)

    if not os.path.exists(collection_path):
        return f"Collection '{collection_name}' not found", 404

    # List video files and load metadata
    video_files = [f for f in os.listdir(collection_path) if f.endswith((".mp4", ".webm", ".mkv", ".mp3"))]
    metadata = load_collection_metadata(collection_path, collection_name)

    # Get the search query from the form (if any)
    search_query = request.args.get("search", "").lower()

    # Match files with metadata and filter by search query
    file_info = []
    for file in video_files:
        file_path = os.path.join(collection_path, file)
        file_id = extract_video_id_from_filename(file)

        # Find matching metadata by comparing video IDs
        matching_meta = next(
            (m for m in metadata if extract_video_id_from_url(m['url']) == file_id), 
            None
        )

        # Check if the file or metadata matches the search query
        if (search_query in file.lower() or
            (matching_meta and search_query in matching_meta.get("author", "").lower())):
            file_info.append({
                "name": file,
                "size": round(os.path.getsize(file_path) / (1024 * 1024), 2),  # File size in MB
                "author": matching_meta["author"] if matching_meta else "Unknown",
                "date": matching_meta["upload_date"] if matching_meta else "Unknown",
                "url": f"/stream/{collection_name}/{file}"
            })

    return render_template("index.html", collection_name=collection_name, files=file_info)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Page for submitting video or collection URL to download."""
    if request.method == "POST":
        url = request.form["url"]
        collection_name = request.form["collection_name"]
        size_limit_mb = 50  # Set a size limit (50MB)

        # Validate URL
        if "tiktok.com" not in url:
            return "Invalid TikTok URL", 400

        # Download the video or collection (based on URL type)
        download_video_or_collection(url, collection_name, size_limit_mb)

        return redirect(url_for("view_collection", collection_name=collection_name))

    return render_template("upload.html")

def download_video_or_collection(url, collection_name, size_limit_mb):
    """Download a video or collection based on the provided URL."""
    # This function will check if the URL is for a single video or a collection
    # and then download it using yt-dlp.

    if "/video/" in url:
        # Download a single video
        download_video(url, collection_name, size_limit_mb)
    else:
        # Download a collection of videos
        download_collection(url, collection_name, size_limit_mb)

def download_video(url, collection_name, size_limit_mb):
    """Download a single TikTok video."""
    from yt_dlp import YoutubeDL
    collection_path = os.path.join(BASE_DOWNLOADS_DIR, collection_name)
    if not os.path.exists(collection_path):
        os.makedirs(collection_path)

    # Download using yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(collection_path, '%(id)s.%(ext)s'),
        'format': 'best',
        'quiet': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_size_mb = info.get('filesize', 0) / (1024 * 1024)
        
        # Only download if under the size limit
        if size_limit_mb and video_size_mb > size_limit_mb:
            print("Video exceeds size limit, skipping download.")
            return

        # Download the video
        ydl.download([url])

def download_collection(url, collection_name, size_limit_mb):
    """Download a collection of TikTok videos."""
    collection_path = os.path.join(BASE_DOWNLOADS_DIR, collection_name)
    if not os.path.exists(collection_path):
        os.makedirs(collection_path)

    # Download using yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(collection_path, '%(id)s.%(ext)s'),
        'quiet': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        for video in info['entries']:
            video_size_mb = video.get('filesize', 0) / (1024 * 1024)

            # Only download if under the size limit
            if size_limit_mb and video_size_mb > size_limit_mb:
                print(f"Video {video['title']} exceeds size limit, skipping.")
                continue

            ydl.download([video['url']])

@app.route("/stream/<collection_name>/<path:filename>")
def stream_file(collection_name, filename):
    """Stream a specific file from a collection."""
    collection_path = os.path.join(BASE_DOWNLOADS_DIR, collection_name)
    try:
        return send_from_directory(collection_path, filename)
    except FileNotFoundError:
        return f"File '{filename}' not found in {collection_path}", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
