from core.downloader import download_video, extract_audio

def main ():
    source = input("enter youtube url or local file path: ")

    video_path = download_video(source)
    print(f"Video downloaded to: {video_path}")

    audio_path = extract_audio(video_path)
    print(f"Audio extracted to: {audio_path}")

if __name__ == "__main__":
    main()