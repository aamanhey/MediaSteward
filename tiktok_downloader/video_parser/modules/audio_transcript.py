import whisper

def transcribe_audio(video_path, output_path):
    """
    Extracts and transcribes audio from a video file.
    """
    print("Loading Whisper model...")
    model = whisper.load_model("base")

    print("Transcribing audio...")
    result = model.transcribe(video_path)

    # Save transcript
    with open(output_path, "w") as f:
        f.write(result["text"])

    print(f"Transcript saved at: {output_path}")
    return result["text"]
