import json
import os
import unittest
from pathlib import Path

import auto_tools_core as core


class AutoToolsCoreTest(unittest.TestCase):
    """Test suite for auto_tools_core decoding and JSON utilities."""

    # ==================== URL Decoding Tests ====================
    def test_auto_decode_url_encoded_chinese(self):
        """Test URL decoding of Chinese characters."""
        self.assertEqual(core.auto_decode_engine("%E4%BD%A0%E5%A5%BD"), "你好")
        self.assertEqual(core.auto_decode_engine("%E4%B8%AD%E6%96%87"), "中文")

    def test_auto_decode_url_encoded_special_chars(self):
        """Test URL decoding of special characters."""
        self.assertEqual(core.auto_decode_engine("%20"), " ")
        self.assertEqual(core.auto_decode_engine("%2F"), "/")
        self.assertEqual(core.auto_decode_engine("%3D"), "=")

    # ==================== HTML Entity Tests ====================
    def test_auto_decode_html_entities(self):
        """Test HTML entity decoding."""
        self.assertEqual(core.auto_decode_engine("foo&amp;bar"), "foo&bar")
        self.assertEqual(core.auto_decode_engine("&lt;tag&gt;"), "<tag>")
        self.assertEqual(core.auto_decode_engine("&quot;text&quot;"), '"text"')
        self.assertEqual(core.auto_decode_engine("&#x4e2d;&#x6587;"), "中文")
        self.assertEqual(core.auto_decode_engine("&#20013;&#25991;"), "中文")

    # ==================== Hex Decoding Tests ====================
    def test_auto_decode_hex(self):
        """Test hex string decoding."""
        self.assertEqual(core.auto_decode_engine("68656c6c6f"), "hello")
        self.assertEqual(core.auto_decode_engine("48656c6c6f20576f726c64"), "Hello World")

    def test_auto_decode_hex_with_spaces(self):
        """Test hex decoding with spaces (should be ignored)."""
        self.assertEqual(core.auto_decode_engine("68 65 6c 6c 6f"), "hello")

    # ==================== Base64 Decoding Tests ====================
    def test_auto_decode_base64(self):
        """Test base64 string decoding."""
        self.assertEqual(core.auto_decode_engine("aGVsbG8="), "hello")
        self.assertEqual(core.auto_decode_engine("SGVsbG8gV29ybGQ="), "Hello World")

    def test_auto_decode_base64_gzip_json_with_chinese(self):
        """Test base64-encoded gzip JSON with Chinese characters."""
        # base64-encoded gzip payload of {"msg": "你好", "value": 123}
        payload = "H4sIANV/QGkC/6tWyi1OV7JSUHqyd8HTpXuVdBSUyhJzSlOBQoZGxrUA9XjiTx8AAAA="
        decoded = core.auto_decode_engine(payload)
        parsed = json.loads(decoded)
        self.assertEqual(parsed["msg"], "你好")
        self.assertEqual(parsed["value"], 123)

    # ==================== Unicode Escape Tests ====================
    def test_auto_decode_unicode_escapes(self):
        """Test Unicode escape sequence decoding."""
        self.assertEqual(core.auto_decode_engine("\\u4e2d\\u6587"), "中文")
        self.assertEqual(core.auto_decode_engine("\\u5f6d\\u65af\\u8bda"), "彭斯诚")

    def test_auto_decode_mixed_literal_and_escapes(self):
        """Test mixed literal text and escape sequences."""
        raw = "彭斯诚 \\u5df2\\u4fdd\\u5b58"
        self.assertEqual(core.auto_decode_engine(raw), "彭斯诚 已保存")

    def test_auto_decode_double_escaped_unicode(self):
        """Test double-escaped Unicode sequences (backslash-u -> unicode -> char)."""
        # This simulates what happens in JSON strings within HTML attributes
        raw = "\\u67b6\\u6784\\u5e08"
        decoded = core.auto_decode_engine(raw)
        self.assertEqual(decoded, "架构师")

    def test_auto_decode_preserves_existing_unicode(self):
        """Test that already-decoded Unicode stays intact."""
        raw = "👤 彭斯诚 架构师"
        self.assertEqual(core.auto_decode_engine(raw), raw)

    # ==================== JSON Sanitize Tests ====================
    def test_json_sanitize_preserves_newlines(self):
        """Test that json_sanitize correctly escapes newlines."""
        raw = '{"msg": "line1\nline2"}'
        sanitized = core.json_sanitize(raw)
        loaded = json.loads(sanitized)
        self.assertEqual(loaded["msg"], "line1\nline2")
        self.assertIn("\\n", sanitized)

    def test_json_sanitize_handles_crlf_correctly(self):
        """Test that \\r\\n is converted to single \\n, not double."""
        raw = '{"msg": "line1\r\nline2"}'
        sanitized = core.json_sanitize(raw)
        loaded = json.loads(sanitized)
        self.assertEqual(loaded["msg"], "line1\nline2")
        self.assertNotEqual(loaded["msg"], "line1\n\nline2")

    def test_json_sanitize_handles_carriage_return(self):
        """Test that \\r alone is converted to \\n."""
        raw = '{"msg": "line1\rline2"}'
        sanitized = core.json_sanitize(raw)
        loaded = json.loads(sanitized)
        self.assertEqual(loaded["msg"], "line1\nline2")

    def test_json_sanitize_preserves_valid_json(self):
        """Test that already-valid JSON is preserved."""
        valid_json = '{"key": "value", "num": 123}'
        sanitized = core.json_sanitize(valid_json)
        loaded = json.loads(sanitized)
        self.assertEqual(loaded["key"], "value")
        self.assertEqual(loaded["num"], 123)

    def test_json_sanitize_handles_multiple_strings(self):
        """Test sanitization with multiple string values."""
        raw = '{"a": "line1\nline2", "b": "line3\r\nline4"}'
        sanitized = core.json_sanitize(raw)
        loaded = json.loads(sanitized)
        self.assertEqual(loaded["a"], "line1\nline2")
        self.assertEqual(loaded["b"], "line3\nline4")

    # ==================== JSON Pretty Tests ====================
    def test_json_pretty_formats(self):
        """Test JSON pretty printing."""
        pretty = core.json_pretty('{"a":1,"b":2}')
        self.assertEqual(pretty, '{\n  "a": 1,\n  "b": 2\n}')

    def test_json_pretty_preserves_unicode(self):
        """Test that pretty printing preserves non-ASCII characters."""
        pretty = core.json_pretty('{"msg":"你好","value":123}')
        parsed = json.loads(pretty)
        self.assertEqual(parsed["msg"], "你好")
        self.assertEqual(parsed["value"], 123)
        self.assertIn("你好", pretty)

    def test_json_pretty_handles_invalid_json(self):
        """Test that invalid JSON is returned unchanged."""
        invalid = "not json at all"
        result = core.json_pretty(invalid)
        self.assertEqual(result, invalid)

    # ==================== Full Pipeline Tests ====================
    def test_full_pipeline_on_urlencoded_json_with_chinese_and_newline(self):
        """Test complete pipeline: decode -> sanitize -> pretty."""
        urlencoded = "%7B%22msg%22%3A%22%E4%BD%A0%E5%A5%BD%5Cnline2%22%2C%22value%22%3A123%7D"
        decoded = core.auto_decode_engine(urlencoded)
        sanitized = core.json_sanitize(decoded)
        pretty = core.json_pretty(sanitized)

        parsed = json.loads(pretty)
        self.assertEqual(parsed["msg"], "你好\nline2")
        self.assertEqual(parsed["value"], 123)
        self.assertIn("\n  \"msg\"", pretty)

    def test_full_pipeline_on_html_with_embedded_json(self):
        """Test decoding HTML with embedded JSON in attributes."""
        html_with_json = 'hx-vals=\'{"name": "\\u5f6d\\u65af\\u8bda", "job": "\\u67b6\\u6784\\u5e08"}\''
        decoded = core.auto_decode_engine(html_with_json)
        # Should decode the Unicode escapes
        self.assertIn("彭斯诚", decoded)
        self.assertIn("架构师", decoded)

    # ==================== Edge Cases ====================
    def test_auto_decode_empty_string(self):
        """Test decoding empty string."""
        self.assertEqual(core.auto_decode_engine(""), "")

    def test_auto_decode_plain_text(self):
        """Test that plain text without encoding is unchanged."""
        plain = "This is plain text"
        self.assertEqual(core.auto_decode_engine(plain), plain)

    def test_auto_decode_multiple_passes(self):
        """Test that multiple encoding layers are decoded."""
        # URL-encoded Unicode escapes
        double_encoded = "%5Cu4e2d%5Cu6587"
        decoded = core.auto_decode_engine(double_encoded)
        self.assertEqual(decoded, "中文")

    def test_json_sanitize_empty_string(self):
        """Test sanitization of empty string value."""
        raw = '{"msg": ""}'
        sanitized = core.json_sanitize(raw)
        loaded = json.loads(sanitized)
        self.assertEqual(loaded["msg"], "")

    def test_json_sanitize_escaped_quotes(self):
        """Test that escaped quotes in strings are preserved."""
        raw = '{"msg": "He said \\"hello\\""}'
        sanitized = core.json_sanitize(raw)
        loaded = json.loads(sanitized)
        self.assertEqual(loaded["msg"], 'He said "hello"')

    # ==================== Real-world Test Cases ====================
    def test_real_world_text_file(self):
        """Test decoding the actual text.txt file from tests directory."""
        test_file = Path(__file__).parent / "text.txt"
        if not test_file.exists():
            self.skipTest("text.txt not found")

        with open(test_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Decode the text
        decoded = core.auto_decode_engine(text)

        # Extract JSON from hx-vals attribute
        import re
        match = re.search(r'hx-vals=[\'"](.*?)[\'"]', decoded)
        if match:
            json_str = match.group(1)
            # Find the JSON object
            start = json_str.find('{')
            if start >= 0:
                brace_count = 0
                json_obj = ""
                for i in range(start, len(json_str)):
                    if json_str[i] == '{':
                        brace_count += 1
                    elif json_str[i] == '}':
                        brace_count -= 1
                    json_obj += json_str[i]
                    if brace_count == 0:
                        break

                # Should be valid JSON
                parsed = json.loads(json_obj)
                self.assertIn("candidate", parsed)
                self.assertEqual(parsed["candidate"]["name"], "彭斯诚")
                self.assertEqual(parsed["candidate"]["job_applied"], "架构师")

    def test_json_extraction_from_html(self):
        """Test decoding HTML text with embedded JSON."""
        html_text = 'some html <div hx-vals=\'{"key": "value"}\'>content</div>'
        decoded = core.auto_decode_engine(html_text)
        
        # The decoded text should still contain the HTML structure
        self.assertIn("some html", decoded)
        self.assertIn("hx-vals", decoded)
        self.assertIn('"key"', decoded)
        self.assertIn('"value"', decoded)
        
        # Extract and format just the JSON part
        import re
        match = re.search(r'\{[^}]+\}', decoded)
        if match:
            json_str = match.group(0)
            sanitized = core.json_sanitize(json_str)
            pretty = core.json_pretty(sanitized)
            parsed = json.loads(pretty)
            self.assertEqual(parsed["key"], "value")


if __name__ == "__main__":
    unittest.main()
