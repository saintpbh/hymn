import requests
from bs4 import BeautifulSoup

url = "https://m.blog.naver.com/kyoung1958/222064185622"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# Print all text to see if titles are commonly listed
print(soup.get_text()[:2000])

# Also check for specific pattern "1장"
import re
text = soup.get_text()
matches = re.findall(r'(\d+)\s*장\s*([^\n]+)', text)
for m in matches[:10]:
    print(m)
