import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multi_children(self):
        child_node_1 = LeafNode("span", "child_1")
        child_node_2 = LeafNode("a", "child_2")
        parent_node = ParentNode("div", [child_node_1, child_node_2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child_1</span><a>child_2</a></div>"
        )

    def test_to_html_with_multi_children_2(self):
        child_node_1 = LeafNode("span", "child_1")
        child_node_2 = LeafNode("a", "child_2")
        child_node_3 = LeafNode(None, "child_3(normal_text)")
        parent_node = ParentNode("div", [child_node_1, child_node_2, child_node_3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child_1</span><a>child_2</a>child_3(normal_text)</div>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("b", "some text")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_child(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_nested_parents(self):
        inner = ParentNode("b", [LeafNode(None, "deep")])
        middle = ParentNode("span", [inner])
        outer = ParentNode("div", [middle])

        self.assertEqual(
            outer.to_html(),
            "<div><span><b>deep</b></span></div>"
        )

    def test_to_html_with_nested_parents_and_siblings(self):
        nested = ParentNode("span", [
            LeafNode("b", "bold"),
            LeafNode(None, " text"),
        ])
        root = ParentNode("div", [
            LeafNode(None, "start"),
            nested,
            LeafNode("i", "end"),
        ])

        self.assertEqual(
            root.to_html(),
            "<div>start<span><b>bold</b> text</span><i>end</i></div>"
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "content")],
            {"class": "box", "id": "main"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="box" id="main">content</div>'
        )

    def test_to_html_with_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_with_only_text_children(self):
        node = ParentNode("p", [
            LeafNode(None, "hello "),
            LeafNode(None, "world")
        ])
        self.assertEqual(node.to_html(), "<p>hello world</p>")

    def test_to_html_with_deeply_nested_parents(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("article", [
                    LeafNode(None, "text")
                ])
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><section><article>text</article></section></div>"
        )

    def test_to_html_no_tag_message(self):
        node = ParentNode(None, [LeafNode(None, "x")])
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertNotEqual(str(cm.exception), "")

    def test_to_html_no_tag_err_message(self):
        node = ParentNode(None, [LeafNode(None, "x")])
        with self.assertRaises(ValueError) as err_obj:
            node.to_html()
        self.assertEqual(str(err_obj.exception), "'tag' can't be None")

    def test_to_html_no_children_err_message(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as err_obj:
            node.to_html()
        self.assertEqual(str(err_obj.exception), "no children for this parent")





if __name__ == "__main__":
    unittest.main()