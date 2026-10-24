#!/usr/bin/env bash
# Build both CVs and publish the academic one to the website's assets folder.
# Usage:  ./build.sh
set -euo pipefail

cd "$(dirname "$0")"

for f in CV_Academic CV_Industry; do
  echo "building $f ..."
  xelatex -interaction=nonstopmode -halt-on-error "$f.tex" > "$f.log" 2>&1 || {
    echo "  FAILED — last errors:"; grep -E '^!' "$f.log" | head -5; exit 1;
  }
  echo "  $f.pdf — $(pdfinfo "$f.pdf" | awk '/^Pages/{print $2}') page(s)"
done

# Both versions are offered from the site's CV menu.
cp CV_Academic.pdf ../assets/HongSon_Nguyen_CV_Academic.pdf
cp CV_Industry.pdf ../assets/HongSon_Nguyen_CV_Industry.pdf

# Kept as an alias of the academic CV: this filename was published first and may
# already be linked from elsewhere. Delete it once you are sure nothing points here.
cp CV_Academic.pdf ../assets/HongSon_Nguyen_CV.pdf

echo "published to ../assets/:"
echo "  HongSon_Nguyen_CV_Academic.pdf"
echo "  HongSon_Nguyen_CV_Industry.pdf"
echo "  HongSon_Nguyen_CV.pdf (alias of the academic version)"

# The terminal portfolio serves its own copies.
PORTFOLIO=../../hongson-github-portfolio/assets
if [ -d "$PORTFOLIO" ]; then
  cp CV_Academic.pdf "$PORTFOLIO/HongSon_Nguyen_CV_Academic.pdf"
  cp CV_Industry.pdf "$PORTFOLIO/HongSon_Nguyen_CV_Industry.pdf"
  echo "also copied both into the portfolio repo — commit them there separately"
fi

rm -f ./*.aux ./*.out ./*.log
