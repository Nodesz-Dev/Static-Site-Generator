import unittest

from inline_markdown import extract_title

class TestExtractTitleSuggestions(unittest.TestCase):
    def test_extract_title_empty_string(self):
        markdown = ""
        result = extract_title(markdown)
        expected = Exception
        self.assertRaises(expected, extract_title(markdown))

    def test_extract_title_whitespace_only(self):
        markdown = "   "
        result = extract_title(markdown)
        expected = Exception
        self.assertRaises(expected, extract_title(markdown))

    def test_extract_title_leading_whitespace(self):
        markdown = "   # Hello World"
        result = extract_title(markdown)
        expected = "Hello World"
        self.assertEqual(expected, result)

    def test_extract_title_trailing_whitespace(self):
        markdown = "# Hello World   "
        result = extract_title(markdown)
        expected = "Hello World"
        self.assertEqual(expected, result)

    def test_extract_title_leading_and_trailing_whitespace(self):
        markdown = "   # Hello World   "
        result = extract_title(markdown)
        expected = "Hello World"
        self.assertEqual(expected, result)

    def test_extract_title_multiple_hashes(self):
        markdown = "##### Hello World"
        expected = Exception
        self.assertRaises(expected, extract_title(markdown))

    def test_extract_title_hash_in_title(self):
        markdown = "# Hello # World"
        result = extract_title(markdown)
        expected = "Hello # World"
        self.assertEqual(expected, result)

    def test_extract_title_newline_before(self):
        markdown = "\n# Hello World"
        result = extract_title(markdown)
        expected = "Hello World"
        self.assertEqual(expected, result)

    def test_extract_title_newline_after(self):
        markdown = "# Hello World\n"
        result = extract_title(markdown)
        expected = "Hello World"
        self.assertEqual(expected, result)
