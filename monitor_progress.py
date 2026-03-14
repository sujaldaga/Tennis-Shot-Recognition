"""
Real-time monitoring of batch video processing
Shows progress of all videos
"""

from pathlib import Path
import time
import sys

def get_status():
    """Get current processing status"""
    videos_results = Path("videos_results")
    videos_temp = Path("videos")
    
    completed = {}
    if videos_results.exists():
        for video_folder in videos_results.iterdir():
            if video_folder.is_dir():
                frame_count = len(list(video_folder.glob("*.png")))
                if frame_count > 0:
                    size_mb = sum(f.stat().st_size for f in video_folder.glob("*.png")) / (1024*1024)
                    completed[video_folder.name] = (frame_count, size_mb)
    
    # Current video being processed
    current = 0
    if videos_temp.exists():
        current = len(list(videos_temp.glob("*.png")))
    
    return completed, current

print("="*80)
print("BATCH VIDEO PROCESSING - REAL-TIME MONITOR")
print("="*80)

# List all videos to process
my_videos = sorted(Path("my_videos").glob("*.mp4"))
print(f"\nTotal videos to process: {len(my_videos)}")
for i, v in enumerate(my_videos, 1):
    print(f"  {i}. {v.name}")

print("\n" + "="*80)
print("MONITORING... (Press Ctrl+C to exit)")
print("="*80)

try:
    iteration = 0
    while True:
        iteration += 1
        completed, current = get_status()
        
        print(f"\n[Iteration {iteration}] Progress Update:")
        print(f"  Completed videos: {len(completed)}")
        print(f"  Current video: {current} frames")
        
        if completed:
            total_frames = sum(c[0] for c in completed.values())
            total_size = sum(c[1] for c in completed.values())
            print(f"\n  Completed:")
            for video_name in sorted(completed.keys()):
                frames, size_mb = completed[video_name]
                print(f"    ✓ {video_name}: {frames} frames ({size_mb:.1f} MB)")
            print(f"\n  Total: {total_frames} frames ({total_size:.1f} MB)")
        
        if len(completed) == len(my_videos):
            print("\n" + "="*80)
            print("✓ ALL VIDEOS PROCESSED SUCCESSFULLY!")
            print("="*80)
            break
        
        time.sleep(15)  # Update every 15 seconds
        
except KeyboardInterrupt:
    print("\n\nMonitoring stopped.")
    completed, current = get_status()
    if completed:
        print(f"\nProgress so far: {len(completed)} videos completed")

print("\n" + "="*80)
print("Results saved in: videos_results/")
print("="*80)
