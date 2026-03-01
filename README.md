# file-utilities

File security toolkit: bulk VirusTotal scanner, ZIP file scanner, PDF compressor.

## Scripts

| Script | Description |
|--------|-------------|
| `VIRUSTOTAL.py` | Scan a single file or URL against VirusTotal (70+ antivirus engines via REST API) |
| `virus-total-folders.py` | Recursively scan every file in a folder via VirusTotal API — outputs a pass/fail report |
| `virustota-zipfile.py` | Extract a ZIP archive in memory and scan all contained files without writing to disk |
| `compresspdf.py` | Compress PDF files to reduce size using Ghostscript; preserves formatting |

## Prerequisites

- Python 3.9+
- VirusTotal API key (free tier available — 4 requests/min, 500/day)
- Ghostscript installed for PDF compression: `gs --version`

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # add VIRUSTOTAL_API_KEY
```

## Usage

```bash
# Scan a single file
python VIRUSTOTAL.py --file /path/to/file.exe

# Scan entire folder
python virus-total-folders.py --folder /path/to/folder

# Scan contents of a ZIP
python virustota-zipfile.py --zip /path/to/archive.zip

# Compress a PDF
python compresspdf.py --input report.pdf --output report_compressed.pdf
```

## Notes

- Free VirusTotal API: 4 lookups/minute. Scripts include rate-limiting delays automatically.
- Large folders will take time — the scripts log progress and skip already-scanned files.

## Built with

Python · VirusTotal API · Ghostscript  
AI-assisted development (Claude, GitHub Copilot) — architecture, requirements, QA validation and debugging by me.
