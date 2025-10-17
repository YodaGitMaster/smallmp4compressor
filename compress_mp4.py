import os
import subprocess
import sys

def get_duration(input_file):
    """Return duration of video in seconds using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries",
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
        sys.exit(1)

def compress_video(input_file, target_mb):
    """Compress MP4 to target size in MB."""
    duration = get_duration(input_file)
    target_bitrate = (target_mb * 8192) / duration  # MB → Kbps

    # Split between video and audio bitrate
    audio_bitrate = 128  # Kbps
    video_bitrate = max(target_bitrate - audio_bitrate, 100)

    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_compressed_{target_mb}MB.mp4"

    print(f"🎬 Duration: {duration:.2f}s")
    print(f"🎯 Target size: {target_mb} MB")
    print(f"📊 Target bitrate: {target_bitrate:.1f} Kbps")
    print(f"🎥 Video bitrate: {video_bitrate:.1f} Kbps | 🔊 Audio bitrate: {audio_bitrate} Kbps")

    command = [
        "ffmpeg", "-y", "-i", input_file,
        "-vcodec", "libx264", "-b:v", f"{video_bitrate}k",
        "-acodec", "aac", "-b:a", f"{audio_bitrate}k",
        "-movflags", "+faststart",
        "-preset", "medium",
        output_file
    ]

    subprocess.run(command)
    print(f"✅ Compression complete: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compress_mp4.py <input.mp4> <target_size_mb>")
        print("Example: python compress_mp4.py video.mp4 10")
        sys.exit(1)

    input_file = sys.argv[1]
    target_size = float(sys.argv[2])

    if not os.path.isfile(input_file):
        print("❌ Input file not found.")
        sys.exit(1)

    if target_size not in [5, 10, 15, 25]:
        print("⚠️  Allowed target sizes: 5, 10, 15, 25 MB")
        sys.exit(1)

    compress_video(input_file, target_size)
