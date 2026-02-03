from playwright.sync_api import sync_playwright
import time
import os
import requests
import base64

OUTPUT_DIR = "public/hymns"
MISSING = [630, 632, 634, 637, 640, 641, 642, 644, 645]

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for num in MISSING:
            print(f"Searching for {num}...")
            try:
                # Search Google Images
                q = f"새찬송가 {num}장 악보"
                url = f"https://www.google.com/search?q={q}&tbm=isch"
                page.goto(url)
                
                # Click first image result
                # Usually div[data-id] or similar. 
                # Just waiting for first img to load might be enough if we pick a good one.
                # Google Images structure is complex.
                
                # Let's try Naver Image Search instead, simpler usually?
                # Or just DuckDuckGo (no captcha usually)
                
                # Let's use Naver Image Search
                url = f"https://search.naver.com/search.naver?where=image&sm=tab_jum&query={q}"
                page.goto(url)
                page.wait_for_selector(".image_tile img")
                
                # Get first image src
                src = page.evaluate("""() => {
                    const img = document.querySelector('.image_tile img');
                    return img ? img.src : null;
                }""")
                
                if src:
                    print(f"Found {src[:30]}...")
                    # Naver thumbnails are usually small (data:image or https)
                    # We might want the large one.
                    # Clicking it opens a viewer.
                    
                    page.click(".image_tile img")
                    time.sleep(2)
                    
                    # Try to find the large image in the viewer
                    # Selector might change.
                    # Fallback to thumbnail if needed, but we want quality.
                    
                    # Let's just take the first result's thumbnail for now to ensure EXISTENCE.
                    # Or try to find source.
                    
                    if src.startswith("data:image"):
                        # Decode
                        header, encoded = src.split(",", 1)
                        data = base64.b64decode(encoded)
                        with open(f"{OUTPUT_DIR}/{num}.jpg", "wb") as f:
                            f.write(data)
                    else:
                        r = requests.get(src)
                        with open(f"{OUTPUT_DIR}/{num}.jpg", "wb") as f:
                            f.write(r.content)
                    print(f"Saved {num}.jpg")
                else:
                    print(f"No image found for {num}")
                    
            except Exception as e:
                print(f"Error {num}: {e}")
        
        browser.close()

if __name__ == "__main__":
    run()
