import os
import sys
from pathlib import Path

print("PROJECT ANALYSIS - TENNIS SHOT RECOGNITION")
print("="*70)

# Check models
project_root = Path.cwd()
print(f"\nProject Root: {project_root}")

models = ['tennis_fully_connected.h5', 'tennis_rnn.h5']
print("\nModels:")
for m in models:
    p = project_root / m
    if p.exists():
        size_mb = p.stat().st_size / (1024*1024)
        print(f"  ✓ {m} ({size_mb:.1f} MB)")
    else:
        print(f"  ✗ {m} NOT FOUND")

# Check python packages
print("\nChecking packages:")
packages = ['tensorflow', 'cv2', 'numpy', 'pandas', 'keras']
for pkg in packages:
    try:
        __import__('tensorflow' if pkg == 'tensorflow' else pkg)
        print(f"  ✓ {pkg}")
    except ImportError:
        print(f"  ✗ {pkg} NOT INSTALLED")

# Check dataset
print("\nDataset:")
dataset = Path(r"C:\Users\SUJAL\Downloads\tennis_shot_recognition-master\tennis_shot_recognition-master\dataset")
if dataset.exists():
    players = [d.name for d in dataset.iterdir() if d.is_dir()]
    print(f"  Players found: {len(players)}")
    for p in sorted(players)[:5]:
        shots_path = dataset / p / 'shots'
        if shots_path.exists():
            csvs = list(shots_path.glob('*.csv'))
            print(f"    - {p}: {len(csvs)} shots")

print("\n" + "="*70)
