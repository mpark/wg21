#!/usr/bin/env bash

# MPark.WG21
#
# Copyright Michael Park, 2026-Present
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

set -e
set -o pipefail

: "${PYTHON_DIR:?Set 'PYTHON_DIR' to the directory to install the virtual environment.}"

if [ "$#" -eq 0 ]; then
  echo "Usage: PYTHON_DIR=... $0 pip-args..."
  exit 1
fi

trap 'rm -rf "${PYTHON_DIR}"' EXIT

rm -rf "${PYTHON_DIR}"
python3 -m venv "${PYTHON_DIR}"

"${PYTHON_DIR}/bin/python3" -m pip install --upgrade pip "$@"

trap - EXIT
