import unittest

from blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_basic_blocks(self):
        md = """# Heading

This is a paragraph.

- item one
- item two"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "# Heading",
            "This is a paragraph.",
            "- item one\n- item two",
        ])

    def test_strips_whitespace(self):
        md = """   # Heading with spaces   

   Paragraph with spaces.   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "# Heading with spaces",
            "Paragraph with spaces.",
        ])

    def test_removes_empty_blocks(self):
        md = """First block



Third block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "First block",
            "Third block",
        ])

    def test_single_block(self):
        md = "Just one block with no separators."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block with no separators."])

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])