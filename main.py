from core.downloader import download_video, extract_audio
from core.audio_analysis import detect_jumpscares, format_time

def main():
    url = input("enter youtube url: ")

    print("dwnloading video...")
    video_path = download_video(url)

    print("extracting audio...")
    audio_path = extract_audio(video_path)

    print("checking jumpscares...")
    timestamps = detect_jumpscares(audio_path)

    print("\n jumpscare possibility at:")
    for t in timestamps:
        print(f"- {format_time(t)} ({t:.2f} sec)")

if __name__ == "__main__":
    main()
