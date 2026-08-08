#!/usr/bin/env python3
import re
import os

os.chdir(r"c:\Users\patha\Downloads\iPortfolio\iPortfolio")

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all portfolio img tags without lazy loading
pattern = r'<img src="(assets/img/portfolio/[^"]+)" class="img-fluid" alt="">'

def replacer(match):
    src = match.group(1)
    filename = src.split('/')[-1].replace('.jpg', '').replace('.jpeg', '')
    # Create meaningful alt text
    alt = filename.replace(' digital painting', '').replace(' painting', '').replace(' with bg', '').replace(' bg', '')
    alt = alt.replace('_', ' ').replace('-', ' ').title()
    return f'<img src="{src}" class="img-fluid" alt="{alt} - Juei Pathak Portfolio Art" loading="lazy" decoding="async">'

new_content = re.sub(pattern, replacer, content)

# Count replacements
original_count = len(re.findall(pattern, content))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

# Verify
with open('index.html', 'r', encoding='utf-8') as f:
    final = f.read()
    final_count = len(re.findall(r'loading="lazy"', final))

print(f"✅ Successfully updated {original_count} portfolio images")
print(f"✅ Total images with lazy loading: {final_count}")
