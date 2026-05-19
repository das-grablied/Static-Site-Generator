import unittest

from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        actual = extract_title("# This is a title")

        self.assertEqual(actual, "This is a title")

    def test_extra_whitespace(self):
        actual = extract_title("# This is a title   ")

        self.assertEqual(actual, "This is a title")

    def test_no_title(self):
        with self.assertRaises(ValueError):
            extract_title("This is not a title")

    def test_no_h1_on_first_line(self):
        actual = extract_title("This is not a title\n# This is a title")

        self.assertEqual(actual, "This is a title")

    def test_h2_no_h1(self):
        with self.assertRaises(ValueError):
            extract_title("## This is a subtitle")

    def test_whitespace_after_h1(self):
        actual = extract_title("#    This is a title")

        self.assertEqual(actual, "This is a title")

    if __name__ == "__main__":
        unittest.main()
