from playwright.sync_api import sync_playwright
import time
from urllib.parse import unquote

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = "https://m.blog.naver.com/kyoung1958/222064185622"
        print(f"Navigating to {url}")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        
        # Scroll bit
        page.mouse.wheel(0, 3000)
        time.sleep(1)

        images = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('img')).map(img => ({
                src: img.src,
                dataSrc: img.getAttribute('data-src'),
                alt: img.alt,
                className: img.className
            }));
        }""")

        print(f"Found {len(images)} images total.")
        for i, img in enumerate(images):
            # Print first 20 to see structure
            if i < 20:
                print(f"[{i}] SRC: {img['src']}")
                print(f"    DATA-SRC: {img['dataSrc']}")
                print(f"    ALT: {img['alt']}")
                print("-" * 20)
        
        browser.close()

if __name__ == "__main__":
    run()
