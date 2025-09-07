from core.downloader import download_video, extract_audio
from core.audio_analysis import detect_audio_jumpscares
from core.visual_analysis import detect_visual_jumpscares

def format_time(seconds: float) -> str:
    jam = int(seconds // 3600)
    menit = int((seconds % 3600) // 60)
    detik = int(seconds % 60)
    return f"{jam:02d}:{menit:02d}:{detik:02d}"

def filter_close_timestamps(timestamps, min_gap=10.0):
    filtered = []
    last = -min_gap
    for t in sorted(timestamps):
        if t - last >= min_gap:
            filtered.append(t)
            last = t
    return filtered

def main():
    url = input("enter youtube url: ").strip()

    print("dwnloading video...")
    video_path = download_video(url)

    print("extracting audio...")
    audio_path = extract_audio(video_path)

    print("checking audio...")
    audio_timestamps = detect_audio_jumpscares(audio_path)

    print("checking visuals...")
    visual_timestamps = detect_visual_jumpscares(video_path)

    print("\n=== Jumpscares Possibility ===")

    print("\n[Audio]")
    for t in filter_close_timestamps(audio_timestamps, min_gap=10.0):
        print(f"➡ {format_time(t)}")

    print("\n[Visual]")
    for t in filter_close_timestamps(visual_timestamps, min_gap=10.0):
        print(f"➡ {format_time(t)}")

if __name__ == "__main__":
    main()
