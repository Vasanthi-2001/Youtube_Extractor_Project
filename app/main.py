
# # PERFECT WORKING CODE FOR AUDIO GENERATOR(MEANS YOUTUBE AUDIO EXTRACTOR) and ALSO FOR NOISE REMOVAL USING DEEPFILTERNET

# from fastapi import FastAPI, Form, UploadFile, File
# from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles

# import os
# import uuid
# import json

# from app.audio_logic import generate_audio_from_youtube
# from app.noise_removal_logic import apply_noise_reduction

# # ---------------- PATHS ----------------
# STATIC_DIR = "app/static"
# UPLOAD_DIR = "app/uploads"
# OUTPUT_DIR = "app/outputs"
# HISTORY_FILE = "app/history.json"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # ---------------- APP ----------------
# app = FastAPI()
# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# # ---------------- HISTORY ----------------
# def load_history():
#     if not os.path.exists(HISTORY_FILE):
#         return {"audio": [], "noise": []}
#     with open(HISTORY_FILE, "r") as f:
#         return json.load(f)


# def save_history(history):
#     with open(HISTORY_FILE, "w") as f:
#         json.dump(history, f, indent=2)


# # ---------------- PAGE RENDER ----------------
# def render_page(content_file: str):
#     with open("app/static/layout.html", encoding="utf-8") as base:
#         layout = base.read()

#     with open(f"app/static/{content_file}", encoding="utf-8") as content:
#         page_content = content.read()

#     return layout.replace("{{CONTENT}}", page_content)


# # ---------------- ROUTES ---------------- 
# @app.get("/")
# def root():
#     return RedirectResponse(url="/audio")


# @app.get("/audio", response_class=HTMLResponse)
# def audio_page():
#     return render_page("audio_index.html")


# @app.get("/noise-removal", response_class=HTMLResponse)
# def noise_page():
#     return render_page("noise_removal.html")


# # ---------------- GENERATE AUDIO ----------------
# @app.post("/generate-audio")
# def generate_audio(
#     youtube_url: str = Form(...),
#     ranges: str = Form(...),
#     output_format: str = Form("mp3")
# ):
#     try:
#         filename = generate_audio_from_youtube(
#             youtube_url,
#             ranges,
#             output_format
#         )

#         history = load_history()
#         history["audio"].append({"filename": filename})
#         save_history(history)

#         return {"status": "success", "filename": filename}

#     except Exception as e:
#         print("ERROR:", e)
#         return {"status": "error", "message": str(e)}


# # ---------------- NOISE REMOVAL ----------------
# @app.post("/noise-remove")
# async def noise_remove(
#     youtube_url: str | None = Form(None),
#     file: UploadFile | None = File(None),
#     output_format: str = Form("wav")
# ):
#     try:
#         # Validate format (noise removal only supports mp3 or wav)
#         if output_format not in ("mp3", "wav"):
#             raise ValueError("Unsupported output format")

#         if youtube_url:
#             # Download full WAV for noise removal
#             src_filename = generate_audio_from_youtube(
#                 youtube_url,
#                 "0:00-99999",
#                 "wav"
#             )
#             src = os.path.join(OUTPUT_DIR, src_filename)

#         else:
#             if not file:
#                 raise ValueError("No file provided")

#             # Save uploaded file safely with UUID
#             ext = os.path.splitext(file.filename)[1]
#             src = os.path.join(
#                 UPLOAD_DIR,
#                 f"{uuid.uuid4().hex}{ext}"
#             )

#             with open(src, "wb") as f:
#                 f.write(await file.read())

#         # Apply noise reduction
#         filename = apply_noise_reduction(src, output_format)

#         # Cleanup source file (important)
#         if os.path.exists(src):
#             os.remove(src)

#         history = load_history()
#         history["noise"].append({"filename": filename})
#         save_history(history)

#         return {"status": "success", "filename": filename}

#     except Exception as e:
#         return {"status": "error", "message": str(e)}
        

# # ---------------- HISTORY ----------------
# @app.get("/history/{mode}")
# def get_history(mode: str):
#     return load_history().get(mode, [])


# # ---------------- DOWNLOAD ----------------
# @app.get("/download/{filename}")
# def download(filename: str):

