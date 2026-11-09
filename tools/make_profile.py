"""Builds the light/dark SVG cards for the DATA-ENRICHER GitHub profile, in the data-enricher.com house style
(barcode logo with the teal bar, paper background, Archivo-like type), modelled on the mark-app profile cards."""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

THEMES = {
    'light': dict(bg='#F4F5F3', dot='#E3E5E0', card='#FFFFFF', line='#DADDD6', ink='#121416', muted='#5F6670',
                  accent='#0B6E6C', tint='#0B6E6C', term='#121416', term_ink='#EEF0F2', term_muted='#7C838C'),
    'dark': dict(bg='#0D1012', dot='#1C2124', card='#151A1D', line='#252C30', ink='#EEF0F2', muted='#9AA2AB',
                 accent='#2FB3AD', tint='#2FB3AD', term='#06080A', term_ink='#EEF0F2', term_muted='#6C747C'),
}
SANS = "Archivo, Inter, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"
REDUCE = '@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def svg(w, h, label, style, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(label)}">\n<title>{esc(label)}</title>\n<style>{style} {REDUCE}</style>\n{body}\n</svg>\n')


def barcode(x, y, s, c, anim=False):
    """The data-enricher logo: a framed barcode with one teal bar. s = size in px."""
    k = s / 32
    bars = [(7, 1.6), (10, 1.6), (12.5, 1.6), (18.5, 1.6), (21, 1.6), (25, 1.6)]
    out = [f'<g transform="translate({x} {y}) scale({k:.4f})">',
           f'<rect x="2.5" y="2.5" width="27" height="27" fill="none" stroke="{c["ink"]}" stroke-width="1.5"/>']
    for i, (bx, bw) in enumerate(bars):
        cls = f' class="bar" style="animation-delay:{0.05 * i:.2f}s"' if anim else ''
        out.append(f'<rect{cls} x="{bx - bw / 2}" y="7" width="{bw}" height="18" fill="{c["ink"]}"/>')
    cls = ' class="bar" style="animation-delay:.35s"' if anim else ''
    out.append(f'<rect{cls} x="14.5" y="7" width="2.5" height="18" fill="{c["accent"]}"/>')
    out.append('</g>')
    return ''.join(out)


