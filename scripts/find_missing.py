import os

existing = set()
for f in os.listdir("public/hymns"):
    if f.endswith(".jpg"):
        try:
            num = int(f.replace(".jpg", ""))
            existing.add(num)
        except:
            pass

missing = []
for i in range(1, 646):
    if i not in existing:
        missing.append(i)

print(f"Missing {len(missing)} files: {missing}")
