import requests
from bs4 import BeautifulSoup

# This site often uses frames. Let's start with the main page.
url = "http://www.holybible.or.kr/Hymn/"
try:
    r = requests.get(url, timeout=10)
    r.encoding = 'euc-kr' # Common for older Korean sites
    print("Main Page preview:")
    print(r.text[:500])
except Exception as e:
    print(e)
