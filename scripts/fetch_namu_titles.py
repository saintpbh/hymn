from playwright.sync_api import sync_playwright
import json

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://namu.wiki/w/%EC%83%88%EC%B0%AC%EC%86%A1%EA%B0%80/%EB%AA%A9%EB%A1%9D", timeout=60000)
        
        # Wait for table
        try:
            page.wait_for_selector("table")
        except:
            print("Table not found")
            return

        # Extract table rows
        # Namuwiki tables are often complex, but let's try to grab all text cells
        # They usually have columns: Number | Title | English Title | ...
        
        data = page.evaluate("""() => {
            const rows = Array.from(document.querySelectorAll('table tbody tr'));
            return rows.map(row => {
                const cells = Array.from(row.querySelectorAll('td'));
                return cells.map(c => c.innerText.trim());
            });
        }""")
        
        print(json.dumps(data, ensure_ascii=False, indent=2))
        browser.close()

if __name__ == "__main__":
    run()
