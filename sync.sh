#!/bin/sh

set -e

[ -d OneDark-Pro ] || git clone https://github.com/Binaryify/OneDark-Pro.git --depth 1

mkdir -p themes/tmp/
cp OneDark-Pro/themes/*.json themes/tmp/

[ -d zed ] || git clone https://github.com/zed-industries/zed.git --depth 1

cd zed

cargo build -p theme_importer
BIN=target/debug/theme_importer

for theme in ../themes/tmp/OneDark-Pro*.json; do
    $BIN $theme --output $theme
done

cd ..

uv run merge.py
