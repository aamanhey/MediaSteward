import cv2
import os

def extract_frames(video_path, output_folder, frame_rate=1):
    """
    Extracts frames from a video at the specified frame rate.
    """
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    success, frame = cap.read()

    while success:
        if frame_count % frame_rate == 0:
            frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
        success, frame = cap.read()
        frame_count += 1

    cap.release()
    print(f"Frames extracted to: {output_folder}")
