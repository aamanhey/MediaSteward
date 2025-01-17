import json
import os

def fetch_video_metadata(video_url, yt_info=None, video_id=None):
    """
    Fetch metadata for a TikTok video.
    Args:
        video_url (str): Video URL.
        yt_info (dict): Optional yt-dlp extracted info.

    Returns:
        dict: Metadata dictionary.
    """
    metadata = {
        "url": video_url,
        "title": yt_info.get("title", "No Title") if yt_info else "No Title",
        "alt_title": yt_info.get("alt_title", "Unknown") if yt_info else "Unknown",
        "description": yt_info.get("description", "Unknown") if yt_info else "Unknown",
        "author": yt_info.get("uploader", "Unknown") if yt_info else "Unknown",
        "author_id": yt_info.get("uploader_id", "Unknown") if yt_info else "Unknown",
        "display_id": yt_info.get("display_id", "Unknown") if yt_info else "Unknown",
        "upload_date": yt_info.get("upload_date", "Unknown") if yt_info else "Unknown",
        "duration": yt_info.get("duration", "Unknown") if yt_info else "Unknown",
        "size_mb": round(yt_info.get("filesize", 0) / (1024 * 1024), 2) if yt_info and yt_info.get("filesize") else "Unknown",
        "tags": yt_info.get("tags", []) if yt_info else [],
        "license": yt_info.get("license", "Unknown") if yt_info else "Unknown",
        "collection" : "N/A"
    }
    print(f"Metadata extracted: {metadata}")
    return metadata


def save_metadata_to_json(metadata, output_file="downloads/catalog.json"):
    """
    Save video metadata to a JSON file.
    Args:
        metadata (dict): Video metadata.
        output_file (str): Path to JSON file.
    """
    
    if output_file is None:
        output_file = "downloads/catalog.json"
    elif output_file == " " or output_file == "":
        output_file = "downloads/test.json"
    
    # Convert to absolute path to avoid directory issues
    output_file = os.path.abspath(output_file)
    
    try:
        # Ensure the directory exists
        # os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Initialize or load existing catalog
        if not os.path.exists(output_file):
            catalog = {"videos": []}
        else:
            try:
                with open(output_file, 'r') as f:
                    catalog = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                catalog = {"videos": []}
        
        # Check if metadata already exists to prevent duplicates
        if not any(video['url'] == metadata['url'] for video in catalog['videos']):
            catalog["videos"].append(metadata)
        
        # Save back to the file
        with open(output_file, 'w') as f:
            json.dump(catalog, f, indent=4)
        
        print(f"Metadata saved to {output_file}.")
        return True
    except Exception as e:
        print(f"Error saving metadata: {e}")
        # Print full traceback for more detailed error information
        import traceback
        traceback.print_exc()
        return False