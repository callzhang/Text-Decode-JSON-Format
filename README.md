# Text Decode + JSON Format (Sublime Text)

Utilities for decoding messy text and formatting JSON in Sublime Text. Includes two commands:

- **Auto Decode**: Iteratively decode URL, HTML entities, Unicode escapes, hex, base64, and gzip.
- **Auto JSON Format**: Decode first, then sanitize string literals, and pretty-print JSON.

## Installation

### Package Control (recommended)
Once the package is in the default channel, run `Package Control: Install Package` and search for **Text Decode + JSON Format**.

### Install via custom source (before channel merge)
1. In Sublime, run `Package Control: Add Repository` and paste `https://github.com/callzhang/Text-Decode-JSON-Format`.
2. Run `Package Control: Install Package` and search for **Text Decode + JSON Format**.
3. Remove the custom repository later if desired via `Package Control: Remove Repository`.

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
