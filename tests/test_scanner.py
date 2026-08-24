import unittest

from scopeguard.scanner import _normalise_target


class ScannerTests(unittest.TestCase):
    def test_normalise_target_adds_https(self):
        self.assertEqual(
            _normalise_target("example.test"),
            ("https://example.test", "example.test", 443),
        )

    def test_normalise_target_rejects_non_http_scheme(self):
        with self.assertRaisesRegex(ValueError, r"HTTP\(S\)"):
            _normalise_target("ftp://example.test")
