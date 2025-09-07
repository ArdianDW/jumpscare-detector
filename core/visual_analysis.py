import cv2
import numpy as np

def detect_visual_jumpscares(video_path: str, threshold: float = 40.0, min_gap: int = 5):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    timestamps = []
    prev_frame = None
    last_detected = -min_gap  

    frame_interval = int(fps) 

    frame_idx = 0
    diff_scores = []

    while True:
        ret = cap.grab()  
        if not ret:
            break

        if frame_idx % frame_interval == 0:
            ret, frame = cap.retrieve()
            if not ret:
                break

            frame = cv2.resize(frame, (320, 240))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if prev_frame is not None:
                diff = cv2.absdiff(gray, prev_frame)
                score = np.mean(diff)
                diff_scores.append(score)

                if len(diff_scores) > 30:
                    avg = np.mean(diff_scores[-30:])
                    std = np.std(diff_scores[-30:])
                    adapt_thresh = avg + 2 * std
                else:
                    adapt_thresh = threshold

                contrast = gray.std()
                prev_contrast = prev_frame.std()
                contrast_change = abs(contrast - prev_contrast)

                if score > adapt_thresh and contrast_change > 10:
                    current_time = frame_idx / fps
                    if current_time - last_detected >= min_gap:
                        timestamps.append(round(current_time, 2)) 
                        last_detected = current_time

            prev_frame = gray

        frame_idx += 1

    cap.release()
    return timestamps
