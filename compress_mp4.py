import os
import subprocess
import sys

def get_ffmpeg_paths():
    """Locate ffmpeg and ffprobe in local bin folder or system PATH."""
    here = os.path.dirname(os.path.abspath(__file__))
    local_bin = os.path.join(here, "bin")

    ffmpeg_path = os.path.join(local_bin, "ffmpeg.exe")
    ffprobe_path = os.path.join(local_bin, "ffprobe.exe")

    if not os.path.isfile(ffmpeg_path) or not os.path.isfile(ffprobe_path):
        # fallback to system PATH
        ffmpeg_path = "ffmpeg"
        ffprobe_path = "ffprobe"

    return ffmpeg_path, ffprobe_path


def get_duration(input_file, ffprobe_path):
    """Return duration of video in seconds using ffprobe."""
    result = subprocess.run(
        [
            ffprobe_path, "-v", "error", "-show_entries",
            "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", input_file
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        print("❌ Could not determine duration.")
        print(result.stderr)
        sys.exit(1)


def compress_video(input_file, target_mb, ffmpeg_path, ffprobe_path):
    """Compress MP4 to target size in MB."""
    duration = get_duration(input_file, ffprobe_path)
    target_bitrate = (target_mb * 8192) / duration  # MB → Kbps

    audio_bitrate = 128  # Kbps
    video_bitrate = max(target_bitrate - audio_bitrate, 100)

    base, _ = os.path.splitext(input_file)
    output_file = f"{base}_compressed_{int(target_mb)}MB.mp4"

    print(f"🎬 Duration: {duration:.2f}s")
    print(f"🎯 Target: {target_mb} MB")
    print(f"📊 Target bitrate: {target_bitrate:.1f} Kbps")
    print(f"🎥 Video bitrate: {video_bitrate:.1f} Kbps | 🔊 Audio: {audio_bitrate} Kbps")

    command = [
        ffmpeg_path, "-y", "-i", input_file,
        "-vcodec", "libx264", "-b:v", f"{video_bitrate}k",
        "-acodec", "aac", "-b:a", f"{audio_bitrate}k",
        "-movflags", "+faststart",
        "-preset", "medium",
        output_file
    ]

    subprocess.run(command)
    print(f"✅ Done: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compress_mp4.py <input.mp4> <target_size_mb>")
        sys.exit(1)

    input_file = sys.argv[1]
    target_size = float(sys.argv[2])

    if not os.path.isfile(input_file):
        print("❌ Input file not found.")
        sys.exit(1)

    if target_size not in [5, 10, 15, 25]:
        print("⚠️ Allowed targets: 5, 10, 15, 25 MB")
        sys.exit(1)

    ffmpeg_path, ffprobe_path = get_ffmpeg_paths()
    compress_video(input_file, target_size, ffmpeg_path, ffprobe_path)
