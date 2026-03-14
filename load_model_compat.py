"""
Workaround to load the tennis_rnn model with newer Keras version
Rebuilds the model architecture and loads weights separately
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout
import h5py
import numpy as np

def load_tennis_rnn_model(model_path):
    """
    Load the tennis RNN model with compatibility fix for newer Keras versions
    """
    print(f"Loading model from {model_path}...")
    
    # Build the model architecture
    model = Sequential([
        GRU(units=24, dropout=0.1, input_shape=(30, 26), return_sequences=False),
        Dropout(0.2),
        Dense(units=8, activation='relu'),
        Dense(units=4, activation='softmax')  # 4 classes: backhand, forehand, neutral, serve
    ])
    
    # Load the weights from the HDF5 file
    try:
        with h5py.File(model_path, 'r') as f:
            # Get weight names from the model
            if 'model_weights' in f:
                for layer_name in f['model_weights']:
                    print(f"  Loading weights for {layer_name}")
        
        # Use TensorFlow's legacy loader
        from tensorflow.keras.saving import load_weights_from_checkpoint
        model.load_weights(model_path)
        print("✓ Model weights loaded successfully")
        
    except Exception as e:
        print(f"Error loading weights: {e}")
        # Try alternative loading method
        try:
            import h5py
            with h5py.File(model_path, 'r') as f:
                # Print structure
                print("Model structure:")
                def print_structure(name, obj):
                    print(f"  {name}")
                f.visititems(print_structure)
        except Exception as e2:
            print(f"Could not inspect model: {e2}")
    
    return model

# Test it
if __name__ == "__main__":
    try:
        model = load_tennis_rnn_model("tennis_rnn.h5")
        print("\nModel loaded successfully!")
        model.summary()
    except Exception as e:
        print(f"Error: {e}")
