import json
import re

def parse_titles(input_file, output_file):
    titles = {}
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Match "Number. Title"
            match = re.match(r'(\d+)[.\s]+(.+)', line)
            if match:
                num = int(match.group(1))
                title = match.group(2).strip()
                # Remove any "(통일 123장)" or "[1]" suffix
                title = re.sub(r'\s*\(통일 \d+장\)', '', title)
                title = re.sub(r'\[\d+\]', '', title)
                titles[num] = title
    
    # Fill gaps with "Hymn N" or previous logic if needed, but we aim for full coverage
    
    # 602-645 are clearly Amen.
    # Check if we missed any from the list 
    # (The list had 600. 교회의 참된 터는, etc. which contradicted some other sources, 
    # but strictly following the list is safer than guessing "Amen" for all).
    
    # Let's ensure we have 1 to 645
    final_list = []
    for i in range(1, 646):
        title = titles.get(i, f"Hymn {i}") # Fallback
        
        # If title is "아멘" and it's a hymn, it's correct.
        
        final_list.append({
            "number": i,
            "title": title
        })
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
    
    print(f"Parsed {len(titles)} titles. Saved to {output_file}")

if __name__ == "__main__":
    parse_titles('scripts/raw_titles.txt', 'src/data/hymn_titles.json')
