from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)
from inline import text_to_textnodes


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            text = " ".join(line.strip() for line in block.split("\n"))
            children.append(
                ParentNode("p", text_to_children(text))
            )

        elif block_type == BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            text = block[level:].strip()

            children.append(
                ParentNode(f"h{level}", text_to_children(text))
            )

        elif block_type == BlockType.CODE:
            lines = block.split("\n")

            # Remove opening and closing ```
            code_text = "\n".join(lines[1:-1]) + "\n"

            code_node = ParentNode(
                "code",
                [text_node_to_html_node(TextNode(code_text, TextType.TEXT))]
            )

            children.append(
                ParentNode("pre", [code_node])
            )

        elif block_type == BlockType.QUOTE:
            lines = []
            for line in block.split("\n"):
                lines.append(line[1:].strip())

            text = " ".join(lines)

            children.append(
                ParentNode("blockquote", text_to_children(text))
            )

        elif block_type == BlockType.ULIST:
            items = []

            for line in block.split("\n"):
                text = line[2:]
                items.append(
                    ParentNode("li", text_to_children(text))
                )

            children.append(
                ParentNode("ul", items)
            )

        elif block_type == BlockType.OLIST:
            items = []

            for line in block.split("\n"):
                text = line.split(". ", 1)[1]
                items.append(
                    ParentNode("li", text_to_children(text))
                )

            children.append(
                ParentNode("ol", items)
            )

    return ParentNode("div", children)