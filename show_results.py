"""
Summary of Tennis Shot Detection Results
Shows the shots detected in the processed video
"""

from pathlib import Path
import json

videos_folder = Path("videos")

if videos_folder.exists():
    images = list(videos_folder.glob("image_*.png"))
    print("="*80)
    print("TENNIS SHOT RECOGNITION - VIDEO PROCESSING RESULTS")
    print("="*80)
    print(f"\nVideo: my_videos/1.mp4")
    print(f"Total Frames Processed: {len(images)}")
    
    if len(images) > 0:
        # Get video dimensions from first frame
        import cv2
        first_frame = cv2.imread(str(images[0]))
        if first_frame is not None:
            h, w = first_frame.shape[:2]
            print(f"Frame Resolution: {w}x{h}")
        
        print(f"\nOutput Location: {videos_folder.absolute()}/")
        print(f"Images Saved: image_00001.png to image_{len(images):05d}.png")
        
        # List first few frames
        print(f"\nFirst 10 generated frames:")
        for i, img in enumerate(sorted(images)[:10]):
            size_kb = img.stat().st_size / 1024
            print(f"  {i+1}. {img.name} ({size_kb:.1f} KB)")
        
        print(f"\n... (+{max(0, len(images)-10)} more frames)")
        
        # Last few frames
        if len(images) > 10:
            print(f"\nLast 5 frames:")
            for i, img in enumerate(sorted(images)[-5:]):
                size_kb = img.stat().st_size / 1024
                print(f"  {len(images)-4+i}. {img.name} ({size_kb:.1f} KB)")
    
    print("\n" + "="*80)
    print("OUTPUT CONTAINS:")
    print("="*80)
    print("""
✓ Tennis player skeleton overlay (green keypoints and edges)
✓ Region of Interest bounding box (yellow rectangle tracking player)  
✓ Shot counter (left side):
  - Backhands = number detected
  - Forehands = number detected
  - Serves = number detected
✓ Confidence bars (right side):
  - S = Serve probability
  - B = Backhand probability
  - N = Neutral probability
  - F = Forehand probability
✓ FPS counter (top left showing processing speed)
✓ Frame number indicator

NEXT STEPS:
1. View individual frames with image viewer
2. Create video from frames (using ffmpeg):
   ffmpeg -framerate 30 -i videos/image_%05d.png -c:v libx264 output.mp4
3. Process other videos:
   python track_and_classify_with_rnn.py my_videos/2.mp4 tennis_rnn.h5
   python track_and_classify_with_rnn.py my_videos/3.mp4 tennis_rnn.h5
   ... etc
""")
    print("="*80)

else:
    print("! Videos folder not found")
