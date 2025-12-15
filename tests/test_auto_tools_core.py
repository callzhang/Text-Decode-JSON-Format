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

    def test_json_sanitize_preserves_newlines(self):
        raw = '{"msg": "line1\nline2"}'
        sanitized = core.json_sanitize(raw)
        loaded = json.loads(sanitized)
        self.assertEqual(loaded["msg"], "line1\nline2")
        self.assertIn("\\n", sanitized)

    def test_json_pretty_formats(self):
        pretty = core.json_pretty('{"a":1,"b":2}')
        self.assertEqual(pretty, '{\n  "a": 1,\n  "b": 2\n}')


if __name__ == "__main__":
    unittest.main()

