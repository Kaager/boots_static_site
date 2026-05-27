import unittest

from markdown_to_html import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2 with **bold**

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <b>bold</b></h2><h6>Heading 6</h6></div>",
        )

    def test_blockquote(self):
        md = """
> This is a quote
> with multiple lines
> and _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nwith multiple lines\nand <i>italic</i> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- first item
- second **bold** item
- third item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second <b>bold</b> item</li><li>third item with <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first
2. second
3. third with _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><ol><li>first</li><li>second</li><li>third with <i>italic</i></li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = """
# My Title

This is a paragraph with **bold** and _italic_.

- list item one
- list item two

> a wise quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>My Title</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i>.</p><ul><li>list item one</li><li>list item two</li></ul><blockquote>a wise quote</blockquote></div>",
        )