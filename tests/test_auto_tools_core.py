import json
import unittest

import auto_tools_core as core


class AutoToolsCoreTest(unittest.TestCase):
    def test_auto_decode_url_and_html(self):
        self.assertEqual(core.auto_decode_engine("%E4%BD%A0%E5%A5%BD"), "你好")
        self.assertEqual(core.auto_decode_engine("foo&amp;bar"), "foo&bar")

    def test_auto_decode_hex_and_base64(self):
        self.assertEqual(core.auto_decode_engine("68656c6c6f"), "hello")
        self.assertEqual(core.auto_decode_engine("aGVsbG8="), "hello")

    def test_auto_decode_base64_gzip_json_with_chinese(self):
        # base64-encoded gzip payload of {"msg": "你好", "value": 123}
        payload = "H4sIANV/QGkC/6tWyi1OV7JSUHqyd8HTpXuVdBSUyhJzSlOBQoZGxrUA9XjiTx8AAAA="
        decoded = core.auto_decode_engine(payload)
        parsed = json.loads(decoded)
        self.assertEqual(parsed["msg"], "你好")
        self.assertEqual(parsed["value"], 123)

    def test_json_sanitize_preserves_newlines(self):
        raw = '{"msg": "line1\nline2"}'
        sanitized = core.json_sanitize(raw)
        loaded = json.loads(sanitized)
        self.assertEqual(loaded["msg"], "line1\nline2")
        self.assertIn("\\n", sanitized)

    def test_full_pipeline_on_urlencoded_json_with_chinese_and_newline(self):
        urlencoded = "%7B%22msg%22%3A%22%E4%BD%A0%E5%A5%BD%5Cnline2%22%2C%22value%22%3A123%7D"
        decoded = core.auto_decode_engine(urlencoded)
        sanitized = core.json_sanitize(decoded)
        pretty = core.json_pretty(sanitized)

        parsed = json.loads(pretty)
        self.assertEqual(parsed["msg"], "你好\nline2")
        self.assertEqual(parsed["value"], 123)
        self.assertIn("\n  \"msg\"", pretty)

    def test_json_pretty_formats(self):
        pretty = core.json_pretty('{"a":1,"b":2}')
        self.assertEqual(pretty, '{\n  "a": 1,\n  "b": 2\n}')


if __name__ == "__main__":
    unittest.main()
