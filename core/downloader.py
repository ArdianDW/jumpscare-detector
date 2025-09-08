import os
import yt_dlp
import subprocess

def download_video(source: str, output_dir: str = "data/input") -> tuple[str, str]:
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        "format": "bestvideo[ext=mp4][height<=360]+bestaudio[ext=m4a]/best[ext=mp4][height<=360]",
        "ffmpeg_location": r"D:\ffmpeg\bin",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "quiet": True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(source, download=True)
        video_path = ydl.prepare_filename(info)
        video_title = info.get("title", "video")

    return video_path, video_title

def extract_audio(video_path: str, output_dir: str = "data/input") -> str:
    os.makedirs(output_dir, exist_ok=True)
    audio_path = os.path.splitext(os.path.join(output_dir, os.path.basename(video_path)))[0] + ".wav"

    ffmpeg_exe = r"D:\ffmpeg\bin\ffmpeg.exe"

    cmd = [
        ffmpeg_exe,
        "-i", video_path,
        "-vn",                
        "-acodec", "pcm_s16le",
        "-ac", "1",           
        "-ar", "44100",       
        audio_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return audio_path