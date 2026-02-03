import json
import os

titles_file = "src/data/hymn_titles.json"
hymns_file = "src/data/hymns.json"

def merge():
    if not os.path.exists(titles_file) or not os.path.exists(hymns_file):
        print("Files not found")
        return

    with open(titles_file, 'r', encoding='utf-8') as f:
        titles_list = json.load(f)
        # Convert to dict for fast lookup
        titles_map = {item['number']: item['title'] for item in titles_list}

    with open(hymns_file, 'r', encoding='utf-8') as f:
        hymns_list = json.load(f)

    updated_count = 0
    for hymn in hymns_list:
        num = hymn['number']
        if num in titles_map:
            hymn['title'] = titles_map[num]
            updated_count += 1
    
    with open(hymns_file, 'w', encoding='utf-8') as f:
        json.dump(hymns_list, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated_count} hymns with real titles in {hymns_file}")

if __name__ == "__main__":
    merge()
