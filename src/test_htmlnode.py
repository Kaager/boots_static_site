import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p")
        expected_string = f"Tag: {node.tag}, Value: None, Children: None, Props: None"
        self.assertEqual(node.__repr__(), expected_string)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank", "some_other_key": "some other value",})
        expected_string = ' href="https://www.google.com" target="_blank" some_other_key="some other value"'
        self.assertEqual(node.props_to_html(), expected_string)

    def test_props_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_none_2(self):
        node = HTMLNode("p")
        self.assertEqual(node.props_to_html(), "")

    def test_constructor_defauls(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

if __name__ == "__main__":
    unittest.main()