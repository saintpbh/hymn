
from playwright.sync_api import sync_playwright
import os
import json
import time
import requests
import re
from urllib.parse import unquote

# Configuration
OUTPUT_DIR = "public/hymns"
DATA_FILE = "src/data/hymns.json"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

URLS = [
    "https://m.blog.naver.com/kyoung1958/222064185622", # 1-50
    # Add fewer URLs for quick debug first? No, let's keep all but debug loop
    "https://m.blog.naver.com/kyoung1958/222064229743", # 51-98
     "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222064237327&navType=by",
     "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222064243050&navType=by",
     "https://m.blog.naver.com/kyoung1958/222064264236",
     "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222064272949&navType=by",
     "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222064280069&navType=by",
     "https://m.blog.naver.com/kyoung1958/222064292947",
     "https://m.blog.naver.com/kyoung1958/222064299737",
     "https://m.blog.naver.com/kyoung1958/222064310655",
     "https://m.blog.naver.com/kyoung1958/222065140533",
     "https://m.blog.naver.com/kyoung1958/222065145505",
     "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222065150620&navType=by", # 521-567
     "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222065154875&navType=by", # 568-608
     "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222065158207&navType=by", # 609-645
]

hymns_db = []
processed_numbers = set()

def download_image(url, number):
    try:
        filepath = os.path.join(OUTPUT_DIR, f"{number}.jpg")
        if os.path.exists(filepath):
            return f"/hymns/{number}.jpg"

        clean_url = url.split('?')[0] + "?type=w1200"
        
        r = requests.get(clean_url, timeout=10)
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(r.content)
        print(f"Downloaded hymn {number}")
        return f"/hymns/{number}.jpg"
    except Exception as e:
        print(f"Failed to download {number}: {e}")
        return None

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        )
        page = context.new_page()

        for url in URLS:
            print(f"Navigating to {url}")
            try:
                page.goto(url, timeout=60000)
                page.wait_for_load_state("networkidle")
                
                # Scroll
                for i in range(5): # Reduce scroll count for speed during debug
                    page.mouse.wheel(0, 2000)
                    time.sleep(1)
                
                image_elements = page.query_selector_all("img")
                print(f"Found {len(image_elements)} images")

                for i, img in enumerate(image_elements):
                    src = img.get_attribute("src")
                    alt = img.get_attribute("alt")
                    
                    if not src or "postfiles.pstatic.net" not in src:
                        src = img.get_attribute("data-src") or img.get_attribute("data-lazy-src")
                    
                    if not src or "postfiles.pstatic.net" not in src:
                        continue
                        
                    if "sticker" in src or "profile" in src:
                        continue

                    # Debug first few
                    if i < 3:
                        print(f"Debug Img: {src[:50]}... Alt: {alt}")

                    if not alt:
                        alt = ""
                    
                    match = re.search(r'(\d+)장', alt)
                    if not match:
                        try:
                            decoded_src = unquote(src)
                            match = re.search(r'(\d+)장', decoded_src)
                            if match and i < 3:
                                print(f"Matched via src decode: {match.group(1)}")
                        except Exception as e:
                            print(f"Decode error: {e}")
                    
                    if match:
                        number = int(match.group(1))
                        
                        if number in processed_numbers:
                            continue
                            
                        local_path = download_image(src, number)
                        
                        if local_path:
                            processed_numbers.add(number)
                            hymns_db.append({
                                "number": number,
                                "title": alt.replace(f"{number}장", "").strip("- ").strip() or f"Hymn {number}",
                                "imagePath": local_path
                            })
                    else:
                        # Log if we expected a match but failed (heuristic: high res image)
                        if 'w800' in src or 'w1200' in src:
                            print(f"Failed to match number for {src[:30]}")

            except Exception as e:
                print(f"Error processing {url}: {e}")
        
        browser.close()

    hymns_db.sort(key=lambda x: x['number'])
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(hymns_db, f, ensure_ascii=False, indent=2)
    print(f"Total hymns processed: {len(hymns_db)}")

if __name__ == "__main__":
    run()
