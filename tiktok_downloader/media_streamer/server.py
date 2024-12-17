from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL, Length
import os
import json
import subprocess
import re

app = Flask(__name__)

# Configurations
app.config['SECRET_KEY'] = 'your_secret_key'  # For form security
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB size limit for uploads
BASE_DOWNLOADS_DIR = os.path.join(os.getcwd(), "downloads")

# Ensure the downloads directory exists
if not os.path.exists(BASE_DOWNLOADS_DIR):
    os.makedirs(BASE_DOWNLOADS_DIR)

def list_subfolders(directory):
    """List all subfolders (collections) in the given directory."""
    return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

def load_collection_metadata(collection_name):
    """Load metadata dynamically from the collection's specific JSON file."""
    collection_metadata_path = os.path.join(BASE_DOWNLOADS_DIR, collection_name, f"{collection_name}.json")
    if os.path.exists(collection_metadata_path):
        with open(collection_metadata_path, "r") as f:
            return json.load(f).get("videos", [])
    return []

def extract_video_id_from_url(url):
    """Extract the video ID from a TikTok URL."""
    match = re.search(r'/video/(\d+)', url)
    return match.group(1) if match else None

def extract_video_id_from_filename(filename):
    """Extract video ID (numbers) from a filename."""
    return os.path.splitext(filename)[0]

def run_downloader(url, collection_name):
    """Run yt-dlp to download a video or collection from TikTok."""
    collection_folder = os.path.join(BASE_DOWNLOADS_DIR, collection_name)
    
    # Create collection folder if it doesn't exist
    if not os.path.exists(collection_folder):
        os.makedirs(collection_folder)

    try:
        # Download the collection or video and save it to the collection folder
        subprocess.run(["yt-dlp", "-o", os.path.join(collection_folder, "%(id)s.%(ext)s"), url], check=True)
    except subprocess.CalledProcessError as e:
        flash(f"Error downloading the video or collection: {e}", 'danger')

class DownloadForm(FlaskForm):
    """Form to submit a TikTok URL and collection name for downloading."""
    url = StringField('Enter TikTok Video or Collection URL', validators=[URL(), Length(max=500)])
    collection_name = StringField('Enter Collection Name (Destination Folder)', validators=[Length(max=100)])
    submit = SubmitField('Download')

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Show the form to submit a link and display collections.
    """
    form = DownloadForm()
    if form.validate_on_submit():
        url = form.url.data
        collection_name = form.collection_name.data
        run_downloader(url, collection_name)  # Run downloader to fetch the video or collection
        flash(f"Started downloading {url} into collection: {collection_name}", 'success')
        return redirect(url_for('index'))

    collections = list_subfolders(BASE_DOWNLOADS_DIR)
    return render_template("index.html", form=form, collections=collections)

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
    metadata = load_collection_metadata(collection_name)

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

    return render_template("index.html", collection_name=collection_name, files=file_info, form=None)

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