def header(c):
    style = ('.rise { animation: rise .8s ease backwards; } @keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }'
             ' .bar { transform-box: fill-box; transform-origin: bottom; animation: grow .5s ease backwards; } @keyframes grow { from { transform: scaleY(0); } }'
             ' .scan { opacity: 0; animation: scan 3.6s ease-in-out infinite; } @keyframes scan { 0%, 100% { transform: translateY(0); opacity: 0; } 10%, 90% { opacity: .9; } 50% { transform: translateY(150px); } }'
             ' .ln { animation: show .4s ease backwards; } @keyframes show { from { opacity: 0; } }'
             ' .cursor { animation: blink 1s steps(1) infinite; } @keyframes blink { 50% { opacity: 0; } }')
    b = [f'<defs><pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="{c["dot"]}"/></pattern></defs>',
         f'<rect width="1200" height="380" rx="18" fill="{c["bg"]}"/><rect width="1200" height="380" rx="18" fill="url(#grid)"/>',
         barcode(56, 110, 160, c, anim=True),
         f'<rect class="scan" x="60" y="118" width="152" height="3" rx="1.5" fill="{c["accent"]}"/>',
         f'<g class="rise"><text x="256" y="172" font-family="{SANS}" font-size="58" font-weight="800" fill="{c["ink"]}">Data Enricher</text></g>',
         f'<text class="rise" style="animation-delay:.2s" x="259" y="208" font-family="{SANS}" font-size="14" font-weight="700" letter-spacing="3" fill="{c["muted"]}">ONE EAN. A COMPLETE PRODUCT PAGE.</text>',
         f'<rect class="rise" style="animation-delay:.35s" x="259" y="232" width="56" height="5" rx="2.5" fill="{c["accent"]}"/>',
         f'<text class="rise" style="animation-delay:.45s" x="259" y="274" font-family="{SANS}" font-size="16" fill="{c["ink"]}">Checked photos &#183; 18 languages &#183; SEO for categories and brands</text>',
         f'<text class="rise" style="animation-delay:.55s" x="259" y="300" font-family="{SANS}" font-size="14" fill="{c["muted"]}">PrestaShop &#183; Odoo &#183; WooCommerce &#183; Magento &#183; Sylius &#183; REST API</text>',
         f'<rect x="800" y="120" width="376" height="216" rx="12" fill="{c["term"]}"/>',
         '<circle cx="822" cy="142" r="5.5" fill="#FF5F57"/><circle cx="840" cy="142" r="5.5" fill="#FEBC2E"/>',
         f'<circle cx="858" cy="142" r="5.5" fill="{c["accent"] if c is THEMES["dark"] else "#2FB3AD"}"/>',
         f'<text x="988" y="146" font-family="{MONO}" font-size="11" fill="{c["term_muted"]}" text-anchor="middle">api.data-enricher.com</text>']
    lines = [
        ('$ POST /lookup {"ean": "7333377653917"}', 'term_ink'),
        ('&#10004; Identified: Husqvarna 550i XP', 'tint'),
        ('&#10004; 8 checked photos, 6 rejected', 'tint'),
        ('&#10004; Texts in 18 languages, meta included', 'tint'),
        ('&#10004; Ready in 9 s. Next time: &lt; 1 s from cache', 'tint'),
    ]
    for i, (t, col) in enumerate(lines):
        fill = c['term_ink'] if col == 'term_ink' else ('#2FB3AD')
        b.append(f'<text class="ln" style="animation-delay:{0.7 + i * 0.8:.1f}s" x="822" y="{184 + i * 26}" font-family="{MONO}" font-size="12.5" fill="{fill}">{t}</text>')
    b.append(f'<rect class="cursor" x="822" y="306" width="8" height="15" fill="#2FB3AD"/>')
    return svg(1200, 380, 'Data Enricher: one EAN, a complete product page. Checked photos, texts in 18 languages and SEO texts for categories and brands.', style, ''.join(b))


CARD_STYLE = '.card { animation: up .7s ease backwards; } @keyframes up { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }'


def stats(c):
    items = [('7&#8211;15 s', 'a new product', 'found, checked and written'),
             ('&lt; 1 s', 'from the cache', 'and those requests are free'),
             ('18', 'languages', 'with the right number format'),
             ('8', 'checked photos', 'same brand, model and version')]
    w, gap, x0 = 270, 24, 24
    b = [f'<rect width="1200" height="180" rx="18" fill="{c["bg"]}"/>']
    for i, (big, title, sub) in enumerate(items):
        x = x0 + i * (w + gap)
        b.append(f'<g class="card" style="animation-delay:{i * 0.12:.2f}s"><rect x="{x}" y="24" width="{w}" height="132" rx="14" fill="{c["card"]}" stroke="{c["line"]}"/>'
                 f'<rect x="{x}" y="24" width="6" height="132" rx="3" fill="{c["accent"]}"/>'
                 f'<text x="{x + 30}" y="88" font-family="{SANS}" font-size="42" font-weight="800" fill="{c["accent"]}">{big}</text>'
                 f'<text x="{x + 30}" y="116" font-family="{SANS}" font-size="17" font-weight="700" fill="{c["ink"]}">{title}</text>'
                 f'<text x="{x + 30}" y="138" font-family="{SANS}" font-size="13.5" fill="{c["muted"]}">{sub}</text></g>')
    return svg(1200, 180, 'Measured: 7 to 15 seconds for a new product, under 1 second from the cache, 18 languages, up to 8 checked photos.', CARD_STYLE, ''.join(b))


