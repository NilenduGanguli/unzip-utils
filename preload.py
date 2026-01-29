import os
import shutil
import time
import json

# Configuration
SOURCE_DIR = "/data/preload_source"
DEST_DIR = "/data/documents"

# Map filename -> desired document_link_id
PRELOAD_MAP = {
    "large_mixed.zip": "000000000a",
    "medium_nested.zip": "000000000b",
    "small_flat.zip": "000000000c"
}

def preload_files():
    print("Starting preload process...")
    
    # Ensure destination exists
    os.makedirs(DEST_DIR, exist_ok=True)
    
    for filename, doc_id in PRELOAD_MAP.items():
        src_path = os.path.join(SOURCE_DIR, filename)
        dest_path = os.path.join(DEST_DIR, doc_id)
        
        if os.path.exists(src_path):
            print(f"Preloading {filename} to ID {doc_id}...")
            try:
                # Copy file content to destination with name = doc_id
                shutil.copy2(src_path, dest_path)
                
                # Write metadata file
                meta_path = dest_path + ".meta"
                with open(meta_path, 'w') as f:
                    json.dump({"filename": filename}, f)
                
                print(f"Successfully preloaded {filename}")
            except Exception as e:
                print(f"Error copying {filename}: {e}")
        else:
            print(f"Warning: Source file {filename} not found in {SOURCE_DIR}")
            
    print("Preload process complete.")

if __name__ == "__main__":
    preload_files()
