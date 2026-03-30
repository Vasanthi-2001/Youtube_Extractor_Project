# PERFECT WORKING CODE

import os
import uuid
import yt_dlp
from pydub import AudioSegment

OUTPUT_DIR = "app/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# Convert time to seconds
# -----------------------------
def convert_to_seconds(time_str: str) -> int:
    parts = list(map(int, time_str.strip().split(":")))

    if len(parts) == 1:
        return parts[0]

    elif len(parts) == 2:
        m, s = parts
        return m * 60 + s

    elif len(parts) == 3:
        h, m, s = parts
        return h * 3600 + m * 60 + s

    else:
        raise ValueError("Invalid time format")


# -----------------------------
# Parse multiple ranges
# Example:
# 00:00-00:25,02:35-04:25, 01:24:30-01:24:33
# -----------------------------
def parse_ranges(ranges_str: str):
    ranges = []

    segments = ranges_str.split(",")

    for seg in segments:
        start, end = seg.split("-")
        start_sec = convert_to_seconds(start.strip())
        end_sec = convert_to_seconds(end.strip())

        if start_sec >= end_sec:
            raise ValueError("Start must be less than end")

        ranges.append((start_sec, end_sec))

    return ranges


# -----------------------------
# Download FULL audio first
# -----------------------------
def download_youtube_audio(youtube_url: str):
    base_name = f"yt_{uuid.uuid4().hex}"
    output_template = os.path.join(
        OUTPUT_DIR,
        f"{base_name}.%(ext)s"
    )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        downloaded_file = ydl.prepare_filename(info)

    return os.path.splitext(downloaded_file)[0] + ".wav"


# -----------------------------
# MAIN FUNCTION
# -----------------------------

#Generate audio file from youtube

def generate_audio_from_youtube(
    youtube_url: str,
    ranges_str: str,
    output_format: str
):

    ranges = parse_ranges(ranges_str)

    source_file = download_youtube_audio(youtube_url)

    audio = AudioSegment.from_file(source_file)

    merged_audio = AudioSegment.empty()

    for start_sec, end_sec in ranges:
        clip = audio[start_sec * 1000 : end_sec * 1000]
        merged_audio += clip

    output_filename = f"merged_{uuid.uuid4().hex}.{output_format}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    merged_audio.export(output_path, format=output_format)

    return output_filename



#Generate audio from local file
# -----------------------------
# Generate from Uploaded File
# -----------------------------
def generate_audio_from_file(
    file_path: str,
    ranges_str: str,
    output_format: str
):

    ranges = parse_ranges(ranges_str)

    audio = AudioSegment.from_file(file_path)

    merged_audio = AudioSegment.empty()

    for start_sec, end_sec in ranges:
        clip = audio[start_sec * 1000 : end_sec * 1000]
        merged_audio += clip

    output_filename = f"merged_{uuid.uuid4().hex}.{output_format}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    merged_audio.export(output_path, format=output_format)

    return output_filename