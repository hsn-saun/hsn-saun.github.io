# Hong-Son Nguyen — academic homepage

A small academic site in the style used by most robotics research groups: one column,
no framework, no build step, and only a few lines of JavaScript.

```
index.html          Home — bio, research interests, news
publications.html   the publication list, with a figure beside each entry
style.css           all styling; light and dark, plus a print stylesheet
assets/             portrait and CV PDFs
assets/figures/     method figures shown beside each publication
cv/                 LaTeX sources for both CVs
tools/              pulls a figure out of a paper PDF
```

Education, experience and awards deliberately live in the CVs only, not on the site.

### The header is duplicated

With no build step and no templating, the top bar, the portrait/name block and the
closing scripts exist verbatim in both pages. **Change one and change the other** — a
nav link, a new contact link, or a change of affiliation has to be applied twice. The
alternative would be a static site generator, which is not worth it for two pages.

## Two files to add

Neither is in the repo yet, and the page is built to degrade gracefully without them.

1. **`assets/portrait.jpg`** — a portrait photo. Any size; it is cropped to a 4:5 box,
   so a head-and-shoulders shot works best. Until you add it, the page shows
   `assets/portrait-placeholder.svg` instead.
2. The CVs are generated — see [`cv/`](cv/). Run `cv/build.sh` and it writes
   `assets/HongSon_Nguyen_CV_Academic.pdf` and `assets/HongSon_Nguyen_CV_Industry.pdf`,
   which the header's **CV** menu offers as a choice, plus copies into the terminal
   portfolio repo if it sits alongside this one.

## Running it locally

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Deploying to GitHub Pages

Push to a GitHub repo, then in **Settings → Pages** set the source to the `main` branch,
root folder. Nothing needs to be built.

Note that the repo name decides the URL: a repo named `<username>.github.io` is served at
`https://<username>.github.io`, while any other name is served at
`https://<username>.github.io/<repo-name>`.

## Editing

Everything is plain HTML — edit `index.html` directly.

- **News**: add a `<dt>`/`<dd>` pair at the top of the `.news` list. Keep it to a handful
  of recent items; a long news list ages badly.
- **Publications**: copy an existing `<li>` in the `.pubs` list and edit it. The order is
  newest first. Each entry carries links in the `.meta` line — add `Code`, `Video`, `PDF`
  or `BibTeX` links there as they become available.
- **Publication figures**: an entry with a thumbnail is `<li class="has-fig">` and holds a
  `<figure class="pub-fig">` before its `<div class="pub-body">`. Drop the class and the
  figure and the entry runs full width instead — one of the seven has no thumbnail,
  the HaUI journal article, whose full text is not online. To make a new one, see
  [`tools/`](tools/README.md), which extracts a figure straight out of the paper PDF.
- **Colors and type**: the palette lives in the `:root` block at the top of `style.css`,
  with the dark overrides in `:root[data-theme="dark"]` right below it.

## Theme

The page opens in light and stays there regardless of the visitor's operating system
setting. The button in the top-right switches to dark, and the choice is remembered in
that browser's `localStorage` under the key `theme`.

Two small scripts drive it: one in `<head>` applies a remembered dark choice before the
first paint, so returning visitors never see a flash of light; the other at the end of
`<body>` handles the button. Everything else on the page works without JavaScript.

To follow the operating system instead of defaulting to light, add this to `style.css`:

```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { /* copy the dark tokens here */ }
}
```

## Where the content came from

Publications are verified against Google Scholar and the publisher pages (arXiv, Springer,
VJOL). Education, experience and awards come from the CV at
<https://sites.google.com/view/hongsonnguyen-cv/cv>.

One thing to keep an eye on: that CV lists the MSc and the NRSL fellowship as ending in
July 2026, while this page presents both as ongoing. Whichever is accurate, keep this page
and the Google Site saying the same thing.
