import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        section_list: list[str] = old_node.text.split(delimiter)
        if len(section_list) % 2 == 0:
            raise ValueError("invalid markdown, unclosed delimiter")
        for i in range(len(section_list)):
            if section_list[i] != "":
                if i % 2 == 0:
                    new_nodes.append(TextNode(section_list[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(section_list[i], text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
        current_text: str = old_node.text
        for image in images:
            section: list[str] = current_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(section) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if section[0] != "":
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, url=image[1]))
            current_text = section[1]
        if len(current_text) > 0:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        current_text: str = old_node.text
        for link in links:
            section: list[str] = current_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(section) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if section[0] != "":
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, url=link[1]))
            current_text = section[1]
        if len(current_text) > 0:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    node = [TextNode(text, text_type=TextType.TEXT)]
    node = split_nodes_delimiter(node, delimiter="**", text_type=TextType.BOLD)
    node = split_nodes_delimiter(node, delimiter="_", text_type=TextType.ITALIC)
    node = split_nodes_delimiter(node, delimiter="`", text_type=TextType.CODE)
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    return node
