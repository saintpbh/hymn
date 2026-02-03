import json

titles_file = "src/data/hymn_titles.json"

updates = {
    630: "진리와 생명 되신 주",
    631: "우리 기도를",
    632: "주여 주여 우리를",
    633: "나의 하나님 받으소서",
    634: "모든 것이 주께로부터",
    635: "하늘에 계신(주기도문)",
    636: "하늘에 계신(주기도문)",
    637: "주님 우리의 마음을 여시어",
    638: "주 너를 지키시고",
    639: "주 함께 하소서",
    640: "아멘",
    641: "아멘",
    642: "아멘",
    643: "아멘",
    644: "아멘",
    645: "아멘"
}

with open(titles_file, 'r', encoding='utf-8') as f:
    titles = json.load(f)

for item in titles:
    n = item['number']
    if n in updates:
        item['title'] = updates[n]

with open(titles_file, 'w', encoding='utf-8') as f:
    json.dump(titles, f, ensure_ascii=False, indent=2)

print("Updated titles for 630-645")
