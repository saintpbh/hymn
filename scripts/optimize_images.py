import os
import shutil
from PIL import Image, ImageOps

INPUT_DIR = "public/hymns"
OUTPUT_DIR = "public/hymns-opt"
MAX_WIDTH = 1200
JPEG_QUALITY = 60

def optimize_images():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    files = sorted([f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    total_files = len(files)
    
    print(f"Optimizing {total_files} images...")
    print(f"Settings: Max Width={MAX_WIDTH}px, Quality={JPEG_QUALITY}, Grayscale=True")
    
    saved_size = 0
    original_size = 0
    
    for i, filename in enumerate(files):
        in_path = os.path.join(INPUT_DIR, filename)
        out_path = os.path.join(OUTPUT_DIR, filename)
        
        # Stats
        original_size += os.path.getsize(in_path)
        
        try:
            with Image.open(in_path) as img:
                # 1. Convert to Grayscale (L)
                img = img.convert('L')
                
                # 2. Resize if too wide
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / float(img.width)
                    new_height = int(float(img.height) * ratio)
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                
                # 3. Save with compression
                img.save(out_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
                
                saved_size += os.path.getsize(out_path)
                
                if i % 50 == 0:
                    print(f"Processed {i}/{total_files}...")
                    
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            # Fallback copy
            shutil.copy(in_path, out_path)
            
    reduction = (1 - (saved_size / original_size)) * 100
    print(f"\nDone!")
    print(f"Original Size: {original_size / 1024 / 1024:.2f} MB")
    print(f"Optimized Size: {saved_size / 1024 / 1024:.2f} MB")
    print(f"Reduction: {reduction:.1f}%")

if __name__ == "__main__":
    optimize_images()