#     path = os.path.join(OUTPUT_DIR, filename)

#     if not os.path.exists(path):
#         return {"status": "error", "message": "File not found"}

#     media_type = "audio/mpeg" if filename.endswith(".mp3") else "audio/wav"

#     return FileResponse(path, media_type=media_type, filename=filename)





















# PERFECT WORKING CODE FOR AUDIO GENERATOR(MEANS YOUTUBE AUDIO EXTRACTOR) , ALSO FOR NOISE REMOVAL USING DEEPFILTERNET AND also for MERGE AUDIO

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from typing import List


import os
import uuid
import json

from app.audio_logic import generate_audio_from_youtube
from app.noise_removal_logic import apply_noise_reduction
from app.merge_logic import merge_audio_files
from app.type_converter_logic import convert_audio_type
from app.audio_padding_logic import extend_audio_duration



# ---------------- PATHS ----------------
STATIC_DIR = "app/static"
UPLOAD_DIR = "app/uploads"
OUTPUT_DIR = "app/outputs"
HISTORY_FILE = "app/history.json"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- APP ----------------
app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ---------------- HISTORY ----------------
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {"audio": [], "noise": [], "merge": [], "convert": [], "type_converter":[], "extend":[]}
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


# ---------------- PAGE RENDER ----------------
def render_page(content_file: str):
    with open("app/static/layout.html", encoding="utf-8") as base:
        layout = base.read()

    with open(f"app/static/{content_file}", encoding="utf-8") as content:
        page_content = content.read()

    return layout.replace("{{CONTENT}}", page_content)


# ---------------- ROUTES ---------------- 
@app.get("/")
def root():
    return RedirectResponse(url="/audio")


@app.get("/audio", response_class=HTMLResponse)
def audio_page():
    return render_page("audio_index.html")


@app.get("/noise-removal", response_class=HTMLResponse)
def noise_page():
    return render_page("noise_removal.html")


@app.get("/merge", response_class=HTMLResponse)
def merge_page():
    return render_page("merge.html")


@app.get("/type-converter", response_class=HTMLResponse)
def type_converter_page():
    return render_page("type_converter.html")


@app.get("/extend-audio", response_class=HTMLResponse)
def extend_audio_page():
    return render_page("audio_padding.html")


# ---------------- GENERATE AUDIO ----------------
@app.post("/generate-audio")
def generate_audio(
    youtube_url: str = Form(...),
    ranges: str = Form(...),
    output_format: str = Form("mp3")
):
    try:
        filename = generate_audio_from_youtube(
            youtube_url,
            ranges,
            output_format
        )

        history = load_history()
        history["audio"].append({"filename": filename})
        save_history(history)

        return {"status": "success", "filename": filename}

    except Exception as e:
        print("ERROR:", e)
        return {"status": "error", "message": str(e)}



#---------------- upload audio ----------------
@app.post("/upload-audio")
async def upload_audio(
    file: UploadFile = File(...),
    ranges: str = Form(...),
    output_format: str = Form("mp3")
):
    try:
        # Save uploaded file temporarily
        ext = os.path.splitext(file.filename)[1]
        temp_path = os.path.join(
            UPLOAD_DIR,
            f"{uuid.uuid4().hex}{ext}"
        )

        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Generate clipped audio
        from app.audio_logic import generate_audio_from_file

        filename = generate_audio_from_file(
            temp_path,
            ranges,
            output_format
        )

        # Delete temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

        history = load_history()
        history["audio"].append({"filename": filename})
        save_history(history)

        return {"status": "success", "filename": filename}

    except Exception as e:
        return {"status": "error", "message": str(e)}





# ---------------- NOISE REMOVAL ----------------
@app.post("/noise-remove")
async def noise_remove(
    youtube_url: str | None = Form(None),
    file: UploadFile | None = File(None),
    output_format: str = Form("wav")
):
    try:
        # Validate format (noise removal only supports mp3 or wav)
        if output_format not in ("mp3", "wav"):
            raise ValueError("Unsupported output format")

        if youtube_url:
            # Download full WAV for noise removal
            src_filename = generate_audio_from_youtube(
                youtube_url,
                "0:00-99999",
                "wav"
            )
            src = os.path.join(OUTPUT_DIR, src_filename)

        else:
            if not file:
                raise ValueError("No file provided")

            # Save uploaded file safely with UUID
            ext = os.path.splitext(file.filename)[1]
            src = os.path.join(
                UPLOAD_DIR,
                f"{uuid.uuid4().hex}{ext}"
            )

            with open(src, "wb") as f:
                f.write(await file.read())

        # Apply noise reduction
        filename = apply_noise_reduction(src, output_format)

        # Cleanup source file (important)
        if os.path.exists(src):
            os.remove(src)

        history = load_history()
        history["noise"].append({"filename": filename})
        save_history(history)

        return {"status": "success", "filename": filename}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    




