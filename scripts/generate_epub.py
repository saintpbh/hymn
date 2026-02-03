import os
import json
import zipfile
import shutil
from datetime import datetime

# Configuration
SOURCE_IMAGES_DIR = "public/hymns-opt"
DATA_FILE = "src/data/hymns.json"
OUTPUT_EPUB = "Hymn365_light.epub"
TEMP_DIR = "epub_temp"
OEBPS_DIR = os.path.join(TEMP_DIR, "OEBPS")
META_INF_DIR = os.path.join(TEMP_DIR, "META-INF")
IMAGES_DEST_DIR = os.path.join(OEBPS_DIR, "images")

def clean_temp():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(OEBPS_DIR)
    os.makedirs(META_INF_DIR)
    os.makedirs(IMAGES_DEST_DIR)

def create_mimetype():
    with open(os.path.join(TEMP_DIR, "mimetype"), "w") as f:
        f.write("application/epub+zip")

def create_container_xml():
    content = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>"""
    with open(os.path.join(META_INF_DIR, "container.xml"), "w") as f:
        f.write(content)

def get_hymn_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return sorted(data, key=lambda x: int(x['number']))

def copy_images(hymns):
    valid_images = []
    print("Copying images from public/hymns-opt...")
    for hymn in hymns:
        num = int(hymn['number'])
        # Source files are like 1.jpg, 2.jpg...
        src_name = f"{num}.jpg"
        src_path = os.path.join(SOURCE_IMAGES_DIR, src_name)
        
        # Destination we rename to hymn_1.jpg to be safe/consistent
        dst_name = f"hymn_{num}.jpg"
        
        if os.path.exists(src_path):
            dst_path = os.path.join(IMAGES_DEST_DIR, dst_name)
            shutil.copy(src_path, dst_path)
            valid_images.append(dst_name)
        else:
            print(f"Warning: Image missing for hymn {num} at {src_path}")
    return valid_images

def create_css():
    css = """
    body { font-family: sans-serif; margin: 0; padding: 5px; text-align: center; }
    h1 { font-size: 1.5em; margin: 0.5em 0; }
    img { max-width: 100%; height: auto; }
    
    /* Navigation Buttons */
    .menu-list { display: flex; flex-direction: column; gap: 10px; }
    .menu-btn {
        display: block;
        padding: 15px;
        background: #f8f8f8;
        border: 2px solid #ddd;
        border-radius: 8px;
        text-decoration: none;
        color: #000;
        font-size: 1.4em;
        font-weight: bold;
    }
    
    /* Grid for Level 4 (Songs) */
    .song-grid { 
        display: grid; 
        grid-template-columns: repeat(2, 1fr); /* 2 columns for big targets */
        gap: 15px; 
        padding: 10px;
    }
    .song-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 80px;
        background: white;
        border: 2px solid #333;
        border-radius: 10px;
        color: black;
        font-size: 1.5em;
        font-weight: bold;
        text-decoration: none;
    }
    
    .back-link { 
        display: block; 
        margin: 20px auto; 
        padding: 12px; 
        width: 80%;
        background: #eee; 
        border-radius: 20px;
        text-decoration: none; 
        color: #333; 
        font-size: 1.2em;
    }
    .hidden-text { font-size: 1px; color: white; display: none; }
    """
    with open(os.path.join(OEBPS_DIR, "style.css"), "w") as f:
        f.write(css)

def create_pages(hymns):
    manifest_items = []
    spine_items = []
    
    # --- LEVEL 1: Main Index (1-100, 101-200...) ---
    index_html = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Hymn Index</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
    <h1>Hymn Reference</h1>
    <div class="menu-list">
"""
    # Create 100-hymn ranges
    ranges_100 = []
    for i in range(0, 645, 100):
        start = i + 1
        end = min(i + 100, 645)
        ranges_100.append((start, end))
        index_html += f'<a href="idx_100_{start}.xhtml" class="menu-btn">{start} - {end}</a>\n'
    
    index_html += "    </div></body></html>"
    with open(os.path.join(OEBPS_DIR, "index.xhtml"), "w") as f:
        f.write(index_html)
    manifest_items.append('<item id="root" href="index.xhtml" media-type="application/xhtml+xml"/>')
    spine_items.append('<itemref idref="root"/>')

    # --- LEVEL 2: 20-hymn Groups (1-20, 21-40...) ---
    for start_100, end_100 in ranges_100:
        html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{start_100}-{end_100}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
    <h1>{start_100} - {end_100}</h1>
    <a href="index.xhtml" class="back-link">← Home</a>
    <div class="menu-list">