ICONS = {
    'photo': 'M-16 -11 h32 v22 h-32 z M-16 6 l9 -8 l7 6 l6 -5 l10 9 M7 -4 m-3 0 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0',
    'text': 'M-14 -12 h28 M-14 -4 h28 M-14 4 h20 M-14 12 h12',
    'globe': 'M0 -15 a15 15 0 1 0 0.01 0 M-15 0 h30 M0 -15 c-8 8 -8 22 0 30 M0 -15 c8 8 8 22 0 30',
    'tag': 'M-14 -14 h13 l15 15 l-13 13 l-15 -15 z M-7 -7 m-2 0 a2 2 0 1 0 4 0 a2 2 0 1 0 -4 0',
    'search': 'M-4 -4 m-10 0 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0 M4 4 l11 11',
    'api': 'M-8 -12 l-9 12 l9 12 M8 -12 l9 12 l-9 12 M3 -14 l-6 28',
}


def features(c):
    tiles = [('photo', 'Checked photos', 'AI rejects other models, logos, collages'),
             ('text', 'Product texts', 'Sections you switch on, off and reorder'),
             ('globe', '18 languages', 'Only facts that can be found online'),
             ('tag', 'Category and brand pages', 'Intro, buying guide, internal links'),
             ('search', 'Own crawler and search', 'No cost per search, paid only as fallback'),
             ('api', 'REST API and batches', 'JSON, 20 EANs per batch, 5 at once')]
    b = [f'<rect width="1200" height="300" rx="18" fill="{c["bg"]}"/>']
    for i, (icon, title, sub) in enumerate(tiles):
        col, row = i % 3, i // 3
        x, y = 24 + col * 392, 24 + row * 136
        cx, cy = x + 58, y + 58
        b.append(f'<g class="card" style="animation-delay:{i * 0.08:.2f}s"><rect x="{x}" y="{y}" width="368" height="116" rx="14" fill="{c["card"]}" stroke="{c["line"]}"/>'
                 f'<circle cx="{cx}" cy="{cy}" r="30" fill="{c["accent"]}" fill-opacity=".13"/>'
                 f'<path transform="translate({cx} {cy}) scale(.85)" d="{ICONS[icon]}" fill="none" stroke="{c["accent"]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<text x="{x + 108}" y="{y + 52}" font-family="{SANS}" font-size="18" font-weight="700" fill="{c["ink"]}">{title}</text>'
                 f'<text x="{x + 108}" y="{y + 76}" font-family="{SANS}" font-size="13.5" fill="{c["muted"]}">{sub}</text></g>')
    return svg(1200, 300, 'Features: checked photos, product texts, 18 languages, category and brand pages, own crawler and search engine, REST API with batches.', CARD_STYLE, ''.join(b))


def pipeline(c):
    steps = [('EAN', 'one barcode'), ('Find', 'own crawler'), ('Check', 'AI photo check'), ('Write', '18 languages'), ('Your shop', 'module or API')]
    style = (CARD_STYLE + ' .flow { stroke-dasharray: 6 8; animation: flow 1.2s linear infinite; } @keyframes flow { to { stroke-dashoffset: -14; } }')
    b = [f'<rect width="1200" height="200" rx="18" fill="{c["bg"]}"/>',
         f'<text x="40" y="52" font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="4" fill="{c["muted"]}">HOW IT WORKS</text>',
         f'<line class="flow" x1="120" y1="122" x2="1080" y2="122" stroke="{c["accent"]}" stroke-width="3"/>']
    for i, (title, sub) in enumerate(steps):
        x = 120 + i * 240
        last = i == len(steps) - 1
        fill = c['accent'] if last or i == 0 else c['card']
        ink = '#FFFFFF' if last or i == 0 else c['accent']
        b.append(f'<g class="card" style="animation-delay:{i * 0.15:.2f}s"><circle cx="{x}" cy="122" r="26" fill="{fill}" stroke="{c["accent"]}" stroke-width="3"/>'
                 f'<text x="{x}" y="128" font-family="{SANS}" font-size="16" font-weight="800" fill="{ink}" text-anchor="middle">{i + 1}</text>'
                 f'<text x="{x}" y="80" font-family="{SANS}" font-size="18" font-weight="800" fill="{c["ink"]}" text-anchor="middle">{title}</text>'
                 f'<text x="{x}" y="174" font-family="{SANS}" font-size="13.5" fill="{c["muted"]}" text-anchor="middle">{sub}</text></g>')
    return svg(1200, 200, 'How it works: an EAN, the own crawler finds the product, AI checks the photos, texts are written in 18 languages, and the result goes into your shop via the module or the API.', style, ''.join(b))


