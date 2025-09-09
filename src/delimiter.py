import re

from src.textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes,delimiter,text_type):
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.text:
            nodes.append(old_node)

        else:
            split_nodes = old_node.text.split(delimiter)
            new_nodes = []
            if len(split_nodes)%2 == 0:
                raise Exception("The delimiter is not balanced")
            for i in range(len(split_nodes)):
                if split_nodes[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_nodes[i],TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_nodes[i],text_type))
            nodes.extend(new_nodes)
    return nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# python
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        while True:
            pairs = extract_markdown_images(text)
            if not pairs:
                if text:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                break

            alt, url = pairs[0]
            needle = f"[!{alt}]({url})"
            before, after = text.split(needle, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGES, url))
            text = after
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        while True:
            pairs = extract_markdown_links(text)
            if not pairs:
                if text:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                break

            label, url = pairs[0]
            needle = f"[{label}]({url})"
            before, after = text.split(needle, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(label, TextType.LINKS, url))
            text = after
    return new_nodes


def text_to_textnodes(text):
    if text is None:
        raise ValueError("text must not be None")
    if text == "":                 # decide behavior explicitly
        return []                  # we’ll return an empty list for ""

    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = [n for n in nodes if not (n.text_type == TextType.TEXT and n.text == "")]
    return nodes

