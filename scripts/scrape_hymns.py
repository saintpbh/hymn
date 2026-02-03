
import requests
from bs4 import BeautifulSoup
import os
import re
import json
import time

# Configuration
OUTPUT_DIR = "public/hymns"
DATA_FILE = "src/data/hymns.json"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

# User-Agent to mimic browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

# List of URLs provided by user
URLS = [
    "https://m.blog.naver.com/kyoung1958/222064185622", # 1-50
    "https://m.blog.naver.com/kyoung1958/222064229743", # 51-98
    "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222064237327&navType=by", # 99-141
    "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222064243050&navType=by", # 142-179
    "https://m.blog.naver.com/kyoung1958/222064264236", # 180-221 (Removed params for cleaner url if needed, but keeping as provided mainly)
    "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222064272949&navType=by", # 222-257
    "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222064280069&navType=by", # 258-300
    "https://m.blog.naver.com/kyoung1958/222064292947", # 301-345
    "https://m.blog.naver.com/kyoung1958/222064299737", # 346-381
    "https://m.blog.naver.com/kyoung1958/222064310655", # 382-428
    "https://m.blog.naver.com/kyoung1958/222065140533", # 429-478
    "https://m.blog.naver.com/kyoung1958/222065145505", # 479-520
    "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222065150620&navType=by", # 521-567
    "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222065154875&navType=by", # 568-608
    "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222065158207&navType=by", # 609-645
]

hymns_db = []
processed_numbers = set()

def download_image(url, number):
    try:
        # Naver blog images often behave better if we clean up query params or use 'w800'
        # But 'src' usually works.
        # We'll save as {number}.jpg
        filepath = os.path.join(OUTPUT_DIR, f"{number}.jpg")
        
        # Check if already exists to save time during dev
        if os.path.exists(filepath):
            print(f"Skipping download for {number} (exists)")
            return f"/hymns/{number}.jpg"

        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(r.content)
        print(f"Downloaded hymn {number}")
        time.sleep(0.1) # Be gentle
        return f"/hymns/{number}.jpg"
    except Exception as e:
        print(f"Failed to download {number} from {url}: {e}")
        return None

def scrape():
    global hymns_db
    
    for url in URLS:
        print(f"Scraping URL: {url}")
        try:
            resp = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Find images
            # Naver mobile pages have images in various containers.
            # We look for img tags that are likely the hymn sheets.
            # They usually have 'postfiles.pstatic.net' in src.
            
            images = soup.find_all('img')
            
            # We need to sort or process them in order.
            # Usually they appear in order in the DOM.
            
            for img in images:
                src = img.get('src')
                if not src or 'postfiles.pstatic.net' not in src:
                    continue
                
                # Check for "sticker" or "profile" images to exclude
                if 'sticker' in src or 'profile' in src:
                    continue

                # Try to extract hymm number from ALT text or Siblings
                # Alt text format often: "새찬송가 1장 ..."
                alt = img.get('alt', '')
                
                match = re.search(r'(\d+)장', alt)
                if not match:
                    # Try to see if previous element text has it?
                    # This is tricky without seeing DOM.
                    # fallback: Extract from filename?
                    # But filenames are hashes.
                    # Let's rely on ALT for now, and print if missing.
                    pass
                
                # Clean up src url
                # Sometimes src has ?type=... we might want high res
                # Usually naver provides a good default.
                # If it's a thumbnail (w80), we might want to change it.
                # But let's assume src is decent or replace type.
                if '?type=' in src:
                    # Remove type param to get original or set to large
                    base_src = src.split('?')[0]
                    high_res_src = f"{base_src}?type=w1200" # Request explicit size
                else:
                    high_res_src = src

                # Determine number
                number = None
                if match:
                    number = int(match.group(1))
                else:
                    # Fallback logic could be sequence based if we are careful
                     # But let's log simple failures first.
                     continue

                if number in processed_numbers:
                    continue
                    
                processed_numbers.add(number)
                
                # Download
                local_path = download_image(high_res_src, number)
                
                if local_path:
                    hymns_db.append({
                        "number": number,
                        "title": alt.replace(f"{number}장", "").strip("- ").strip(), # Simple cleanup
                        "imagePath": local_path
                    })

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # Sort DB
    hymns_db.sort(key=lambda x: x['number'])
    
    # Save
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(hymns_db, f, ensure_ascii=False, indent=2)
    
    print(f"Scraping complete. Found {len(hymns_db)} hymns.")

if __name__ == "__main__":
    scrape()
