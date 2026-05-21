import unittest
from htmlnode import HTMLNode, LeafNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_string = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected_string)

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!", {"class": "text"})
        self.assertEqual(
            repr(node),
            "Tag: p, Value: Hello, world!, Props: {'class': 'text'}"
        )
    
    def test_leaf_repr_no_props(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(
            repr(node),
            "Tag: p, Value: Hello, world!, Props: None"
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()