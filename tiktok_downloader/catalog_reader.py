import os
import json
from tabulate import tabulate

def read_catalogue(catalogue_folder="downloads", filename="catalog/catalog.json"):
    """
    Read metadata files from the catalogue folder and display as a table.
    
    Args:
        catalogue_folder (str): Path to the folder containing metadata JSON files
    """
    # filename = "catalog.json"
    if filename is None:
        filename = "catalog/catalog.json"
    elif filename == " " or filename == "":
        filename = "test/test.json"

    # Iterate through all JSON files in the folder
    filepath = os.path.join(catalogue_folder, filename)
    print("Filepath ", filepath)

    # Check if the catalogue folder exists
    if not os.path.exists(filepath):
        print(f"Catalogue folder {filepath} does not exist.")
        return

    # Collect metadata from all JSON files
    metadata_entries = []
    
    # Iterate through all JSON files in the folder
    filepath = os.path.join(catalogue_folder, filename)
    # print("Filepath ", filepath)

    totals = {
        "size" : 0,
        "count" : 0
    } 
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            meta_file = json.load(f)

            for metadata in meta_file["videos"]:
            
                # Extract key information for the table
                entry = {
                    'Video ID (URL)': metadata.get('url', 'N/A'),
                    'Creator': metadata.get('author', 'N/A'),
                    'Upload Date': metadata.get('upload_date', 'N/A'),
                    'Duration': f"{metadata.get('duration', 0):.2f} sec" if metadata.get('duration') else 'N/A',
                    'Size' : metadata.get('size_mb'),
                    'Tags' : metadata.get('tags'),
                    'Title': metadata.get('title', 'N/A')[:100] + ('...' if len(metadata.get('title', '')) > 100 else ''),
                }

                totals["size"] += metadata.get('size_mb')
                totals["count"] += 1
                
                metadata_entries.append(entry)
    
    except json.JSONDecodeError:
        print(f"Error reading metadata file: {filename}")
    except Exception as e:
        print(f"Unexpected error processing {filename}: {e}")
    
    # Print the table
    if metadata_entries:
        print(tabulate(metadata_entries, headers='keys', tablefmt='pretty'))
        print(f"\nTotal videos in catalogue: {len(metadata_entries)}")
        print(f"Total size of videos in catalogue: {totals["size"]} MB")
    else:
        print("No metadata files found in the catalogue.")

if __name__ == "__main__":
    read_catalogue()