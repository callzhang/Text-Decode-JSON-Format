# Text Decode + JSON Format (Sublime Text)

Utilities for decoding messy text and formatting JSON in Sublime Text. Includes two commands:

- **Auto Decode**: Iteratively decode URL, HTML entities, Unicode escapes, hex, base64, and gzip.
- **Auto JSON Format**: Decode first, then sanitize string literals, and pretty-print JSON.

## Installation

### Package Control (recommended)
1. Publish this repository publicly on GitHub (name it to match the package, e.g., `Text-Decode-JSON-Format` or similar).
2. Tag a release (e.g., `v1.0.0`).
3. Submit a PR to [`package_control_channel`](https://github.com/wbond/package_control_channel) adding the repo URL to the default channel, using the package name **Text Decode + JSON Format**. After merge, users can run `Package Control: Install Package` and search for that name.

### Manual install
1. Copy `auto_tools.py`, `auto_tools_core.py`, and `auto_tools.sublime-commands` into your Sublime `Packages/User` directory.
2. Use the command palette to run the commands below.

## Commands
- `Auto Decode (URL+HTML+Unicode+Base64+Hex)`: runs `auto_decode`
- `Auto JSON Format (Decode + Fix + Pretty)`: runs `auto_json_format`

Both commands operate on the current selection(s); if nothing is selected, they process the entire buffer.

## Development
- Run tests: `python -m unittest`
- Files of interest:
  - `auto_tools_core.py`: decoding and JSON utilities (pure Python, unit-tested)
  - `auto_tools.py`: Sublime command bindings
  - `auto_tools.sublime-commands`: palette entries
