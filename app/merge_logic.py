import os
import uuid
from pydub import AudioSegment

OUTPUT_DIR = "app/outputs"
UPLOAD_DIR = "app/uploads"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------- MERGE AUDIO FILES ----------------
def merge_audio_files(audio_paths: list, output_format: str = "mp3"):
    """
    Merges multiple audio files into one file.
    Supports mp3 or wav output.
    Returns output filename.
    """

    if not audio_paths:
        raise ValueError("No audio files provided for merging")
 
    if output_format not in ("mp3", "wav"):
        raise ValueError("Unsupported output format")

    merged_audio = AudioSegment.empty()

    for path in audio_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        audio = AudioSegment.from_file(path)
        merged_audio += audio

    output_filename = f"merged_{uuid.uuid4().hex}.{output_format}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    merged_audio.export(output_path, format=output_format)

    return output_filename