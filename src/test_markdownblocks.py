import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

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

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_1(self):
        string = "# This is a heading"
        block_type = block_to_block_type(string)
        self.assertEqual(BlockType.HEADING, block_type)
    
    def test_heading_3(self):
        string = "### This is a heading"
        block_type = block_to_block_type(string)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_code_block(self):
        string = "```\nsome code\n```"
        block_type = block_to_block_type(string)
        self.assertEqual(BlockType.CODE, block_type)

    def test_unordered_list(self):
        string = "- some item\n- some other item\n- yet another item"
        block_type = block_to_block_type(string)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_ordered_list(self):
        string = "1. item 1\n2. item 2\n3. item 3"
        block_type = block_to_block_type(string)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)
        
    def test_ordered_list_skip(self):
        string = "1. item 1\n3. item 3\n4. item 4"
        block_type = block_to_block_type(string)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_quote_block(self):
        string = ">this is a quote\n>from someone"
        block_type = block_to_block_type(string)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_paragraph(self):
        string = "this is just a paragraph"
        b_type = block_to_block_type(string)
        self.assertEqual(BlockType.PARAGRAPH, b_type)

    def test_not_valid_heading(self):
        string = "####### this heading is not valid"
        b_type = block_to_block_type(string)
        self.assertEqual(BlockType.PARAGRAPH, b_type)

    def test_not_a_real_code_block(self):
        string = "```\nnot a real code block```"
        b_type = block_to_block_type(string)
        self.assertEqual(BlockType.PARAGRAPH, b_type)

    def test_fake_quote(self):
        string = ">hello\nthere\n>obi-wan"
        b_type = block_to_block_type(string)
        self.assertEqual(BlockType.PARAGRAPH, b_type)