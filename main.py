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

    print("downloading video...")
    video_path, video_title = download_video(url)

    print("extracting audio...")
    audio_path = extract_audio(video_path)

    print("checking audio...")
    audio_timestamps = detect_audio_jumpscares(audio_path)

    print("checking visuals (as confirmation)...")
    visual_timestamps = detect_visual_jumpscares(video_path, audio_timestamps)

    output_lines = []
    output_lines.append("=== Jumpscares Possibility ===\n")

    output_lines.append("[Audio]")
    for t in filter_close_timestamps(audio_timestamps, min_gap=10.0):
        output_lines.append(f"➡ {format_time(t)}")
    output_lines.append("")

    output_lines.append("[Audio + Visual confirmed]")
    for t in filter_close_timestamps(visual_timestamps, min_gap=10.0):
        output_lines.append(f"➡ {format_time(t)}")

    print("\n".join(output_lines))

    import os
    os.makedirs("data/output", exist_ok=True)
    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in video_title)
    filename = os.path.join("data/output", f"jumpscare {safe_title}.txt")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"\nresult : {filename}")

if __name__ == "__main__":
    main()
