from modules.audio_transcript import transcribe_audio
from modules.frame_extraction import extract_frames
from modules.object_detection import detect_objects_yolo
from modules.text_extraction import extract_text_from_frames
from modules.summarize_tags import summarize_and_tag
from modules.database import save_to_db

# Paths
video_path = "data/test/input_videos/7324798752915492139.mp4"
output_transcript = "data/test/output/transcript.txt"
frame_folder = "data/test/output/frames"
ocr_output = "data/test/output/extracted_text"
db_path = "data/test/output/video_data.db"

# Pipeline
def full_parsing_pipeline(video_file):
    transcript = transcribe_audio(video_file, output_transcript)
    extract_frames(video_file, frame_folder)
    text_data = extract_text_from_frames(frame_folder, ocr_output)
    summary = summarize_and_tag(transcript)
    save_to_db(("test_input_video", transcript, summary), db_path)

full_parsing_pipeline(video_path)