import unittest

from src.generate_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_extract_title_whitespace(self):
        md = "#    Hello World    "
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_not_first_line(self):
        md = """
paragraph

# My Title

more text
"""
        self.assertEqual(extract_title(md), "My Title")

    def test_extract_title_missing(self):
        md = """
## Heading

paragraph
"""
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()