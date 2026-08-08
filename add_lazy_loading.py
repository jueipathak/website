#!/usr/bin/env python3
"""
Add lazy loading attributes to all portfolio images in HTML
"""
import re

html_file = "c:\\Users\\patha\\Downloads\\iPortfolio\\iPortfolio\\index.html"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Dictionary mapping image paths to better alt text
alt_text_map = {
    "Arijit Sir Caricature.jpeg": "Arijit Singh Caricature Artwork",
    "borkarcouple.jpg": "Borkar Couple Caricature",
    "Parshuram Sir Caricature.jpg": "Parshuram Sir Caricature",
    "Sankalp Caricature.jpg": "Sankalp Caricature Artwork",
    "Shivani Maam Caricature.jpg": "Shivani Maam Caricature",
    "forest guardian.jpeg": "Forest Guardian Concept Art",
    "Vivienne bg.jpg": "Vivienne Character Design",
    "dr strange realistic.jpg": "Dr. Strange Realistic Digital Painting",
    "Azrael bg.jpg": "Azrael Character Design",
    "Lord Magnus bg.jpg": "Lord Magnus Character Design",
    "Tyranix with bg.jpg": "Tyranix Character Design",
    "Juei board 1.jpg": "Gaming Character Design Board 1",
    "Juei board 2.jpg": "Gaming Character Design Board 2",
    "halloween.jpg": "Halloween Character Artwork",
    "halloween 2.jpg": "Halloween Character Artwork 2",
    "halloween3.jpg": "Halloween Character Artwork 3",
    "dragon empress.jpeg": "Dragon Empress Concept Art",
    "forest houses environment.jpeg": "Forest Houses Environment Concept",
    "lit town.jpeg": "Lit Town Concept Artwork",
    "phoenix.jpeg": "Phoenix Concept Art",
    "skeleton bird.jpeg": "Skeleton Bird Concept Art",
    "town.jpeg": "Town Environment Concept",
    "col. dhamdhere digital painting.jpg": "Colonel Dhamdhere Digital Portrait",
    "vaishali tai digital painting.jpg": "Vaishali Tai Digital Portrait"
}

# Find and replace all portfolio images
for filepath, alt_text in alt_text_map.items():
    filename = filepath.split('/')[-1]
    
    # Pattern for img tags with this file
    pattern = rf'<img src="assets/img/portfolio/[^"]*{re.escape(filename)}"[^>]*class="img-fluid"[^>]*alt="[^"]*"[^>]*>'
    
    # Check if already has lazy loading
    if f'src="assets/img/portfolio/{filepath}"' in content:
        old_pattern = f'<img src="assets/img/portfolio/{filepath}" class="img-fluid" alt="">'
        new_content = f'<img src="assets/img/portfolio/{filepath}" class="img-fluid" alt="{alt_text}" loading="lazy" decoding="async">'
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_content)
            print(f"✅ Updated: {filename}")

# Write back
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ All portfolio images updated with lazy loading and descriptive alt text!")
