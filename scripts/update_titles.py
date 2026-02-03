
import json
import os

# Configuration
DATA_FILE = "src/data/hymns.json"
NEW_TITLES_FILE = "scripts/namu_titles.json"

def update_titles():
    # Load existing hymns data
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        hymns_db = json.load(f)

    # Load new titles
    if not os.path.exists(NEW_TITLES_FILE):
        print(f"Error: {NEW_TITLES_FILE} not found.")
        return

    with open(NEW_TITLES_FILE, 'r', encoding='utf-8') as f:
        new_titles = json.load(f)
    
    # Create a lookup map for new titles
    title_map = {item['number']: item['title'] for item in new_titles}

    updated_count = 0
    
    # Update titles in hymns_db
    for hymn in hymns_db:
        number = hymn['number']
        if number in title_map:
            new_title = title_map[number]
            if hymn['title'] != new_title:
                hymn['title'] = new_title
                updated_count += 1
    
    # Save updated DB
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(hymns_db, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully updated {updated_count} hymn titles in {DATA_FILE}")

if __name__ == "__main__":
    update_titles()
