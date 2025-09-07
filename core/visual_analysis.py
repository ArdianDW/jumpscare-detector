import cv2
import numpy as np

def detect_visual_jumpscares(video_path: str, audio_timestamps: list[float], window: float = 1.5):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    confirmed = []

    for ts in audio_timestamps:
        start_frame = max(0, int((ts - window) * fps))
        end_frame = min(total_frames, int((ts + window) * fps))

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        prev_gray = None
        detected = False

        for f in range(start_frame, end_frame, int(fps // 2) or 1): 
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if prev_gray is not None:
                brightness_change = abs(gray.mean() - prev_gray.mean())
                if brightness_change > 20: 
                    detected = True
                    break
            prev_gray = gray

        if detected:
            confirmed.append(ts)
        else:
            confirmed.append(ts)
    cap.release()
    return confirmed
