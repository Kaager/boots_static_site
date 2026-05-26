import unittest

from textnode import TextNode, TextType
from otherfunctions import split_nodes_delimiter, extract_markdown_images, extract_markdown_link, split_nodes_image, split_nodes_link

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

class TestExtractMarkdownImagesAndLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). Some more text with another image: ![alt_image_text](https://i.imgur.comasdfas/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("alt_image_text", "https://i.imgur.comasdfas/zjjcJKZ.png")], matches)

    def test_expect_nothing_back(self):
        matches = extract_markdown_images(
            "This is text but with incorrect markdown syntax for an image: [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([], matches)

    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_link(text)
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_expect_empty_list(self):
        matches = extract_markdown_link(
            "This is text but with incorrect markdown syntax for an image: ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([], matches)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_with_no_images(self):
        node = TextNode("This is a textnode with no image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([node], new_nodes)

    def test_split_image_with_non_text_type(self):
        node = TextNode("This is some bold text", TextType.BOLD_TEXT)
        new_node = split_nodes_image([node])
        self.assertEqual([node], new_node)

    def test_split_image_no_leading_text(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) and then some text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and then some text", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_image_with_only_an_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )

    def test_split_image_no_trailing_text(self):
        node = TextNode("Some leading text and then an image: ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Some leading text and then an image: ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )

    def test_split_image_multiple_old_nodes(self):
        node1 = TextNode("Some leading text and then an image: ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("Some leading text and then an image: ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes
        )


class TestSplitNodesLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINKS, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.LINKS, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_with_no_links(self):
        node = TextNode("This is a textnode with no link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual([node], new_nodes)

    def test_split_link_with_non_text_type(self):
        node = TextNode("This is some bold text", TextType.BOLD_TEXT)
        new_node = split_nodes_link([node])
        self.assertEqual([node], new_node)

    def test_split_link_no_leading_text(self):
        node = TextNode("[image](https://i.imgur.com/zjjcJKZ.png) and then some text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.LINKS, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and then some text", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_link_with_only_an_image(self):
        node = TextNode("[image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.LINKS, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )

    def test_split_link_no_trailing_text(self):
        node = TextNode("Some leading text and then an image: [image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Some leading text and then an image: ", TextType.TEXT),
                TextNode("image", TextType.LINKS, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )

    def test_split_link_multiple_old_nodes(self):
        node1 = TextNode("Some leading text and then an image: [image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node2 = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("Some leading text and then an image: ", TextType.TEXT),
                TextNode("image", TextType.LINKS, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINKS, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.LINKS, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes
        )