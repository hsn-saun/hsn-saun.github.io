# tools/extract_figure.py

Pulls one figure out of a paper PDF and writes it as a PNG, for the thumbnails
beside each entry in the Publications list.

```bash
curl -sL https://arxiv.org/pdf/2608.21411 -o paper.pdf
python3 tools/extract_figure.py paper.pdf 1 assets/figures/social-graph-mamba.png --dpi 600
#                               ^pdf      ^fig no.  ^output

# A whole proceedings volume: give the chapter's page range, or figure numbers
# from other chapters will match first.
python3 tools/extract_figure.py 978-981-97-5504-2.pdf 7 assets/figures/pure-pursuit-drl.png \
        --dpi 600 --from 577 --to 595
```

`--dpi 600` is worth using: the default renders fine for a thumbnail but the
figures are also linked at full size, where 260 dpi shows.

Needs `pdftotext` and `pdftoppm` (poppler-utils) and Python `pillow` + `numpy`.

## How it works, and where it can go wrong

`pdfimages` is no help on these papers: the figures are vector drawings with
raster pieces layered on top, so there is no single embedded image to pull out.
Instead the script finds the figure's *caption* with `pdftotext -bbox-layout`,
then crops the page region directly above it.

Three rules do the real work:

- **Which columns.** A caption that straddles the page centre belongs to a
  figure spanning both columns; otherwise the figure sits in the caption's own
  column.
- **Where the figure starts.** Walking up from the caption, the script stops at
  the first line of *body text*, defined as wider than a quarter of the page.
  Short lines are skipped on purpose: axis ticks and the labels drawn inside a
  diagram come back from `pdftotext` as text too, and stopping at those crops
  the figure down to nothing.
- **Which line is the caption.** IEEE punctuates ("Fig. 1:"), Springer often
  does not ("Fig. 4 The motion path..."). The strict pattern is tried across
  every page first, and only then the loose one — matching loosely from the
  start would catch a cross-reference like "Fig. 1 shows..." in the body text
  and crop a page with no figure on it.

Whatever survives is cropped, then tightened against the surrounding whitespace.

If a figure comes out wrong, the usual causes are a caption above rather than
below its figure, or a figure with a wide text annotation inside it that trips
the body-text rule. Check the result before committing it — the script does not
know what the figure is supposed to look like.

## Papers without a figure

Six of the seven publications have a figure. The exception is the 2023 Hanoi
University of Industry journal article: VJOL publishes no full-text galley for
it, so there is nothing to extract from. That entry runs full width instead, and
the Publications list is built to look right either way.

The Springer chapters are paywalled, but the proceedings volumes were supplied
locally and the figures came out of those. Keep the source PDFs somewhere
outside the repo — they are large and not ours to redistribute.