def platforms(c):
    items = [('PrestaShop', '1.7.7 to 9'), ('Odoo', '16 to 20'), ('WooCommerce', '8 and newer'),
             ('Magento', '2.4.4 and newer'), ('Sylius', '2'), ('REST API', 'any platform or PIM')]
    w = 178
    b = [f'<rect width="1200" height="150" rx="18" fill="{c["bg"]}"/>']
    for i, (name, ver) in enumerate(items):
        x = 24 + i * (w + 16)
        b.append(f'<g class="card" style="animation-delay:{i * 0.08:.2f}s"><rect x="{x}" y="24" width="{w}" height="102" rx="14" fill="{c["card"]}" stroke="{c["line"]}"/>'
                 f'<rect x="{x + 20}" y="44" width="28" height="4" rx="2" fill="{c["accent"]}"/>'
                 f'<text x="{x + 20}" y="80" font-family="{SANS}" font-size="19" font-weight="800" fill="{c["ink"]}">{name}</text>'
                 f'<text x="{x + 20}" y="104" font-family="{SANS}" font-size="13.5" fill="{c["muted"]}">{ver}</text></g>')
    return svg(1200, 150, 'Works with PrestaShop 1.7.7 to 9, Odoo 16 to 20, WooCommerce 8 and newer, Magento 2.4.4 and newer, Sylius 2, and any platform through the REST API.', CARD_STYLE, ''.join(b))


def footer():
    t = THEMES['light']
    style = '.wave { animation: drift 8s linear infinite; } @keyframes drift { to { transform: translateX(-600px); } }'
    dark = {**t, 'ink': '#FFFFFF', 'accent': '#121416'}
    b = [f'<rect width="1200" height="140" rx="18" fill="{t["accent"]}"/>',
         '<path class="wave" d="M0 110 Q 150 80 300 110 T 600 110 T 900 110 T 1200 110 T 1500 110 T 1800 110 V140 H0 Z" fill="#FFFFFF" fill-opacity=".12"/>',
         '<rect x="40" y="30" width="80" height="80" rx="14" fill="#F4F5F3"/>',
         barcode(48, 38, 64, {**t}),
         '<text x="150" y="68" font-family="' + SANS + '" font-size="26" font-weight="800" fill="#FFFFFF">Try it with your own EAN.</text>',
         '<text x="150" y="98" font-family="' + SANS + '" font-size="15" fill="#E3F3F2">Live demo, no account needed &#183; data-enricher.com &#183; a product by MARK-APP</text>',
         '<g transform="translate(1100 70)"><circle r="30" fill="#121416"/><path d="M-9 -1 h18 M2 -9 l8 8 l-8 8" fill="none" stroke="#2FB3AD" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>']
    del dark
    return svg(1200, 140, 'Try it with your own EAN: live demo on data-enricher.com, a product by MARK-APP.', style, ''.join(b))


for name, fn in [('header', header), ('stats', stats), ('features', features), ('pipeline', pipeline), ('platforms', platforms)]:
    for mode, theme in THEMES.items():
        (OUT / f'{name}-{mode}.svg').write_text(fn(theme))
(OUT / 'footer.svg').write_text(footer())

# self-check: every file is well-formed XML
import xml.dom.minidom
for f in OUT.glob('*.svg'):
    xml.dom.minidom.parse(str(f))
print('ok', len(list(OUT.glob('*.svg'))), 'svgs')
