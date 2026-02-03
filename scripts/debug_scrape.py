
import requests
from bs4 import BeautifulSoup

url = "https://m.blog.naver.com/kyoung1958/222064185622"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    images = soup.find_all('img')
    print(f"Total images: {len(images)}")
    
    for i, img in enumerate(images):
        src = img.get('src', 'No src')
        if 'postfiles.pstatic.net' in src:
            print(f"--- Image {i} ---")
            print(f"Src: {src}")
            print(f"Alt: {img.get('alt', 'No Alt')}")
            print(f"Class: {img.get('class')}")
            parent = img.parent
            print(f"Parent Text: {parent.get_text()[:50] if parent else 'None'}")
            
        if i > 20: break 
except Exception as e:
    print(e)
