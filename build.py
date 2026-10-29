"""Rebuild the standalone HTML and offline package using Python 3 standard library."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parent
html = (root / 'index.html').read_text(encoding='utf-8')
css = (root / 'style.css').read_text(encoding='utf-8')
js = (root / 'app.js').read_text(encoding='utf-8')
assert '<link rel="stylesheet" href="style.css">' in html
assert '<script src="app.js" defer></script>' in html
html = html.replace('<link rel="stylesheet" href="style.css">', '<style>\n' + css + '\n</style>')
html = html.replace('<script src="app.js" defer></script>', '')
html = html.replace('</body>', '<script>\n' + js.replace('</script', '<\\/script') + '\n</script></body>')
(root / 'nexus-demo.html').write_text(html, encoding='utf-8')
files = ['index.html', 'style.css', 'app.js', 'nexus-demo.html', 'README.md', 'QA.md', 'build.py', 'dashboard.png', 'about.png', 'mobile.png', 'report.png']
with ZipFile(root / 'nexus-demo-package.zip', 'w', ZIP_DEFLATED) as archive:
    for name in files:
        archive.write(root / name, 'nexus-worklog-portfolio/' + name)
with ZipFile(root / 'nexus-demo-package.zip') as archive:
    assert archive.testzip() is None
print('Generated nexus-demo.html and nexus-demo-package.zip')
