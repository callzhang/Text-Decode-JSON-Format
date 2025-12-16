# Text Decode + JSON Format (Sublime Text)

Sublime Text commands that rescue mangled payloads (URLs, HTML entities, Unicode escapes, hex/base64, even gzip’d blobs) and turn them into readable text or pretty JSON—great for API logs, scraped pages, and double-encoded data.

- **Auto Decode**: Iteratively unwrap URL, HTML, Unicode escape sequences, hex, base64, and gzip.
- **Auto JSON Format**: Runs Auto Decode, fixes string literal escapes, then pretty-prints JSON with non‑ASCII preserved.

## Installation

### Local Installation Script (easiest)

**macOS/Linux:**
```bash
./install.sh
```

**With custom path:**
```bash
./install.sh --path ~/Library/Application\ Support/Sublime\ Text/Packages/User
```

**Help:**
```bash
./install.sh --help
```

The script will automatically:
- Find your Sublime Text `Packages/User` directory
- Copy all necessary files
- Provide installation confirmation

### Package Control (recommended for distribution)
Once the package is in the default channel, run `Package Control: Install Package` and search for **Text Decode + JSON Format**.

### Install via custom source (before channel merge)
1. In Sublime, run `Package Control: Add Repository` and paste `https://github.com/callzhang/Text-Decode-JSON-Format`.
2. Run `Package Control: Install Package` and search for **Text Decode + JSON Format**.
3. Remove the custom repository later if desired via `Package Control: Remove Repository`.

### Manual install
1. Copy `auto_tools.py`, `auto_tools_core.py`, and `auto_tools.sublime-commands` into your Sublime `Packages/User` directory.
2. Use the command palette to run the commands below.

## Commands
- `Auto Decode (URL+HTML+Unicode+Base64+Hex)`: command `auto_decode`
- `Auto JSON Format (Decode + Fix + Pretty)`: command `auto_json_format`

Both commands operate on the current selection(s); if nothing is selected, they process the entire buffer.

## Quick start
1) Select the garbled text (or nothing to process the whole file).  
2) Open the Command Palette → run `Auto Decode` or `Auto JSON Format`.  
3) The result replaces your selection.

## Typical examples

### 1) URL-encoded Chinese
Input: `%E4%BD%A0%E5%A5%BD`  
`Auto Decode` → `你好`

### 2) HTML entities
Input: `foo&amp;bar`  
`Auto Decode` → `foo&bar`

### 3) Base64 + gzip JSON blob
Input: `H4sIANV/QGkC/6tWyi1OV7JSUHqyd8HTpXuVdBSUyhJzSlOBQoZGxrUA9XjiTx8AAAA=`  
`Auto Decode` → `{"msg": "你好", "value": 123}`

### 4) Mixed literal + escaped text
Input: `彭斯诚 \\u5df2\\u4fdd\\u5b58`  
`Auto Decode` → `彭斯诚 已保存`

### 5) Full pipeline to pretty JSON
Input: `%7B%22msg%22%3A%22%E4%BD%A0%E5%A5%BD%5Cnline2%22%2C%22value%22%3A123%7D`  
`Auto JSON Format` → 
```json
{
  "msg": "你好\nline2",
  "value": 123
}
```

## Notes & tips
- Unicode-safe: already-decoded Chinese/emoji stay intact while escape sequences still get resolved.
- Gzip: base64-encoded gzip blobs are detected and decompressed automatically.
- JSON sanitizer: normalizes `\r\n`/`\r` to `\n` inside strings so pretty-print stays valid.

## Development
- Run tests: `python -m pytest` (or `python -m unittest`)
- Key files:
  - `auto_tools_core.py`: decoding + JSON utilities (pure Python, unit tests)
  - `auto_tools.py`: Sublime command bindings
  - `auto_tools.sublime-commands`: palette entries

## Release log
- **v1.0.2**: Safer Unicode escape handling (prevents mojibake) and additional coverage.
- **v1.0.1**: Install docs update.
- **v1.0.0**: Initial release.
