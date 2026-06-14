import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode(
            "a",
            "Google",
            None,
            {"href": "https://www.google.com"},
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com"',
        )

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            "a",
            "Google",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "Hello world")

        self.assertEqual(node.props_to_html(), "")

    
class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "hello")],
            {"class": "container"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container">hello</div>'
        )

    def test_nested_parents(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "text")
                    ]
                )
            ]
        )

        self.assertEqual(
            node.to_html(),
            "<div><p><b>text</b></p></div>"
        )

    def test_no_tag_raises(self):
        node = ParentNode(
            None,
            [LeafNode(None, "text")]
        )

        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children_raises(self):
        node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            node.to_html()

    def test_multiple_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode(None, "a"),
                LeafNode(None, "b"),
                LeafNode(None, "c"),
            ]
        )

        self.assertEqual(
            node.to_html(),
            "<div>abc</div>"
        )



    

if __name__ == "__main__":
    unittest.main()