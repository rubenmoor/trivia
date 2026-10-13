#!/usr/bin/env bash
# Achievement icons (plan 86, SW-11): <API>.svg → png/<API>_achieved.png + png/<API>_unachieved.png
# (greyscale, dimmed) at Steamworks' 256×256. ImageMagick (librsvg) from the dev shell.
set -euo pipefail
cd "$(dirname "$0")"
size=256
rm -rf png
mkdir png
for svg in *.svg; do
  id=${svg%.svg}
  magick -background none -density 192 "$svg" -resize "${size}x${size}!" "png/${id}_achieved.png"
  magick "png/${id}_achieved.png" -modulate 60,0 "png/${id}_unachieved.png"
done
echo "$(ls png | wc -l) PNGs in $(pwd)/png"
