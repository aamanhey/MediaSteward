from flask import Flask, render_template, send_from_directory
import os
import json
import re

app = Flask(__name__)

# Base downloads directory where all collections reside
BASE_DOWNLOADS_DIR = os.path.join(os.getcwd(), "downloads")

def list_subfolders(directory):
    """List all subfolders (collections) in the given directory."""
    return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

def load_collection_metadata(collection_path, collection_name):
    """Load metadata from collection.json in the selected collection folder."""
    metadata_file = os.path.join(collection_path, f"{collection_name}.json")
    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
            return json.load(f).get("videos", [])
    return []

def extract_video_id_from_url(url):
    """Extract the video ID from a TikTok URL."""
    match = re.search(r'/video/(\d+)', url)
    return match.group(1) if match else None

def extract_video_id_from_filename(filename):
    """Extract video ID (numbers) from a filename."""
    return os.path.splitext(filename)[0]

@app.route("/")
def index():
    """
    Display the list of collections (subfolders) in the downloads directory.
    """
    collections = list_subfolders(BASE_DOWNLOADS_DIR)
    return render_template("collections.html", collections=collections)

@app.route("/collection/<collection_name>")
def view_collection(collection_name):
    """
    View the table of videos and metadata for a selected collection.
    """
    collection_path = os.path.join(BASE_DOWNLOADS_DIR, collection_name)

    # Check if the collection exists
    if not os.path.exists(collection_path):
        return f"Collection '{collection_name}' not found", 404

    # Load files and metadata
    video_files = [f for f in os.listdir(collection_path) if f.endswith((".mp4", ".webm", ".mkv", ".mp3"))]
    metadata = load_collection_metadata(collection_path, collection_name)

    # Match files with metadata
    file_info = []
    for file in video_files:
        file_path = os.path.join(collection_path, file)
        file_id = extract_video_id_from_filename(file)

        # Find matching metadata by comparing video IDs
        matching_meta = next(
            (m for m in metadata if extract_video_id_from_url(m['url']) == file_id), 
            None
        )

        file_info.append({
            "name": file,
            "size": round(os.path.getsize(file_path) / (1024 * 1024), 2),  # File size in MB
            "author": matching_meta["author"] if matching_meta else "Unknown",
            "date": matching_meta["upload_date"] if matching_meta else "Unknown",
            "url": f"/stream/{collection_name}/{file}"
        })

    return render_template("index.html", collection_name=collection_name, files=file_info)

@app.route("/stream/<collection_name>/<path:filename>")
def stream_file(collection_name, filename):
    """
    Stream a specific file from the selected collection.
    """
    collection_path = os.path.join(BASE_DOWNLOADS_DIR, collection_name)
    try:
        return send_from_directory(collection_path, filename)
    except FileNotFoundError:
        return f"File '{filename}' not found in {collection_path}", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
