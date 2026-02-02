import cv2
import numpy as np
import os

# CORE LOGIC

def logistic_map(size, r=3.99, x0=0.5):
    """Generates the chaotic key sequence."""
    x = x0
    seq = np.empty(size, dtype=np.uint8)
    for i in range(size):
        x = r * x * (1 - x)
        seq[i] = int((x * 1000) % 256)
    return seq

def automatic_roi(image, window_size=64):
    """Finds the area with the highest variance (detail)."""
    h, w = image.shape
    max_var = -1
    best = (0, 0, window_size, window_size)

    for y in range(0, h - window_size, window_size):
        for x in range(0, w - window_size, window_size):
            block = image[y:y+window_size, x:x+window_size]
            v = np.var(block)
            if v > max_var:
                max_var = v
                best = (x, y, window_size, window_size)
    return best

def process_image(image, roi, r, x0):
    """Encrypts or Decrypts the ROI using XOR."""
    x, y, w, h = roi
    # Extract ROI
    roi_img = image[y:y+h, x:x+w]
    
    # Generate Key
    key = logistic_map(roi_img.size, r, x0).reshape(roi_img.shape)
    
    # Transform (XOR)
    transformed_roi = cv2.bitwise_xor(roi_img, key)
    
    # Place back into image
    output = image.copy()
    output[y:y+h, x:x+w] = transformed_roi
    
    return output

def save_encrypted_file(image, filename, folder="encrypted"):
    """Saves the image to the specific folder."""
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder: {folder}")
    
    path = os.path.join(folder, filename)
    cv2.imwrite(path, image)
    return path