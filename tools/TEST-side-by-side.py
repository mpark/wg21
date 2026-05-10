#!/usr/bin/env python3
"""Generate a split Markdown/rendered-HTML view aligned on major block starts."""

from __future__ import annotations

import html
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = ROOT / "Makefile"
MARKDOWN = ROOT / "TEST.md"

HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
DIV_FENCE_RE = re.compile(r"^:::+")


def block_syncs(lines: list[str]) -> dict[int, dict[str, int | str]]:
    syncs: dict[int, dict[str, int | str]] = {}
    in_front_matter = False
    in_fence = False
    div_depth = 0
    fence_marker = ""
    fence_start = 0
    div_start = 0
    next_sync = 1

    for line_no, line in enumerate(lines, start=1):
        stripped = line.rstrip("\n")

        if line_no == 1 and stripped == "---":
            in_front_matter = True
            continue
        if in_front_matter:
            if stripped == "---":
                in_front_matter = False
            continue

        if DIV_FENCE_RE.match(stripped):
            if div_depth == 0 and stripped.strip() != ":::":
                syncs[line_no] = {"id": f"b{next_sync}", "end": line_no}
                next_sync += 1
                div_start = line_no
            if stripped.strip() == ":::":
                if div_depth == 1 and div_start:
                    syncs[div_start]["end"] = line_no
                    div_start = 0
                div_depth = max(0, div_depth - 1)
            else:
                div_depth += 1
            continue

        if div_depth:
            continue

        fence_match = FENCE_RE.match(stripped)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                syncs[line_no] = {"id": f"b{next_sync}", "end": line_no}
                next_sync += 1
                in_fence = True
                fence_marker = marker[0]
                fence_start = line_no
            elif marker.startswith(fence_marker * 3):
                if fence_start:
                    syncs[fence_start]["end"] = line_no
                    fence_start = 0
                in_fence = False
                fence_marker = ""
            continue

        if in_fence:
            continue

        if HEADING_RE.match(stripped):
            syncs[line_no] = {"id": f"b{next_sync}", "end": line_no}
            next_sync += 1

    return syncs


def instrument_markdown(lines: list[str], syncs: dict[int, dict[str, int | str]]) -> str:
    out: list[str] = []
    for line_no, line in enumerate(lines, start=1):
        meta = syncs.get(line_no)
        if meta is not None:
            out.append(
                f'<!--SYNC {meta["id"]} {line_no} {meta["end"]}-->\n\n'
            )
        out.append(line)
    return "".join(out)


def source_pane(lines: list[str], syncs: dict[int, dict[str, int | str]]) -> str:
    out = ['<pre class="source-content">']
    for line_no, line in enumerate(lines, start=1):
        attrs = [f'class="source-line"', f'id="src-L{line_no}"', f'data-src-line="{line_no}"']
        meta = syncs.get(line_no)
        if meta is not None:
            attrs.append(f'data-sync="{meta["id"]}"')
            attrs.append(f'data-sync-end="{meta["end"]}"')
        escaped = html.escape(line.rstrip("\n")) or " "
        out.append(
            f'<span {" ".join(attrs)}><span class="source-text">{escaped}</span></span>'
        )
    out.append("</pre>")
    return "".join(out)


def extract_between(text: str, start_pat: str, end_pat: str, name: str) -> str:
    start = re.search(start_pat, text, flags=re.IGNORECASE | re.DOTALL)
    end = re.search(end_pat, text, flags=re.IGNORECASE | re.DOTALL)
    if start is None or end is None or start.end() > end.start():
        raise ValueError(f"could not extract {name} from generated HTML")
    return text[start.end() : end.start()]


def render_markdown_with_make(markdown: Path, output: Path, make: str) -> None:
    subprocess.run(
        [
            make,
            "-f",
            str(MAKEFILE),
            f"SRCDIR={markdown.parent}",
            f"OUTDIR={output.parent}",
            str(output),
        ],
        cwd=ROOT,
        stdout=sys.stderr,
        stderr=sys.stderr,
        check=True,
    )


