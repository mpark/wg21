#!/usr/bin/env bash

# MPark.WG21
#
# Copyright Michael Park, 2026
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

set -e

: "${REVEALJS_VER:?Set 'REVEALJS_VER' to the desired version of Reveal.js}"
: "${REVEALJS_SHA256:?Set 'REVEALJS_SHA256' to the expected archive checksum}"
: "${REVEALJS_DIR:?Set 'REVEALJS_DIR' to the directory to install Reveal.js}"

URL="https://registry.npmjs.org/reveal.js/-/reveal.js-${REVEALJS_VER}.tgz"
mkdir -p "$(dirname "${REVEALJS_DIR}")"
INSTALL_DIR="$(mktemp -d "${REVEALJS_DIR}.tmp.XXXXXX")"
ARCHIVE="${INSTALL_DIR}/reveal.js.tgz"
trap 'rm -rf "${INSTALL_DIR}"' EXIT

curl -fsSL "${URL}" -o "${ARCHIVE}"
ACTUAL_SHA256="$(python3 -c \
  'import hashlib, pathlib, sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())' \
  "${ARCHIVE}")"
if [[ "${ACTUAL_SHA256}" != "${REVEALJS_SHA256}" ]]; then
  echo "Unexpected checksum for Reveal.js ${REVEALJS_VER}: ${ACTUAL_SHA256}" >&2
  exit 1
fi

tar xzf "${ARCHIVE}" --strip-components 1 -C "${INSTALL_DIR}"
rm "${ARCHIVE}"
rm -rf "${REVEALJS_DIR}"
mv "${INSTALL_DIR}" "${REVEALJS_DIR}"

trap - EXIT
