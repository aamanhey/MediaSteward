import os

def get_file_size(filepath):
    """
    Get the size of a file in MB.
    Args:
        filepath (str): Path to the file.

    Returns:
        float: File size in MB.
    """
    if os.path.exists(filepath):
        return os.path.getsize(filepath) / (1024 * 1024)
    return 0

collections = {
    "los angeles" : "https://www.tiktok.com/@adrianmanhey/collection/Los%20Angeles-7327482342845483819",
    "clips" : "https://www.tiktok.com/@adrianmanhey/collection/Clips-7350903529052425006",
    "up" : "https://www.tiktok.com/@adrianmanhey/collection/UP-7287386486037662507",
    "brain" : "https://www.tiktok.com/@adrianmanhey/collection/Brain-7247113726611180334"
}