def build_split_page(rendered_html: str, source_html: str) -> str:
    head = extract_between(rendered_html, r"<head[^>]*>", r"</head>", "head")
    body = extract_between(rendered_html, r"<body[^>]*>", r"</body>", "body")
    body = re.sub(
        r"<!--SYNC ([^ ]+) ([0-9]+) ([0-9]+)-->",
        r'<span class="sync-point" data-sync="\1" data-src-line="\2" data-src-end="\3"></span>',
        body,
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head}
<style>
html, body {{
  margin: 0 !important;
  height: 100%;
}}
body {{
  overflow: hidden;
  background: #fff;
}}
.split-view {{
  display: grid;
  grid-template-columns: minmax(24rem, 1fr) minmax(24rem, 1fr);
  height: 100vh;
}}
.source-pane,
.render-pane {{
  overflow: auto;
  height: 100vh;
  box-sizing: border-box;
}}
.source-pane {{
  border-right: 1px solid #c8cdd2;
  background: #f6f8fa;
}}
.render-pane {{
  background: #fff;
}}
.source-content {{
  margin: 0;
  padding: 0.75rem 0 2rem;
  font: 13px/1.35 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  tab-size: 2;
  white-space: pre;
}}
.source-line {{
  display: block;
  box-sizing: border-box;
  min-height: 1.35em;
  padding: 0 0.75rem;
}}
.source-line[data-sync] {{
  background: #fff4bf;
}}
.source-text {{
  color: #1f2933;
}}
.render-pane > .render-content {{
  padding: 0 1rem 3rem;
}}
.render-pane .wrapper {{
  position: relative;
  margin-top: 3rem;
  margin-bottom: 3rem;
}}
.render-pane li {{
  position: relative;
}}
.sync-point {{
  display: block;
  height: 0;
  overflow: hidden;
}}
.sync-spacer {{
  display: block;
  height: var(--sync-height, 0px);
}}
@media (max-width: 900px) {{
  .split-view {{
    grid-template-columns: 1fr;
    grid-template-rows: 50vh 50vh;
  }}
  .source-pane,
  .render-pane {{
    height: 50vh;
  }}
  .source-pane {{
    border-right: 0;
    border-bottom: 1px solid #c8cdd2;
  }}
}}
</style>
</head>
<body data-syntax-highlighting="on" data-deleted-text="show">
<main class="split-view">
  <section class="source-pane" aria-label="Markdown source">
{source_html}
  </section>
  <section class="render-pane" aria-label="Rendered HTML">
    <div class="render-content">
{body}
    </div>
  </section>
</main>
<script>
(() => {{
  const leftPane = document.querySelector('.source-pane');
  const rightPane = document.querySelector('.render-pane');

  function clearSpacers() {{
    document.querySelectorAll('.sync-spacer').forEach((el) => el.remove());
  }}

  function spacer(height) {{
    const el = document.createElement('span');
    el.className = 'sync-spacer';
    el.style.setProperty('--sync-height', `${{Math.max(0, height)}}px`);
    return el;
  }}

  function topInPane(el, pane) {{
    const elRect = el.getBoundingClientRect();
    const paneRect = pane.getBoundingClientRect();
    return elRect.top - paneRect.top + pane.scrollTop;
  }}

  function centerInPane(el, pane) {{
    return topInPane(el, pane) + el.getBoundingClientRect().height / 2;
  }}

  function sourceCenterInPane(start, pane) {{
    const endLine = start.dataset.syncEnd;
    const end = endLine ? document.getElementById(`src-L${{endLine}}`) : null;
    if (!end || end === start) return centerInPane(start, pane);
    const startTop = topInPane(start, pane);
    const endBottom = topInPane(end, pane) + end.getBoundingClientRect().height;
    return (startTop + endBottom) / 2;
  }}

  function alignHeadings() {{
    clearSpacers();
    const rightPoints = [...document.querySelectorAll('.render-pane .sync-point[data-sync]')];
    for (const right of rightPoints) {{
      const sync = right.dataset.sync;
      const left = document.querySelector(`.source-pane .source-line[data-sync="${{sync}}"]`);
      if (!left) continue;
      const rightTarget = right.nextElementSibling || right;
      const leftCenter = sourceCenterInPane(left, leftPane);
      const rightCenter = centerInPane(rightTarget, rightPane);
      const diff = rightCenter - leftCenter;
      if (diff > 1) {{
        left.before(spacer(diff));
      }} else if (diff < -1) {{
        right.before(spacer(-diff));
      }}
    }}
  }}

  let syncing = false;
  function mirrorScroll(from, to) {{
    if (syncing) return;
    syncing = true;
    to.scrollTop = from.scrollTop;
    requestAnimationFrame(() => {{ syncing = false; }});
  }}

  leftPane.addEventListener('scroll', () => mirrorScroll(leftPane, rightPane));
  rightPane.addEventListener('scroll', () => mirrorScroll(rightPane, leftPane));

  window.addEventListener('load', alignHeadings);
  window.addEventListener('resize', () => requestAnimationFrame(alignHeadings));
  alignHeadings();
}})();
</script>
</body>
</html>
"""


def main() -> None:
    markdown = MARKDOWN

    lines = markdown.read_text(encoding="utf-8").splitlines(keepends=True)
    syncs = block_syncs(lines)

    with tempfile.TemporaryDirectory(prefix="wg21-header-split-") as tmp:
        tmpdir = Path(tmp)
        srcdir = tmpdir / "src"
        outdir = tmpdir / "out"
        srcdir.mkdir()
        outdir.mkdir()
        instrumented = srcdir / markdown.name
        rendered = outdir / f"{markdown.stem}.html"
        instrumented.write_text(instrument_markdown(lines, syncs), encoding="utf-8")
        render_markdown_with_make(instrumented, rendered, "make")
        split = build_split_page(
            rendered.read_text(encoding="utf-8"),
            source_pane(lines, syncs),
        )

    sys.stdout.write(split)
    print(f"aligned {len(syncs)} block starts", file=sys.stderr)


if __name__ == "__main__":
    main()
