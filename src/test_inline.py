import unittest
from textnode import TextNode, TextType
from inline import split_nodes_delimiter
from inline import extract_markdown_images, extract_markdown_links
from inline import split_nodes_image, split_nodes_link, text_to_textnodes
from markdown_blocks import block_to_block_type, BlockType, markdown_to_blocks


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE
        )

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_bold(self):
        node = TextNode(
            "This is **bold** text",
            TextType.TEXT
        )

        result = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_italic(self):
        node = TextNode(
            "This is _italic_ text",
            TextType.TEXT
        )

        result = split_nodes_delimiter(
            [node],
            "_",
            TextType.ITALIC
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_invalid_markdown(self):
        node = TextNode(
            "This is `broken markdown",
            TextType.TEXT
        )

        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [node],
                "`",
                TextType.CODE
            )

    def test_non_text_node(self):
        node = TextNode(
            "already bold",
            TextType.BOLD
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE
        )

        self.assertEqual(result, [node])


# Additional tests for extract_markdown_images and extract_markdown_links

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "![rick](https://a.com) and ![obi](https://b.com)"
        )
        self.assertListEqual(
            [
                ("rick", "https://a.com"),
                ("obi", "https://b.com"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "A [link](https://boot.dev)"
        )
        self.assertListEqual(
            [("link", "https://boot.dev")],
            matches,
        )

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "[boot](https://boot.dev) and [youtube](https://youtube.com)"
        )
        self.assertListEqual(
            [
                ("boot", "https://boot.dev"),
                ("youtube", "https://youtube.com"),
            ],
            matches,
        )

    def test_links_do_not_match_images(self):
        matches = extract_markdown_links(
            "![image](https://image.com) [link](https://link.com)"
        )
        self.assertListEqual(
            [("link", "https://link.com")],
            matches,
        )

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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Text [one](https://one.com) and [two](https://two.com)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://one.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://two.com"),
            ],
            split_nodes_link([node]),
        )

    def test_link_at_beginning(self):
        node = TextNode(
            "[Boot.dev](https://boot.dev) is great",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" is great", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_image_at_end(self):
        node = TextNode(
            "Look at this ![cat](cat.png)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("Look at this ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "cat.png"),
            ],
            split_nodes_image([node]),
        )

    def test_no_links(self):
        node = TextNode(
            "just plain text",
            TextType.TEXT,
        )

        self.assertListEqual(
            [node],
            split_nodes_link([node]),
        )

    def test_non_text_node(self):
        node = TextNode(
            "bold",
            TextType.BOLD,
        )

        self.assertListEqual(
            [node],
            split_nodes_link([node]),
        )

    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word and a "
            "`code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode(
                "link",
                TextType.LINK,
                "https://boot.dev"
            ),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_newlines(self):
        md = """

Paragraph one


Paragraph two



Paragraph three

"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "Paragraph one",
                "Paragraph two",
                "Paragraph three",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_heading_h1(self):
        block = "# Heading"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_heading_h6(self):
        block = "###### Heading"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )

    def test_quote_single_line(self):
        block = "> quoted text"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_quote_multi_line(self):
        block = "> line 1\n> line 2\n> line 3"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_unordered_list(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ULIST
        )

    def test_ordered_list(self):
        block = "1. item 1\n2. item 2\n3. item 3"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.OLIST
        )

    def test_ordered_list_wrong_start(self):
        block = "2. item 1\n3. item 2"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_ordered_list_wrong_sequence(self):
        block = "1. item 1\n3. item 2"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_unordered_list_mixed(self):
        block = "- item 1\nnormal text"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )


if __name__ == "__main__":
    unittest.main()