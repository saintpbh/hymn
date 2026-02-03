from playwright.sync_api import sync_playwright
import os
import requests
import re
import sys
import time
from urllib.parse import unquote

OUTPUT_DIR = "public/hymns"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Targets: 62, 102, 111 (re-download) AND 630, 632, 634, 637, 640, 641, 642, 644, 645 (missing)
TARGETS = {62, 102, 111, 630, 632, 634, 637, 640, 641, 642, 644, 645}

URLS = [
    "https://m.blog.naver.com/kyoung1958/222064229743", # 51-98 (Contains 62)
    "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222064237327&navType=by", # 99-?? (Contains 102, 111)
    "https://m.blog.naver.com/PostView.naver?blogId=kyoung1958&logNo=222065158207&navType=by", # End range (Contains 600+)
]

processed = set()

def download_image(url, number):
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            filepath = os.path.join(OUTPUT_DIR, f"{number}.jpg")
            with open(filepath, 'wb') as f:
                f.write(r.content)
            print(f"Downloaded {number}.jpg")
            return True
    except Exception as e:
        print(f"Failed {number}: {e}")
    return False

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for url in URLS:
            print(f"Scanning {url}...")
            page.goto(url, timeout=60000)
            
            # Scroll to load lazy images
            for _ in range(5):
                page.mouse.wheel(0, 3000)
                time.sleep(1)

            images_data = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('img')).map(img => img.src || img.getAttribute('data-src'));
            }""")

            for src in images_data:
                if not src: continue
                
                # Check for our targets
                match = None
                
                # Regex 1: /62장 or /062장
                m1 = re.search(r'/(\d{1,3})(?:%EC%9E%A5|장)', src)
                if m1: match = int(m1.group(1))
                
                if not match:
                    decoded = unquote(src)
                    m2 = re.search(r'/(\d{1,3})(?:장|_)', decoded)
                    if m2: match = int(m2.group(1))

                if match and match in TARGETS:
                    if match not in processed:
                        print(f"Found target {match}: {src[:50]}...")
                        if download_image(src, match):
                            processed.add(match)

        browser.close()
        print(f"Processed: {processed}")
        missing = TARGETS - processed
        if missing:
            print(f"Still missing: {missing}")

if __name__ == "__main__":
    run()
