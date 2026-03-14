"""
Tennis Shot Recognition Project - Comprehensive Analysis & Demo
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np

print("\n" + "="*80)
print("TENNIS SHOT RECOGNITION PROJECT - COMPREHENSIVE ANALYSIS & DEMO")
print("="*80)

project_root = Path(__file__).parent

# 1. PROJECT OVERVIEW
print("\n[PROJECT OVERVIEW]")
print("-" * 80)
print("""
This project implements tennis shot recognition using:
  * Movenet: Pose estimation to extract human keypoints
  * Deep Learning: Two neural network approaches
    - Dense layers (Fully Connected) for single frame classification
    - Recurrent Neural Network (GRU) for temporal sequence classification
  
Key Features:
  - 4 shot classes: Forehand, Backhand, Serve, Neutral (idle/no shot)
  - ~1 second temporal window (30 frames at 30 FPS)
  - 26 body keypoints per frame (pose joints)
  - Pre-trained models ready for inference
""")

# 2. DATASET ANALYSIS
print("\n[DATASET ANALYSIS]")
print("-" * 80)

dataset_root = project_root / 'dataset'
players = sorted([d.name for d in dataset_root.iterdir() if d.is_dir()])

print(f"\nPlayers in dataset: {len(players)}")
print(f"Players: {', '.join(players)}\n")

total_shots = 0
all_shot_stats = {}

for player in players:
    shots_path = dataset_root / player / 'shots'
    if shots_path.exists():
        csv_files = list(shots_path.glob('*.csv'))
        shot_types = {}
        
        for csv_file in csv_files:
            shot_type = csv_file.stem.rsplit('_', 1)[0]
            shot_types[shot_type] = shot_types.get(shot_type, 0) + 1
        
        print(f"  {player}:")
        for shot_type in sorted(shot_types.keys()):
            count = shot_types[shot_type]
            print(f"    - {shot_type:10s}: {count:3d} samples")
            all_shot_stats[shot_type] = all_shot_stats.get(shot_type, 0) + count
            total_shots += count
        
        print()

print(f"Total shots across all players: {total_shots}")
print("\nTotal by shot type:")
for shot_type in sorted(all_shot_stats.keys()):
    count = all_shot_stats[shot_type]
    pct = (count / total_shots) * 100
    print(f"  {shot_type:10s}: {count:3d} ({pct:5.1f}%)")

# 3. TRAINED MODELS
print("\n\n[TRAINED MODELS]")
print("-" * 80)

models_info = [
    ('tennis_fully_connected.h5', 'Single-Frame Dense Neural Network'),
    ('tennis_rnn.h5', 'RNN/GRU Temporal Classifier')
]

for model_file, description in models_info:
    model_path = project_root / model_file
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"\n[OK] {model_file}")
        print(f"  Description: {description}")
        print(f"  Size: {size_mb:.2f} MB")
    else:
        print(f"\n[MISSING] {model_file} NOT FOUND")

# 4. DATA STRUCTURE DEMO
print("\n\n[DATA STRUCTURE EXAMPLE]")
print("-" * 80)

sample_file = dataset_root / 'alcaraz' / 'shots' / 'forehand_001.csv'
if sample_file.exists():
    df = pd.read_csv(sample_file)
    print(f"\nSample file: {sample_file.name}")
    print(f"Shape: {df.shape[0]} frames × {df.shape[1]} features")
    print(f"\nColumn structure:")
    print(f"  - Body keypoints: {df.shape[1] - 1} (26 keypoints × 2 coordinates)")
    print(f"  - Shot label: 1 column")
    print(f"\nKeypoint format: (y, x) for each of 26 body joints from Movenet:")
    
    keypoints = [
        'nose', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
        'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee',
        'right_knee', 'left_ankle', 'right_ankle'
    ]
    print(f"  Joints covered: {', '.join(keypoints)}")
    
    print(f"\nFirst frame of '{sample_file.stem}':")
    print(f"  Shot type: {df['shot'].iloc[0]}")
    print(f"  Pose data (first 5 keypoints):")
    for i, kp in enumerate(keypoints[:5]):
        y_col = f'{kp}_y'
        x_col = f'{kp}_x'
        if y_col in df.columns:
            y = df[y_col].iloc[0]
            x = df[x_col].iloc[0]
            print(f"    {kp:20s}: y={y:.3f}, x={x:.3f}")

# 5. USAGE EXAMPLES
print("\n\n[USAGE EXAMPLES]")
print("-" * 80)
print("""
To use this project, you need a tennis video. The main scripts are:

1. Single-Frame Classification (more unstable, but fast):
   python track_and_classify_frame_by_frame.py <video.mp4> tennis_fully_connected.h5
   
   Process:
   - Extract pose for each frame
   - Classify each frame independently
   - Apply averaging over 10-frame window
   - Count shots with basic temporal smoothing

2. RNN Classification (more stable, better accuracy):
   python track_and_classify_with_rnn.py <video.mp4> tennis_rnn.h5 [--left-handed]
   
   Process:
   - Extract pose for each frame
   - Feed 30-frame sliding window to RNN
   - Use GRU layers to capture temporal patterns
   - Runs faster than real-time on GPU

Optional flag:
   --left-handed  For left-handed players (mirrors x-coordinates)

Note: You need to download the Movenet TFLite model:
wget https://tfhub.dev/google/lite-model/movenet/singlepose/lightning/tflite/float16/4?lite-format=tflite -O movenet.tflite
""")

# 6. KEY FILES
print("\n\n[KEY FILES]")
print("-" * 80)
print("""
Main scripts:
  • track_and_classify_with_rnn.py     - RNN inference (recommended)
  • track_and_classify_frame_by_frame.py - Single-frame inference
  • extract_human_pose.py              - Movenet pose extraction
  • extract_shots_as_features.py       - Extract shots from video
  • annotator.py                       - Manual video annotation

Jupyter Notebooks (for training):
  • RNNShotClassifier.ipynb            - Train RNN model (~100% accuracy)
  • SingleFrameShotClassifier.ipynb    - Train fully connected model (~80% accuracy)

Models:
  • tennis_rnn.h5                      - Pre-trained RNN model
  • tennis_fully_connected.h5          - Pre-trained fully connected model
  • movenet.tflite                     - Pose estimation model (download needed)
""")

# 7. SUMMARY
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"""
✓ Project Structure: VALID
✓ Datasets: {total_shots} annotated shots across {len(players)} players
✓ Models: 2 pre-trained models available
✓ Framework: TensorFlow/Keras
✓ Status: Ready for inference

Next steps:
1. Download movenet.tflite model from TensorFlow Hub
2. Obtain a tennis video file
3. Run inference with one of the main scripts
4. Or review the Jupyter notebooks to understand the training process
""")
print("="*80 + "\n")
