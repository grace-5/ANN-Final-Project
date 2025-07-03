
import os
import hashlib
from PIL import Image
import numpy as np
import shutil

# Folder paths
RAW_DATA_DIR = r'PCOS'
CLEANED_DATA_DIR = 'cleaned_PCOS'  # Output folder for cleaned dataset
IMAGE_SIZE = (240, 240)  # Resize target size

def remove_duplicates_and_resize():
    seen_hashes = set()

    for label in ['infected', 'noninfected']:
        source_dir = os.path.join(RAW_DATA_DIR, label)
        target_dir = os.path.join(CLEANED_DATA_DIR, label)
        os.makedirs(target_dir, exist_ok=True)

        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)

            # Read and hash image
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

            if file_hash in seen_hashes:
                print(f"Duplicate removed: {filename}")
                continue  # Skip duplicate
            seen_hashes.add(file_hash)

            # Load image, resize, and save to cleaned dataset
            try:
                with Image.open(file_path) as img:
                    img = img.convert('L')  # Convert to grayscale
                    img_resized = img.resize(IMAGE_SIZE)
                    cleaned_filename = f"{file_hash}.jpg"
                    cleaned_path = os.path.join(target_dir, cleaned_filename)
                    img_resized.save(cleaned_path, 'JPEG')
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

    print("Cleaning & preprocessing complete.")

def main():
    # Remove old cleaned folder if exists
    if os.path.exists(CLEANED_DATA_DIR):
        shutil.rmtree(CLEANED_DATA_DIR)

    remove_duplicates_and_resize()

if __name__ == '__main__':
    main()
