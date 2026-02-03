import requests

base_urls = [
    "http://www.holybible.or.kr/Hymn/img/",
    "http://www.holybible.or.kr/Hymn/score/",
    "http://file.goodtv.co.kr/Hymn/",
    "http://new.holybible.or.kr/data/Hymn/"
]

target = 630
extensions = [".jpg", ".gif", ".png"]

print(f"Probing for {target}...")

found = False
for base in base_urls:
    for ext in extensions:
        url = f"{base}{target}{ext}"
        try:
            r = requests.head(url, timeout=2)
            if r.status_code == 200:
                print(f"FOUND: {url}")
                found = True
                break
        except:
            pass
    if found: break

if not found:
    print("No simple pattern found.")
