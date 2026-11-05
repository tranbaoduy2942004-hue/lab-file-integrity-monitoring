#!/bin/bash
set -euo pipefail

DIR=/home/ubuntu/fim-lab
CFG="$DIR/app.conf"
BACKUP="$DIR/baseline.conf"
LOG="$DIR/actions.log"

hash() {
    sha256sum "$1" | cut -d' ' -f1
}

case "${1:-}" in
  baseline)
    if [ -e "$CFG" ] || [ -e "$BACKUP" ]; then
        echo "BASELINE_ALREADY_EXISTS"; exit 1
    fi
    printf 'service=web\naudit=enabled\nauth=required\n' > "$BACKUP"
    cp "$BACKUP" "$CFG"
    echo "BASELINE_CREATED sha256=$(hash "$CFG")" | tee -a "$LOG"
    ;;

  tamper)
    test -f "$BACKUP" && test -f "$CFG"
    cmp -s "$BACKUP" "$CFG" || {
        echo "STOP: FILE_ALREADY_MODIFIED"; exit 1;
    }
    sed -i 's/^audit=enabled$/audit=disabled/' "$CFG"
    grep -Fxq 'audit=disabled' "$CFG"
    echo "UNAUTHORIZED_CHANGE sha256=$(hash "$CFG")" | tee -a "$LOG"
    ;;

  restore)
    test -f "$BACKUP"
    cp "$BACKUP" "$CFG"
    cmp -s "$BACKUP" "$CFG"
    echo "FILE_RESTORED sha256=$(hash "$CFG")" | tee -a "$LOG"
    ;;

  status)
    echo "=== CONFIG ==="
    cat "$CFG"
    echo "=== SHA256 ==="
    hash "$CFG"
    echo "=== BASELINE SHA256 ==="
    hash "$BACKUP"
    ;;

  *)
    echo "Usage: manage_fim.sh baseline|tamper|restore|status"
    exit 2
    ;;
esac
