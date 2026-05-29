#!/usr/bin/env bash

# MPark.WG21
#
# Copyright Michael Park, 2022
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

set -e
set -o pipefail

: "${PANDOC_VER:?Set 'PANDOC_VER' to the desired version of Pandoc}"
: "${PANDOC_DIR:?Set 'PANDOC_DIR' to the directory to install Pandoc.}"

URL="https://github.com/jgm/pandoc/releases/download/${PANDOC_VER}/"
OS="$(uname -s)"
case "${OS}" in
  Linux)
    ARCHIVE_ROOT="pandoc-${PANDOC_VER}"
    URL+="${ARCHIVE_ROOT}-linux-amd64.tar.gz"
    TAR_ARGS=xz
    ;;
  Darwin)
    ARCHIVE_ROOT="pandoc-${PANDOC_VER}-$(uname -m)"
    URL+="${ARCHIVE_ROOT}-macOS.zip"
    TAR_ARGS=x
    ;;
  *) echo "Unsupported OS: ${OS}."; exit 1 ;;
esac

mkdir -p "${PANDOC_DIR}"
curl -sSL "${URL}" | tar "${TAR_ARGS}" --strip-components 2 -C "${PANDOC_DIR}" "${ARCHIVE_ROOT}/bin"
chmod -R u+x "${PANDOC_DIR}"
