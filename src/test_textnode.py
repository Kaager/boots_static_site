import unittest
from textnode import TextNode, TextType, text_node_to_html_node

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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_txt_to_html_err(self):
        node = TextNode("This is a text node", "not_a_real_type")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_txt_to_html_err_msg(self):
        node = TextNode("This is a text node", "not_a_real_type")
        with self.assertRaises(Exception) as err_obj:
            text_node_to_html_node(node)
        self.assertEqual(str(err_obj.exception), "type is not one defined in TextType")

    def test_txt_to_html_bold(self):
        t_node = TextNode("some bold text", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(t_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "some bold text")
        self.assertEqual(html_node.props, None)

    def test_txt_to_html_italic(self):
        t_node = TextNode("some italic text", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(t_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "some italic text")
        self.assertEqual(html_node.props, None)

    def test_txt_to_html_code(self):
        t_node = TextNode("some code", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(t_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "some code")
        self.assertEqual(html_node.props, None)

    def test_txt_to_html_links(self):
        t_node = TextNode("go to google", TextType.LINKS, "google.com")
        html_node = text_node_to_html_node(t_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "go to google")
        self.assertEqual(html_node.props["href"], "google.com")

    def test_text_to_html_image(self):
        t_node = TextNode("alt text", TextType.IMAGE, "path/to/image")
        html_node = text_node_to_html_node(t_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "path/to/image")
        self.assertEqual(html_node.props["alt"], "alt text")








if __name__ == "__main__":
    unittest.main()