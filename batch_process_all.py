"""
Batch Process All Tennis Videos with Separate Output Folders
Processes all videos and saves results in separate folders
"""

import subprocess
import os
import shutil
from pathlib import Path

videos_dir = Path("my_videos")
outputs_base = Path("videos_results")
video_files = sorted([f for f in videos_dir.glob("*.mp4")])

print("="*80)
print("BATCH PROCESSING ALL TENNIS VIDEOS")
print("="*80)
print(f"\nFound {len(video_files)} videos to process:\n")

for i, video in enumerate(video_files, 1):
    size_mb = video.stat().st_size / (1024*1024)
    print(f"  {i}. {video.name} ({size_mb:.1f} MB)")

python_exe = r".\.venv\Scripts\python.exe"
model = "tennis_rnn.h5"
temp_videos_folder = Path("videos")

print("\n" + "="*80)
print("STARTING PROCESSING...")
print("="*80)

# Create base output directory
outputs_base.mkdir(exist_ok=True)

for i, video in enumerate(video_files, 1):
    video_name = video.stem  # Get filename without extension
    output_folder = outputs_base / video_name
    
    print(f"\n[{i}/{len(video_files)}] Processing: {video.name}")
    print(f"    Output folder: {output_folder}/")
    
    # Remove old output folder if exists
    if temp_videos_folder.exists():
        shutil.rmtree(temp_videos_folder)
    temp_videos_folder.mkdir(exist_ok=True)
    
    # Run processing
    try:
        cmd = f'python track_and_classify_with_rnn.py "{video}" {model}'
        print(f"    Command: {cmd}")
        result = os.system(cmd)
        
        if result == 0:
            # Move generated frames to video-specific folder
            if temp_videos_folder.exists():
                frames = list(temp_videos_folder.glob("image_*.png"))
                if frames:
                    output_folder.mkdir(parents=True, exist_ok=True)
                    for frame in frames:
                        shutil.move(str(frame), str(output_folder / frame.name))
                    print(f"    ✓ {len(frames)} frames saved")
                else:
                    print(f"    ! No frames generated")
            else:
                print(f"    ✗ Output folder not found")
        else:
            print(f"    ✗ Processing failed")
            
    except Exception as e:
        print(f"    ✗ Error: {e}")

print("\n" + "="*80)
print("BATCH PROCESSING COMPLETE")
print("="*80)

# Summary
print("\nGenerated Results:")
for i, video in enumerate(video_files, 1):
    video_name = video.stem
    output_folder = outputs_base / video_name
    if output_folder.exists():
        frame_count = len(list(output_folder.glob("image_*.png")))
        print(f"  {i}. {video_name}: {frame_count} frames → {output_folder}/")
    else:
        print(f"  {i}. {video_name}: NOT PROCESSED")

print(f"\nAll results saved in: {outputs_base.absolute()}/")
