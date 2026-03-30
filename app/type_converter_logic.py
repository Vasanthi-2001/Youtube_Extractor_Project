import os
import uuid
from pydub import AudioSegment

OUTPUT_DIR = "app/outputs"

SUPPORTED_FORMATS = [
    "mp3",
    "wav",
    "ogg"
]

def convert_audio_type(input_path: str, output_format: str):

    if output_format not in SUPPORTED_FORMATS:
        raise ValueError("Unsupported format selected.")

    # 🔥 ensure outputs folder exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        audio = AudioSegment.from_file(input_path)
    except Exception:
        raise ValueError("Unsupported or corrupted input audio file.")

    output_filename = f"converted_{uuid.uuid4().hex}.{output_format}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    audio.export(output_path, format=output_format)

    return output_filename