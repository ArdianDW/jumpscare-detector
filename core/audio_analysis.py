import librosa
import numpy as np

def format_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def detect_jumpscares(audio_path: str, sr: int = 22050) -> list[str]:
    y, sr = librosa.load(audio_path, sr=sr)

    hop_length = 512
    frame_length = 1024
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]

    stft = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop_length))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
    bass_band = (freqs >= 20) & (freqs <= 200)
    bass_energy = stft[bass_band].mean(axis=0)

    rms = (rms - rms.min()) / (rms.max() - rms.min() + 1e-9)
    bass_energy = (bass_energy - bass_energy.min()) / (bass_energy.max() - bass_energy.min() + 1e-9)

    rms_diff = np.diff(rms, prepend=rms[0])
    bass_diff = np.diff(bass_energy, prepend=bass_energy[0])

    jumpscare_times = []
    cooldown = 8.0
    last_detect = -cooldown

    for i in range(len(rms)):
        time = librosa.frames_to_time(i, sr=sr, hop_length=hop_length)
        if rms_diff[i] > 0.25 and bass_diff[i] > 0.15:
            if time - last_detect >= cooldown:
                jumpscare_times.append(time)
                last_detect = time

    return jumpscare_times
