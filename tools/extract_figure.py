#!/usr/bin/env python3
"""Crop a figure out of a paper PDF by locating its caption box.

pdfimages is no use here: these figures are vector art with raster pieces layered
on top, so there is no single embedded image to pull. Instead we find the caption
line, walk upwards until we hit the previous text, and crop what lies between.
"""
import re, subprocess, sys, xml.etree.ElementTree as ET
from PIL import Image

NS = {'x': 'http://www.w3.org/1999/xhtml'}


def page_lines(pdf, page):
    out = subprocess.run(
        ['pdftotext', '-bbox-layout', '-f', str(page), '-l', str(page), pdf, '-'],
        capture_output=True, text=True, check=True).stdout
    # Scanned proceedings sometimes carry control characters straight through from
    # the PDF's text layer, which makes pdftotext emit XML no parser will accept.
    out = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', out)
    root = ET.fromstring(out)
    pg = root.find('.//x:page', NS)
    W, H = float(pg.get('width')), float(pg.get('height'))
    lines = []
    for ln in pg.iter('{http://www.w3.org/1999/xhtml}line'):
        text = ' '.join(w.text or '' for w in ln)
        lines.append((float(ln.get('xMin')), float(ln.get('yMin')),
                      float(ln.get('xMax')), float(ln.get('yMax')), text.strip()))
    return W, H, lines


def find_caption(pdf, fignum, firstpage, lastpage):
    """Locate the caption line for a figure.

    Tried strictest first. IEEE-style captions punctuate ("Fig. 1:"), Springer
    often does not ("Fig. 4 The motion path..."), but the loose pattern alone
    also matches cross-references in the body text such as "Fig. 1 shows...",
    which would send the crop to a page with no figure on it.
    """
    strict = re.compile(r'^(Fig\.|Figure)\s*%d\s*[:.]\s' % fignum)
    loose = re.compile(r'^(Fig\.|Figure)\s*%d\s+[A-Z]' % fignum)
    pages = []
    for p in range(firstpage, lastpage + 1):
        pages.append((p,) + page_lines(pdf, p))
    for pat in (strict, loose):
        for p, W, H, lines in pages:
            for ln in lines:
                if pat.match(ln[4]):
                    return p, W, H, lines, ln
    return None


def crop(pdf, fignum, out_png, dpi=260, firstpage=1, lastpage=12):
    hit = find_caption(pdf, fignum, firstpage, lastpage)
    if not hit:
        raise SystemExit('caption Fig. %d not found in %s' % (fignum, pdf))
    page, W, H, lines, cap = hit
    cx0, cy0, cx1, _, captext = cap

    # A caption straddling the page centre belongs to a figure spanning both
    # columns; otherwise the figure sits in whichever column the caption is in.
    mid = W / 2
    if cx0 < mid < cx1:
        x0, x1 = 0.03 * W, 0.97 * W
    elif cx1 <= mid:
        x0, x1 = 0.03 * W, mid
    else:
        x0, x1 = mid, 0.97 * W

    # Walk up from the caption to the nearest line of *body text*. Short lines are
    # skipped: axis ticks and box labels drawn inside the figure come back from
    # pdftotext as text too, and bounding on those would crop the figure to nothing.
    body_min_width = 0.25 * W
    top = 0.04 * H
    for lx0, ly0, lx1, ly1, txt in lines:
        if ly1 >= cy0 - 1 or not txt:
            continue
        if lx1 < x0 or lx0 > x1:
            continue
        if (lx1 - lx0) < body_min_width:
            continue                      # a label inside the figure, not body text
        top = max(top, ly1 + 5)

    box = (x0, top, x1, cy0 - 2)
    if box[3] - box[1] < 40:
        raise SystemExit('figure region too short for Fig. %d in %s' % (fignum, pdf))

    subprocess.run(['pdftoppm', '-png', '-r', str(dpi), '-f', str(page), '-l', str(page),
                    pdf, out_png + '.page'], check=True)
    import glob
    rendered = sorted(glob.glob(out_png + '.page*.png'))[0]
    im = Image.open(rendered)
    s = dpi / 72.0
    im = im.crop(tuple(int(v * s) for v in box))

    # trim residual white margin
    import numpy as np
    a = np.array(im.convert('L'))
    ink = np.where((a < 245).any(axis=1))[0], np.where((a < 245).any(axis=0))[0]
    if len(ink[0]) and len(ink[1]):
        im = im.crop((max(0, ink[1].min() - 8), max(0, ink[0].min() - 8),
                      min(im.width, ink[1].max() + 9), min(im.height, ink[0].max() + 9)))
    im.save(out_png)
    subprocess.run(['rm', '-f'] + glob.glob(out_png + '.page*.png'))
    print('%s  Fig.%d  page %d  %dx%d  "%s"' % (pdf, fignum, page, im.width, im.height, captext[:60]))


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Crop one figure out of a paper PDF.')
    ap.add_argument('pdf')
    ap.add_argument('fignum', type=int)
    ap.add_argument('out_png')
    ap.add_argument('--dpi', type=int, default=260,
                    help='render resolution; raise it for a book-sized page (default 260)')
    ap.add_argument('--from', dest='first', type=int, default=1,
                    help='first page to search — set this when the PDF is a whole '
                         'proceedings volume, so figure numbers from other chapters '
                         'are not picked up')
    ap.add_argument('--to', dest='last', type=int, default=12, help='last page to search')
    a = ap.parse_args()
    crop(a.pdf, a.fignum, a.out_png, dpi=a.dpi, firstpage=a.first, lastpage=a.last)
