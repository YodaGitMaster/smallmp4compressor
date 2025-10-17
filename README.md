# 🎬 MP4 Compressor

A simple Python script to compress MP4 videos to target sizes of **5, 10, 15, or 25 MB** using FFmpeg.

---

## 🚀 Features
- Auto bitrate calculation based on target size  
- Preserves decent audio quality (AAC 128 kbps)  
- Outputs new file with `_compressed_<SIZE>MB` suffix  
- Works on macOS, Windows, and Linux  

---

## 🧩 Requirements
- Python 3.8+
- FFmpeg installed and available in system PATH

Install Python dependencies:
```bash
pip install -r requirements.txt
```

## How to use it
```bash
python compress_mp4.py "myvideo.mp4" 10
```

## ⚙️ Step 1 — Download FFmpeg portable build

Go to the official Windows builds site:
```
🔗 https://www.gyan.dev/ffmpeg/builds/
```

Under “Release builds”, download:
```
ffmpeg-release-essentials.zip
```

Extract the archive (right-click → Extract All…).
You’ll get a folder like:
```
ffmpeg-2025-xx-xx-git-essentials_build\
    └── bin\
        ├── ffmpeg.exe
        ├── ffprobe.exe
        └── ...
```

Copy those two executables into your project’s bin/ folder:
```
smallmp4compressor/bin/ffmpeg.exe
smallmp4compressor/bin/ffprobe.exe
```
