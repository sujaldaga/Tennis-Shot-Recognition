"""
Batch Process All Tennis Videos
Processes all videos in my_videos/ folder automatically
"""

import subprocess
import os
from pathlib import Path

videos_dir = Path("my_videos")
video_files = sorted([f for f in videos_dir.glob("*.mp4")])

print("="*80)
print("BATCH PROCESSING ALL TENNIS VIDEOS")
print("="*80)
print(f"\nFound {len(video_files)} videos to process:")
for i, video in enumerate(video_files, 1):
    size_mb = video.stat().st_size / (1024*1024)
    print(f"  {i}. {video.name} ({size_mb:.1f} MB)")

print("\n" + "="*80)
print("PROCESSING STARTED")
print("="*80)

python_exe = ".venv/Scripts/python.exe"
model = "tennis_rnn.h5"

for i, video in enumerate(video_files, 1):
    print(f"\n[{i}/{len(video_files)}] Processing {video.name}...")
    
    cmd = [
        python_exe,
        "track_and_classify_with_rnn.py",
        str(video),
        model
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✓ {video.name} completed successfully")
        else:
            print(f"✗ {video.name} failed with code {result.returncode}")
    except Exception as e:
        print(f"✗ Error processing {video.name}: {e}")

print("\n" + "="*80)
print("ALL VIDEOS PROCESSED")
print("="*80)

# Count total frames generated
videos_folder = Path("videos")
if videos_folder.exists():
    total_frames = len(list(videos_folder.glob("image_*.png")))
    print(f"\nTotal frames generated: {total_frames}")
    print(f"Output location: {videos_folder.absolute()}")
