import os
import uuid
from pydub import AudioSegment

OUTPUT_DIR = "app/outputs"

def extend_audio_duration(input_path: str, extra_seconds: int):

    audio = AudioSegment.from_file(input_path)

    # current duration
    current_ms = len(audio)

    # exact target duration
    target_ms = current_ms + (extra_seconds * 1000)

    # create silence long enough
    silence = AudioSegment.silent(duration=extra_seconds * 1000)

    # combine 
    padded_audio = audio + silence

    # trim or extend EXACTLY to target
    padded_audio = padded_audio[:target_ms]

    filename = f"extended_{uuid.uuid4().hex}.wav"
    output_path = os.path.join(OUTPUT_DIR, filename)

    padded_audio.export(output_path, format="wav")

    return filename