#!/usr/bin/env python
"""
Analysis and test script for Tennis Shot Recognition project
"""

import os
import sys
from pathlib import Path

print("=" * 70)
print("TENNIS SHOT RECOGNITION PROJECT - ANALYSIS AND TEST")
print("=" * 70)

# Check project structure
print("\n1. PROJECT STRUCTURE:")
project_root = Path(__file__).parent

print("\n   Main Scripts:")
scripts = [
    'extract_human_pose.py',
    'extract_shots_as_features.py', 
    'track_and_classify_frame_by_frame.py',
    'track_and_classify_with_rnn.py',
    'annotator.py',
    'visualize_features.py'
]
for script in scripts:
    path = project_root / script
    exists = "✓" if path.exists() else "✗"
    print(f"      {exists} {script}")

print("\n   Trained Models:")
models = [
    'tennis_fully_connected.h5',
    'tennis_rnn.h5'
]
for model in models:
    path = project_root / model
    exists = "✓" if path.exists() else "✗"
    size = f"({path.stat().st_size / 1e6:.1f} MB)" if path.exists() else ""
    print(f"      {exists} {model} {size}")

print("\n   Jupyter Notebooks:")
notebooks = [
    'RNNShotClassifier.ipynb',
    'SingleFrameShotClassifier.ipynb'
]
for nb in notebooks:
    path = project_root / nb
    exists = "✓" if path.exists() else "✗"
    print(f"      {exists} {nb}")

print("\n   Datasets:")
dataset_root = project_root / 'dataset'
if dataset_root.exists():
    players = [d.name for d in dataset_root.iterdir() if d.is_dir()]
    print(f"      Players: {', '.join(sorted(players))}")
    
    for player in sorted(players):
        shots_path = dataset_root / player / 'shots'
        if shots_path.exists():
            shot_files = list(shots_path.glob('*.csv'))
            if shot_files:
                shot_types = {}
                for f in shot_files:
                    shot_type = f.stem.rsplit('_', 1)[0]
                    shot_types[shot_type] = shot_types.get(shot_type, 0) + 1
                print(f"        {player}: {', '.join([f'{t}: {c}' for t, c in sorted(shot_types.items())])}")

# Check dependencies
print("\n2. DEPENDENCIES:")
deps = [
    'tensorflow',
    'opencv',
    'numpy',
    'pandas',
    'keras',
    'h5py'
]

for dep in deps:
    try:
        if dep == 'opencv':
            __import__('cv2')
        else:
            __import__(dep)
        print(f"      ✓ {dep}")
    except ImportError:
        print(f"      ✗ {dep} (NOT INSTALLED)")

# Check movenet model
print("\n3. MOVENET MODEL:")
movenet_path = project_root / 'movenet.tflite'
if movenet_path.exists():
    print(f"      ✓ movenet.tflite ({movenet_path.stat().st_size / 1e6:.1f} MB)")
else:
    print(f"      ✗ movenet.tflite (NOT FOUND)")
    print(f"        Download from: https://tfhub.dev/google/lite-model/movenet/singlepose/lightning/tflite/float16/4?lite-format=tflite")

# Test key imports
print("\n4. TESTING KEY IMPORTS:")
try:
    from extract_human_pose import HumanPoseExtractor, RoI
    print("      ✓ extract_human_pose.HumanPoseExtractor")
except Exception as e:
    print(f"      ✗ extract_human_pose.HumanPoseExtractor: {e}")

# Summary
print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
print("\nProject Overview:")
print("  - Tennis shot recognition system using Movenet + Neural Networks")
print("  - Two classification approaches:")
print("    1. Single Frame: Dense NN (tennis_fully_connected.h5)")
print("    2. Temporal: RNN/GRU (tennis_rnn.h5)")
print("  - Shot types: forehand, backhand, serve, neutral")
print("\nMain Commands:")
print("  - python track_and_classify_frame_by_frame.py <video.mp4> tennis_fully_connected.h5")
print("  - python track_and_classify_with_rnn.py <video.mp4> tennis_rnn.h5 [--left-handed]")
print("\nNote: You need a tennis video to run the main scripts")
print("=" * 70)
