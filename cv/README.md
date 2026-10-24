# CV sources

Two CVs built from the same facts, for two different readers.

| File | Length | For |
|---|---|---|
| `CV_Academic.tex` | 2 pages | PhD applications, research positions. Education and the full publication list carry the document. |
| `CV_Industry.tex` | 2 pages | Robotics / perception / ML engineering roles. Skills and outcomes first; publications compressed to one line. |

`cvstyle.sty` holds the shared layout, so a change to spacing or colour reaches both.

## Building

```bash
./build.sh
```

Needs `xelatex` and the `Charis SIL` font. The script builds both PDFs and copies
the academic one to `../assets/HongSon_Nguyen_CV.pdf`, which is the filename the
website's CV link points at. Edit that line in `build.sh` if you would rather the
site serve the industry version.

Charis SIL is a Charter derivative, so the CVs and the website share the same
typeface, and it covers Vietnamese diacritics — which plain Charter does not.

## Contact details

Phone, email and IELTS score are written into the `.tex` files directly — search for
`+84` or `IELTS` to change them. There are no placeholders left.

## Editing

- **A new publication**: copy a `\pub{authors}{title}{venue}{link}` block in
  `CV_Academic.tex`. The fourth argument takes a `\plink{label}{url}` call, or empty
  braces when there is no link. Write your own name as `\me` in the author list —
  it renders bold and in full-strength ink while co-authors stay muted grey.
- **A new job**: copy an `\entry{dates}{title}{employer}` block followed by an
  `achievements` list.
- **Links use icons.** `\ilink{icon}{text}{url}` in the header, `\plink{label}{url}`
  beside a publication. Icon names come from `fontawesome5` and `academicons`; not
  every name in their documentation exists in the installed version, so build after
  adding one. `\faExternalLinkAlt` and `\aiArxiv`, for instance, do not work here.
- **Page balance** is what to watch. The academic CV fills two pages almost exactly;
  adding a publication will push it to a third unless something else comes out.

## Kept in sync by hand

The facts here come from the same sources as the website: the CV site at
<https://sites.google.com/view/hongsonnguyen-cv/cv> for education, experience and
awards, and Google Scholar for publications. The monthly Scholar sync routine
updates the *portfolio site only* — it does not touch these files, so a new paper
needs adding here by hand.
