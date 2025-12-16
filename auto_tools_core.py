import urllib.parse
import html
import codecs
import base64
import gzip
import json
import re
from io import BytesIO


# ---------------------------
# Detection helpers
# ---------------------------
def looks_like_base64(s):
    s = s.strip().replace("\n", "")
    if not re.match(r'^[A-Za-z0-9+/=]+$', s):
        return False
    return len(s) % 4 == 0


def looks_like_hex(s):
    s = s.replace(" ", "").replace("\n", "")
    return len(s) >= 4 and bool(re.match(r'^[0-9a-fA-F]+$', s)) and len(s) % 2 == 0


def try_decode_hex(s):
    try:
        raw = bytes.fromhex(s)
        return raw.decode("utf-8")
    except Exception:
        return s


def try_decode_base64(s):
    try:
        raw = base64.b64decode(s, validate=True)
        try:
            return raw.decode("utf-8")
        except Exception:
            return raw
    except Exception:
        return s


def try_decode_gzip(raw):
    try:
        bio = BytesIO(raw)
        with gzip.GzipFile(fileobj=bio) as f:
            return f.read().decode("utf-8")
    except Exception:
        return None


# ---------------------------
# Multi-pass AUTO-DECODE ENGINE
# ---------------------------
def auto_decode_engine(text):
    prev = None
    cur = text

    for _ in range(10):
        prev = cur

        # Decode explicit escape sequences without re-interpreting already
        # decoded non-ASCII characters (which would produce mojibake).
        if "\\u" in cur or "\\n" in cur or "\\t" in cur or "\\x" in cur:
            def _unescape(match):
                frag = match.group(0)
                try:
                    return bytes(frag, "utf-8").decode("unicode_escape")
                except Exception:
                    return frag

            cur = re.sub(
                r"\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8}|\\x[0-9a-fA-F]{2}|\\[nrtfb\"\\]",
                _unescape,
                cur,
            )

        if "%" in cur:
            try:
                tmp = urllib.parse.unquote(cur)
                if tmp != cur:
                    cur = tmp
            except Exception:
                pass

        if "&" in cur:
            tmp = html.unescape(cur)
            if tmp != cur:
                cur = tmp

        stripped = cur.strip()

        if looks_like_hex(stripped):
            tmp = try_decode_hex(stripped)
            if tmp != stripped:
                cur = tmp

        if looks_like_base64(stripped):
            tmp = try_decode_base64(stripped)
            if tmp != stripped:
                if isinstance(tmp, bytes):
                    gz = try_decode_gzip(tmp)
                    if gz:
                        cur = gz
                    else:
                        try:
                            cur = tmp.decode("utf-8")
                        except Exception:
                            pass
                else:
                    cur = tmp

        if cur == prev:
            break

    return cur


# ---------------------------
# JSON sanitizer
# ---------------------------
def json_sanitize(s):
    def fix_string(m):
        inner = m.group(1)
        # Handle \r\n as a single unit first to avoid double newline
        inner = inner.replace("\r\n", "\\n")
        inner = inner.replace("\r", "\\n")
        inner = inner.replace("\n", "\\n")
        return '"' + inner + '"'

    return re.sub(r'"([^"\\]*(?:\\.[^"\\]*)*)"', fix_string, s)


# ---------------------------
# Pretty JSON
# ---------------------------
def json_pretty(s):
    try:
        obj = json.loads(s)
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return s
