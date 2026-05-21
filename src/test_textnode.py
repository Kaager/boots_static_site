import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_another_eq(self):
        node = TextNode("Text in a test", TextType.ITALIC_TEXT, None)
        node2 = TextNode("Text in a test", TextType.ITALIC_TEXT, None)
        self.assertEqual(node, node2)

    def test_another_eq_2(self):
        node = TextNode("Text in a test", TextType.ITALIC_TEXT, None)
        node2 = TextNode("Text in a test", TextType.ITALIC_TEXT)
        self.assertEqual(node, node2)

    def test_another_eq_3(self):
        node = TextNode("Text in a test", TextType.ITALIC_TEXT, "some url")
        node2 = TextNode("Text in a test", TextType.ITALIC_TEXT, "some url")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is some test text", TextType.ITALIC_TEXT)
        node2 = TextNode("This is some OTHER test text", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_2(self):
        node = TextNode("some text", TextType.LINKS)
        node2 = TextNode("some text", TextType.IMAGE)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_3(self):
        node = TextNode("some alt text", TextType.LINKS, "some url")
        node2 = TextNode("some alt text", TextType.LINKS, "some other url")
        self.assertNotEqual(node, node2)

    def test_edge_not_rq(self):
        node = TextNode("some text", TextType.TEXT)
        self.assertNotEqual(node, "some text")


if __name__ == "__main__":
    unittest.main()