"""
        # Split into 20 chunks
        for j in range(start_100 - 1, end_100, 20):
            s = j + 1
            e = min(j + 20, end_100)
            html += f'<a href="idx_20_{s}.xhtml" class="menu-btn">{s} - {e}</a>\n'
        
        html += "    </div></body></html>"
        filename = f"idx_100_{start_100}.xhtml"
        with open(os.path.join(OEBPS_DIR, filename), "w") as f:
            f.write(html)
        id_ref = f"idx_100_{start_100}"
        manifest_items.append(f'<item id="{id_ref}" href="{filename}" media-type="application/xhtml+xml"/>')
        spine_items.append(f'<itemref idref="{id_ref}"/>')

        # --- LEVEL 3: 10-hymn Groups (1-10, 11-20...) ---
        for j in range(start_100 - 1, end_100, 20):
            s_20 = j + 1
            e_20 = min(j + 20, end_100)
            
            html_20 = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{s_20}-{e_20}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
    <h1>{s_20} - {e_20}</h1>
    <a href="idx_100_{start_100}.xhtml" class="back-link">← Up ({start_100}-{end_100})</a>
    <div class="menu-list">
"""
            for k in range(s_20 - 1, e_20, 10):
                s_10 = k + 1
                e_10 = min(k + 10, e_20)
                html_20 += f'<a href="idx_10_{s_10}.xhtml" class="menu-btn">{s_10} - {e_10}</a>\n'

            html_20 += "    </div></body></html>"
            filename_20 = f"idx_20_{s_20}.xhtml"
            with open(os.path.join(OEBPS_DIR, filename_20), "w") as f:
                f.write(html_20)
            id_ref_20 = f"idx_20_{s_20}"
            manifest_items.append(f'<item id="{id_ref_20}" href="{filename_20}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{id_ref_20}"/>')

            # --- LEVEL 4: 10 Hymn Buttons (The Song Grid) ---
            for k in range(s_20 - 1, e_20, 10):
                s_10 = k + 1
                e_10 = min(k + 10, e_20)
                
                html_10 = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{s_10}-{e_10}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
    <h1>{s_10} - {e_10}</h1>
    <a href="idx_20_{s_20}.xhtml" class="back-link">← Up ({s_20}-{e_20})</a>
    <div class="song-grid">
"""
                for m in range(s_10, e_10 + 1):
                    html_10 += f'<a href="hymn_{m}.xhtml" class="song-btn">{m}</a>\n'

                html_10 += "    </div></body></html>"
                filename_10 = f"idx_10_{s_10}.xhtml"
                with open(os.path.join(OEBPS_DIR, filename_10), "w") as f:
                    f.write(html_10)
                id_ref_10 = f"idx_10_{s_10}"
                manifest_items.append(f'<item id="{id_ref_10}" href="{filename_10}" media-type="application/xhtml+xml"/>')
                spine_items.append(f'<itemref idref="{id_ref_10}"/>')

    # --- HYMN PAGES ---
    for hymn in hymns:
        num = hymn['number']
        title = hymn['title']
        img_file = f"hymn_{num}.jpg"
        
        # Calculate parent index (start of the 10-block)
        num_int = int(num)
        range_10_start = ((num_int - 1) // 10) * 10 + 1
        
        page_html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{num}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
    <div class="hidden-text">Hymn {num} {title}</div>
    <img src="images/{img_file}" alt="{title}" />
    <br/>
    <a href="idx_10_{range_10_start}.xhtml" class="back-link">Back to List</a>
</body></html>"""
        
        filename = f"hymn_{num}.xhtml"
        with open(os.path.join(OEBPS_DIR, filename), "w") as f:
            f.write(page_html)
        
        id_ref = f"hymn_{num}"
        manifest_items.append(f'<item id="{id_ref}" href="{filename}" media-type="application/xhtml+xml"/>')
        spine_items.append(f'<itemref idref="{id_ref}"/>')
        
        # Add image to manifest
        manifest_items.append(f'<item id="img_{num}" href="images/{img_file}" media-type="image/jpeg"/>')

    return manifest_items, spine_items

def create_opf(manifest_items, spine_items):
    manifest_str = "\n        ".join(manifest_items)
    spine_str = "\n        ".join(spine_items)
    
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="3.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>Hymn365 (Light)</dc:title>
        <dc:creator>SaintPBH</dc:creator>
        <dc:identifier id="bookid">urn:uuid:hymn365-light-v1</dc:identifier>
        <dc:language>ko</dc:language>
        <meta property="dcterms:modified">{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}</meta>
        <meta name="cover" content="cover-image"/>
    </metadata>
    <manifest>
        <item id="css" href="style.css" media-type="text/css"/>
        <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
        {manifest_str}
    </manifest>
    <spine toc="ncx">
        {spine_str}
    </spine>
</package>"""
    
    with open(os.path.join(OEBPS_DIR, "content.opf"), "w") as f:
        f.write(opf)

def create_ncx(hymns):
    # Minimal NCX for legacy support
    ncx = """<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head><meta name="dtb:uid" content="urn:uuid:hymn365-touch-v2"/></head>
    <docTitle><text>Hymn365</text></docTitle>
    <navMap>
        <navPoint id="root" playOrder="1">
            <navLabel><text>Home Index</text></navLabel>
            <content src="index.xhtml"/>
        </navPoint>
    </navMap>
</ncx>"""
    with open(os.path.join(OEBPS_DIR, "toc.ncx"), "w") as f:
        f.write(ncx)

def zip_epub():
    print(f"Zipping to {OUTPUT_EPUB}...")
    with zipfile.ZipFile(OUTPUT_EPUB, 'w', zipfile.ZIP_DEFLATED) as epub:
        epub.write(os.path.join(TEMP_DIR, "mimetype"), "mimetype", compress_type=zipfile.ZIP_STORED)
        for root, _, files in os.walk(TEMP_DIR):
            for file in files:
                if file == "mimetype": continue
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, TEMP_DIR)
                epub.write(abs_path, rel_path)

def main():
    print("Starting Touch-Optimized Generation...")
    clean_temp()
    create_mimetype()
    create_container_xml()
    create_css()
    
    hymns = get_hymn_data()
    copy_images(hymns)
    
    manifest, spine = create_pages(hymns)
    create_ncx(hymns)
    create_opf(manifest, spine)
    
    zip_epub()
    shutil.rmtree(TEMP_DIR)
    print("Done.")

if __name__ == "__main__":
    main()
