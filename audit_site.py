import pathlib, re, json

root = pathlib.Path('.')
html_files = []
for html in root.rglob('*.html'):
    name = html.name.lower()
    if 'index-old' in name or name.startswith('template'):
        continue
    if 'iportfolio' in str(html.parent).lower() and html.parent != root:
        continue
    html_files.append(html)
refs_re = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.I)
img_re = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\']', re.I)

local_refs = []
missing_refs = []
external_refs = []
img_refs = []

for html in html_files:
    text = html.read_text(encoding='utf-8', errors='ignore')
    page_dir = html.parent

    for m in refs_re.findall(text):
        url = m.strip()
        if not url:
            continue

        if url.startswith(('mailto:', 'tel:', 'http://', 'https://', '//', '#', 'javascript:', 'data:')):
            if url.startswith(('http://', 'https://')):
                external_refs.append((str(html), url))
            continue

        target = url.split('#')[0].split('?')[0]
        if not target:
            continue

        resolved = (page_dir / target).resolve()
        if resolved.exists():
            local_refs.append((str(html), url, str(resolved)))
        else:
            missing_refs.append((str(html), url, str(resolved)))

    for m in img_re.findall(text):
        url = m.strip()
        if not url or url.startswith(('http://', 'https://', '//', 'data:')):
            if url.startswith(('http://', 'https://')):
                external_refs.append((str(html), url))
            continue
        target = url.split('#')[0].split('?')[0]
        if not target:
            continue
        resolved = (page_dir / target).resolve()
        if resolved.exists():
            img_refs.append((str(html), url, str(resolved)))
        else:
            missing_refs.append((str(html), url, str(resolved)))

print('HTML files audited:', len(html_files))
print('Local local href/src refs:', len(local_refs))
print('Image refs:', len(img_refs))
print('Broken refs:', len(missing_refs))
print('External refs:', len(external_refs))

if missing_refs:
    print('\nBROKEN REFS')
    for page, url, resolved in missing_refs:
        print(page, '=>', url, '=>', resolved)

if external_refs:
    print('\nEXTERNAL REFS')
    for page, url in external_refs:
        print(page, '=>', url)
