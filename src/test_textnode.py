import unittest
from textnode import TextNode, TextType
from textnode import text_node_to_html_node 

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Different text", TextType.BOLD)

        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)

        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode(
            "Click me",
            TextType.LINK,
            "https://www.boot.dev"
        )

        node2 = TextNode(
            "Click me",
            TextType.LINK,
            "https://www.boot.dev"
        )

        self.assertEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("Plain text", TextType.TEXT)
        node2 = TextNode("Plain text", TextType.TEXT, None)

        self.assertEqual(node, node2)

class TestTexttoHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")


    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")


    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")


    def test_link(self):
        node = TextNode(
            "Boot.dev",
            TextType.LINK,
            "https://www.boot.dev"
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(
            html_node.props,
            {"href": "https://www.boot.dev"}
        )


    def test_image(self):
        node = TextNode(
            "logo",
            TextType.IMAGE,
            "https://www.boot.dev/logo.png"
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://www.boot.dev/logo.png",
                "alt": "logo",
            }
        )


if __name__ == "__main__":
    unittest.main()