# ---------------- MERGE AUDIO ----------------

@app.post("/merge-audio")
async def merge_audio(
    files: List[UploadFile] = File(...),
    output_format: str = Form("mp3")
):
    try:
        if len(files) < 2:
            return {
                "status": "error",
                "message": "Please upload at least 2 audio files"
            }

        audio_paths = []

        # Save uploaded files
        for file in files:
            ext = os.path.splitext(file.filename)[1]
            temp_path = os.path.join(
                UPLOAD_DIR,
                f"{uuid.uuid4().hex}{ext}"
            )

            with open(temp_path, "wb") as f:
                f.write(await file.read())

            audio_paths.append(temp_path)

        # Merge
        output_filename = merge_audio_files(audio_paths, output_format)

        # Cleanup uploaded temp files
        for path in audio_paths:
            if os.path.exists(path):
                os.remove(path)

        # Save history
        history = load_history()
        if "merge" not in history:
            history["merge"] = []

        history["merge"].append({"filename": output_filename})
        save_history(history)

        return {
            "status": "success",
            "filename": output_filename
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }



# -------------- Type converter ----------
@app.post("/convert-type")
async def convert_type(
    file: UploadFile = File(...),
    output_format: str = Form(...)
):
    try:
        import uuid
        import os

        ext = os.path.splitext(file.filename)[1]
        temp_path = os.path.join(
            UPLOAD_DIR,
            f"{uuid.uuid4().hex}{ext}"
        )

        with open(temp_path, "wb") as f:
            f.write(await file.read())

        filename = convert_audio_type(
            temp_path,
            output_format
        )

        if os.path.exists(temp_path):
            os.remove(temp_path)

        history = load_history()
        history["type_converter"].append({"filename": filename})
        save_history(history)

        return {"status": "success", "filename": filename}

    except Exception as e:
        return {"status": "error", "message": str(e)}



# ---------------- EXTERND AUDIO ----------------
@app.post("/extend-audio")
async def extend_audio(
    file: UploadFile = File(...),
    target_seconds: int = Form(...)
):
    try:

        ext = os.path.splitext(file.filename)[1]

        temp_path = os.path.join(
            UPLOAD_DIR,
            f"{uuid.uuid4().hex}{ext}"
        )

        with open(temp_path, "wb") as f:
            f.write(await file.read())

        filename = extend_audio_duration(
            temp_path,
            target_seconds
        )

        if os.path.exists(temp_path):
            os.remove(temp_path)

        history = load_history()

        if "extend" not in history:
            history["extend"] = []

        history["extend"].append({"filename": filename})

        save_history(history)

        return {"status": "success", "filename": filename}

    except Exception as e:
        return {"status": "error", "message": str(e)}



# ---------------- HISTORY ----------------
@app.get("/history/{mode}")
def get_history(mode: str):
    return load_history().get(mode, [])


# ---------------- DOWNLOAD ----------------
@app.get("/download/{filename}")
def download(filename: str):

    path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(path):
        return {"status": "error", "message": "File not found"}

    media_type = "audio/mpeg" if filename.endswith(".mp3") else "audio/wav"

    return FileResponse(path, media_type=media_type, filename=filename)




# ----------------- Delete button -------------
@app.delete("/delete/{filename}")
def delete_file(filename: str):

    path = os.path.join(OUTPUT_DIR, filename)

    # Delete file if exists
    if os.path.exists(path):
        os.remove(path)

    # Remove from history
    history = load_history()

    for mode in history:
        history[mode] = [
            item for item in history[mode]
            if item["filename"] != filename
        ]

    save_history(history)

    return {"status": "success"}