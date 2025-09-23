import os
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

def process_link(url: str):
	print(f"Processing: {url}")
	try:
		video_path, video_title = download_video(url)
		print("  Extracting audio...")
		audio_path = extract_audio(video_path)
		print("  Checking audio...")
		audio_timestamps = detect_audio_jumpscares(audio_path)
		print("  Checking visuals...")
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

		os.makedirs("data/output", exist_ok=True)
		safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in video_title)
		filename = os.path.join("data/output", f"jumpscare {safe_title}.txt")
		with open(filename, "w", encoding="utf-8") as f:
			f.write("\n".join(output_lines))
		print(f"  Result saved: {filename}")

		try:
			os.remove(video_path)
			os.remove(audio_path)
			print("  Video and audio deleted.")
		except Exception as e:
			print(f"  Cleanup failed: {e}")
	except Exception as e:
		print(f"  Error processing {url}: {e}")

def main():
	links_file = "data/input/links.txt"
	if not os.path.exists(links_file):
		print(f"Links file not found: {links_file}")
		return
	with open(links_file, "r", encoding="utf-8") as f:
		links = [line.strip() for line in f if line.strip()]
	if not links:
		print("No links found in links.txt.")
		return
	for url in links:
		process_link(url)

if __name__ == "__main__":
	main()
