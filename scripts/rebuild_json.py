import json
import os

TITLES_FILE = "src/data/hymn_titles.json"
HYMNS_DIR = "public/hymns"
OUTPUT_FILE = "src/data/hymns.json"

def run():
    # Load titles
    with open(TITLES_FILE, 'r', encoding='utf-8') as f:
        titles_list = json.load(f)
        titles_map = {item['number']: item['title'] for item in titles_list}
    
    # Scan directory
    hymns = []
    files = os.listdir(HYMNS_DIR)
    
    for f in files:
        if f.endswith(".jpg"):
            try:
                num = int(f.replace(".jpg", ""))
                title = titles_map.get(num, f"Hymn {num}")
                
                hymns.append({
                    "number": num,
                    "title": title,
                    "imagePath": f"/hymns/{num}.jpg"
                })
            except Exception as e:
                print(f"Skipping {f}: {e}")
                
    # Sort
    hymns.sort(key=lambda x: x['number'])
    
    # Write
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(hymns, f, ensure_ascii=False, indent=2)
        
    print(f"Rebuilt hymns.json with {len(hymns)} entries.")

if __name__ == "__main__":
    run()
