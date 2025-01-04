#!/bin/bash

# 現在のディレクトリとそのサブディレクトリ内のすべての.pyと.mdファイルを検索
find . -type f \( -name "*.py" -o -name "*.md" \) | while read -r file; do
  # BOM付きUTF-8として変換
  # 一時ファイルを作成してから、元のファイルを上書き
  temp_file=$(mktemp)
  echo -e '\xEF\xBB\xBF' | cat - "$file" > "$temp_file"
  mv "$temp_file" "$file"
  echo "Converted: $file"
done

echo "Conversion completed for all .py and .md files."