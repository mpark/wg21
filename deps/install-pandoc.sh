#!/usr/bin/env bash

: "${PANDOC_VER:?Set 'PANDOC_VER' to the desired version of Pandoc}"
: "${PANDOC_DIR:?Set 'PANDOC_DIR' to the directory to install Pandoc.}"

URL="https://github.com/jgm/pandoc/releases/download/${PANDOC_VER}/"
OS="$(uname -s)"
case "${OS}" in
  Linux ) URL+="pandoc-${PANDOC_VER}-linux-amd64.tar.gz"  ;;
  Darwin) URL+="pandoc-${PANDOC_VER}-macOS.zip"           ;;
  *     ) echo "Unspported OS: ${OS}."; exit 1 ;;
esac

mkdir -p "${PANDOC_DIR}"
curl -sSL "${URL}" | tar xz --strip-components 2 -C "${PANDOC_DIR}" -m - "pandoc-${PANDOC_VER}/bin"
chmod -R u+x "${PANDOC_DIR}"
