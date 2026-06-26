from src.htmlnode import HTMLNode, ParentNode
from src.inline_markdown import text_to_textnodes
from src.markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks
from src.textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    html: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                paragraph_children = text_to_children(block)
                paragraph_node = ParentNode("p", paragraph_children)
                html.append(paragraph_node)
            case BlockType.HEADING:
                tag = markdown_to_html_headings(block)
                number_of_hashes = int(tag[1])
                heading_text = block[number_of_hashes + 1 :]
                heading_children = text_to_children(heading_text)
                heading_node = ParentNode(tag, heading_children)
                html.append(heading_node)
            case BlockType.CODE:
                code_text = code_text = block[4:-3]
                text_node: TextNode = TextNode(code_text, TextType.CODE)
                html.append(ParentNode("pre", [text_node_to_html_node(text_node)]))
            case BlockType.ULIST:
                lines = block.split("\n")
                li_nodes = []
                for line in lines:
                    item_text = line[2:]
                    item_children = text_to_children(item_text)
                    li_nodes.append(ParentNode("li", item_children))
                list_node = ParentNode("ul", li_nodes)
                html.append(list_node)
            case BlockType.OLIST:
                lines = block.split("\n")
                li_nodes = []
                for line in lines:
                    item_text = line.split(". ", 1)[1]
                    item_children = text_to_children(item_text)
                    li_nodes.append(ParentNode("li", item_children))
                list_node = ParentNode("ol", li_nodes)
                html.append(list_node)
            case _:
                raise ValueError("Invalid block type")

    return ParentNode("div", html)


def text_to_children(text: str) -> list[HTMLNode]:
    nodes: list[HTMLNode] = []
    text_nodes: list[TextNode] = text_to_textnodes(text)
    for text_node in text_nodes:
        if text_node.text_type == TextType.TEXT:
            text_node.text = text_node.text.replace("\n", " ")
        nodes.append(text_node_to_html_node(text_node))
    return nodes


def markdown_to_html_headings(block: str) -> str:
    if block.startswith("###### "):
        return "h6"
    if block.startswith("##### "):
        return "h5"
    if block.startswith("#### "):
        return "h4"
    if block.startswith("### "):
        return "h3"
    if block.startswith("## "):
        return "h2"
    if block.startswith("# "):
        return "h1"
    return ""
