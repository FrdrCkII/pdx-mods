#!/bin/env bash

target_dir="${1:-./common/autonomous_states}"

shopt -s nullglob

cd "$target_dir" || { echo "no dir '$target_dir'" >&2; exit 1; }

for file in *.txt; do
    [[ -f "$file" ]] || continue

    if ! grep -Fqw 'use_overlord_color' "$file"; then
        tmpfile=$(mktemp)
        {
            head -n 1 "$file"
            printf "\tuse_overlord_color = yes\n"
            tail -n +2 "$file"
        } > "$tmpfile"

        mv "$tmpfile" "$file"
    fi
done
