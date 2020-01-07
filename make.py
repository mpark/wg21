#!/usr/bin/env python3

import glob
import os
import os.path
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request

self_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
data_dir = 'data'  # pandoc crashes on absolute data directory
out_dir = os.path.join(self_dir, 'generated')


def should_refresh(index_path: str) -> bool:
    try:
        return time.time() - os.path.getmtime(index_path) > 60 * 60 * 12
    except OSError:
        return True


def prepare():
    os.makedirs(out_dir, exist_ok=True)
    index_path = os.path.join(data_dir, 'index.yaml')
    if should_refresh(index_path):
        try:
            urllib.request.urlretrieve("https://wg21.link/index.yaml", filename=index_path)
        except urllib.error.URLError:
            pass  # Will update next time


def cook(file_name: str):
    assert '/' not in file_name and '\\' not in file_name, \
        "Please just provide filenames. The files should be located in the same dir as this script."

    name, _ = os.path.splitext(file_name)
    src_path = os.path.join(self_dir, name + '.md')
    dst_path = os.path.join(out_dir, file_name)
    subprocess.call([
        'pandoc',
        src_path,
        os.path.join(data_dir, 'references.md'),
        '--number-sections',
        '--self-contained',
        '--table-of-contents',
        '--bibliography', os.path.join(data_dir, 'index.yaml'),
        '--csl', os.path.join(data_dir, 'cpp.csl'),
        '--css', os.path.join(data_dir, 'template', '14882.css'),
        '--filter', 'pandoc-citeproc',
        '--filter', os.path.join(data_dir, 'filter', 'wg21.py'),
        '--metadata', 'datadir:' + data_dir,
        '--metadata-file', os.path.join(data_dir, 'metadata.yaml'),
        '--syntax-definition', os.path.join(data_dir, 'syntax', 'isocpp.xml'),
        '--template', os.path.join(data_dir, 'template', 'wg21'),
        '--output', dst_path
    ])


def main():
    prepare()
    file_names = sys.argv[1:]
    if not file_names:
        file_names = glob.glob(os.path.join(self_dir, '*.md'))
        file_names.remove(os.path.join(self_dir, 'README.md'))
        file_names = [os.path.splitext(os.path.basename(x))[0] for x in file_names]
        file_names = [f"{x}.{ext}" for ext in ('latex', 'pdf', 'html') for x in file_names]
    for file_name in file_names:
        cook(file_name)


if __name__ == '__main__':
    main()
