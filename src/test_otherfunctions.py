import unittest

from textnode import TextNode, TextType
from otherfunctions import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_skips_non_text_nodes(self):
        node = TextNode("already bold", TextType.BOLD_TEXT)

        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(
            new_nodes,
            [
                TextNode("already bold", TextType.BOLD_TEXT),
            ],
        )

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has an `unclosed code block", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

    def test_italic_delimiter(self):
        node = TextNode("This text has some italic text. _This is italic_.", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This text has some italic text. ", TextType.TEXT),
                TextNode("This is italic", TextType.ITALIC_TEXT),
                TextNode(".", TextType.TEXT)
            ]
        )

    def test_multiple_bold_delimiters(self):
        node = TextNode("This has multiple **bold** text. **This is also bold****So is this**.**Even this.**", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This has multiple ", TextType.TEXT),
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" text. ", TextType.TEXT),
                TextNode("This is also bold", TextType.BOLD_TEXT),
                TextNode("So is this", TextType.BOLD_TEXT),
                TextNode(".", TextType.TEXT),
                TextNode("Even this.", TextType.BOLD_TEXT)
            ]
        )