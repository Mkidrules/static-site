import unittest
from block_to_html import markdown_to_html_node, text_to_children
from markdown_blocks import markdown_to_blocks


class TestMarkdownToHtml(unittest.TestCase):

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

    def test_heading(self):
        md = "# Heading"

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading</h1></div>"
        )

    def test_heading_with_inline(self):
        md = "## A **bold** heading"

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h2>A <b>bold</b> heading</h2></div>"
        )

    def test_quote_block(self):
        md = """
> This is a quote
> spread across
> multiple lines
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote spread across multiple lines</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- First item
- Second item
- Third item
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        )

    def test_paragraph_inline_markdown(self):
        md = "This has **bold**, _italic_, and `code`."

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><p>This has <b>bold</b>, <i>italic</i>, and <code>code</code>.</p></div>"
        )

    def test_multi_block_document(self):
        md = """
# Heading

This is a paragraph.

- Item 1
- Item 2
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading</h1><p>This is a paragraph.</p><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        )


if __name__ == "__main__":
    unittest.main()