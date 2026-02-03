import re
from urllib.parse import unquote

src = "https://mblogthumb-phinf.pstatic.net/MjAyMDA4MThfMTU5/MDAxNTk3NzU0ODUyOTIz.7u9O6su8cUDDVYbDM8Foen7nISksKCASW6PUkNXA5cEg.InXizi8Eg9wQ4Xj9PkqFFRDVLyEvMbJq1wze1DQ_xtwg.JPEG.kyoung1958/001%EC%9E%A5_%EB%A7%8C%EB%B3%B5%EC%9D%98_%EA%B7%BC%EC%9B%90_%ED%95%98%EB%82%98%EB%8B%98.jpg?type=w2"

print(f"Testing Src: {src}")

match = re.search(r'/(\d{1,3})(?:%EC%9E%A5|장)', src)
if match:
    print(f"Match found: {match.group(1)}")
else:
    print("No match on direct src")

decoded_src = unquote(src)
print(f"Decoded: {decoded_src}")
match_decoded = re.search(r'/(\d{1,3})(?:장|_)', decoded_src)
if match_decoded:
    print(f"Match found on decoded: {match_decoded.group(1)}")
else:
    print("No match on decoded")
