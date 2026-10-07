"""Build the teaching guide PDF from its Markdown source on Windows."""

from __future__ import annotations

import html
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Docs" / "project_walkthrough.md"
OUTPUT = ROOT / "Docs" / "project_walkthrough.pdf"


def find_browser() -> str | None:
    """Find an installed Chromium-based browser executable."""
    candidates = [
        Path(os.environ.get("PROGRAMFILES(X86)", ""))
        / "Microsoft"
        / "Edge"
        / "Application"
        / "msedge.exe",
        Path(os.environ.get("PROGRAMFILES", ""))
        / "Microsoft"
        / "Edge"
        / "Application"
        / "msedge.exe",
        Path(os.environ.get("LOCALAPPDATA", ""))
        / "Microsoft"
        / "Edge"
        / "Application"
        / "msedge.exe",
        Path(os.environ.get("PROGRAMFILES", ""))
        / "Google"
        / "Chrome"
        / "Application"
        / "chrome.exe",
        Path(os.environ.get("LOCALAPPDATA", ""))
        / "Google"
        / "Chrome"
        / "Application"
        / "chrome.exe",
    ]
    for candidate in candidates:
        if str(candidate.parent) not in ("", ".") and candidate.is_file():
            return str(candidate)
    return shutil.which("msedge") or shutil.which("chrome") or shutil.which("chromium")


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Guide source not found: {SOURCE}")

    browser = find_browser()
    if browser is None:
        raise FileNotFoundError(
            "Microsoft Edge or Google Chrome is required to print the guide to PDF."
        )

    body = markdown.markdown(
        SOURCE.read_text(encoding="utf-8"),
        extensions=["tables", "fenced_code", "toc"],
        output_format="html",
    )
    base_uri = html.escape(ROOT.as_uri() + "/", quote=True)
    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<base href="{base_uri}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Swiggy Business &amp; Operations Analytics - Teaching Guide</title>
<style>
@page {{
  size: A4;
  margin: 16mm 15mm 19mm;
  @bottom-right {{
    content: "Swiggy Analytics | " counter(page);
    color: #64748b;
    font: 8pt Arial, sans-serif;
  }}
}}
* {{ box-sizing: border-box; }}
body {{
  color: #172033;
  font: 10pt/1.48 Arial, Helvetica, sans-serif;
  max-width: 100%;
}}
h1, h2, h3, h4 {{ color: #0b3b57; line-height: 1.2; page-break-after: avoid; }}
h1 {{ font-size: 25pt; border-bottom: 3px solid #f38b24; padding-bottom: 8pt; }}
h2 {{ font-size: 17pt; margin-top: 22pt; border-bottom: 1px solid #dbe3ea; padding-bottom: 4pt; }}
h3 {{ font-size: 12pt; margin-top: 15pt; }}
p, li {{ orphans: 3; widows: 3; }}
blockquote {{
  margin: 12pt 0;
  padding: 8pt 12pt;
  border-left: 4px solid #f38b24;
  background: #fff6eb;
}}
table {{ border-collapse: collapse; width: 100%; margin: 9pt 0 13pt; font-size: 8.5pt; }}
thead {{ display: table-header-group; }}
th {{ background: #0b3b57; color: white; text-align: left; }}
th, td {{ border: 1px solid #cbd5e1; padding: 5pt 6pt; vertical-align: top; }}
tr {{ page-break-inside: avoid; }}
code {{ font-family: Consolas, "Courier New", monospace; font-size: 8.7pt; }}
pre {{
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  background: #f1f5f9;
  border: 1px solid #dbe3ea;
  border-radius: 4px;
  padding: 9pt;
  page-break-inside: avoid;
}}
pre code {{ font-size: 8pt; }}
a {{ color: #075985; text-decoration: underline; }}
img {{ max-width: 100%; max-height: 120mm; object-fit: contain; }}
hr {{ border: 0; border-top: 1px solid #dbe3ea; }}
@media screen {{
  body {{ max-width: 900px; margin: 32px auto; padding: 36px; }}
}}
</style>
</head>
<body>
{body}
</body>
</html>"""

    with tempfile.TemporaryDirectory(prefix="swiggy-guide-") as temp_dir:
        html_path = Path(temp_dir) / "project_walkthrough.html"
        profile_path = Path(temp_dir) / "browser-profile"
        html_path.write_text(document, encoding="utf-8")
        result = subprocess.run(
            [
                browser,
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--user-data-dir={profile_path}",
                f"--print-to-pdf={OUTPUT}",
                html_path.as_uri(),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0 or not OUTPUT.is_file() or OUTPUT.stat().st_size == 0:
            details = (result.stderr or result.stdout).strip()
            raise RuntimeError(f"PDF generation failed: {details or result.returncode}")

    print(f"Created {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
