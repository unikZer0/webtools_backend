import cv2
import os

def extract_frames(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Cannot open video")

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_idx = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % fps == 0:
            cv2.imwrite(
                os.path.join(output_dir, f"frame_{saved:04d}.jpg"),
                frame
            )
            saved += 1

        frame_idx += 1

    cap.release()
    return saved
