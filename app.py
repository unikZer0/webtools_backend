from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os, zipfile, uuid
from service.video_service import extract_frames
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/video-to-frames-zip")
async def video_to_frames_zip(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())

    # 1. save uploaded video
    video_path = f"{UPLOAD_DIR}/{uid}_{file.filename}"
    with open(video_path, "wb") as f:
        f.write(await file.read())

    # 2. extract frames
    frames_dir = f"{OUTPUT_DIR}/{uid}_frames"
    extract_frames(video_path, frames_dir)

    # 3. zip frames
    zip_path = f"{OUTPUT_DIR}/{uid}_frames.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for img in os.listdir(frames_dir):
            zipf.write(
                os.path.join(frames_dir, img),
                arcname=img
            )

    # 4. expose zip to user (DOWNLOAD)
    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename="frames.zip"
    )
