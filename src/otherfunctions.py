import re

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise Exception("not valid Markdown syntax")
        
        for i in range(len(split_node)):
            if split_node[i] == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(split_node[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_node[i], text_type))
    
    return new_nodes


def extract_markdown_images(text):
   return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_link(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        image_list = extract_markdown_images(node.text)
        if image_list == []:
            new_nodes.append(node)
            continue

        tmp_node_text = node.text

        for image in image_list:
            split_image_string = tmp_node_text.split(f"![{image[0]}]({image[1]})", maxsplit=1)

            if split_image_string[0] != "":
                new_nodes.append(TextNode(split_image_string[0], TextType.TEXT))
            
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            tmp_node_text = split_image_string[1]

        if tmp_node_text != "":
            new_nodes.append(TextNode(tmp_node_text, TextType.TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links_list = extract_markdown_link(node.text)
        if links_list == []:
            new_nodes.append(node)
            continue

        tmp_node_text = node.text

        for link in links_list:
            split_links_string = tmp_node_text.split(f"[{link[0]}]({link[1]})", maxsplit=1)

            if split_links_string[0] != "":
                new_nodes.append(TextNode(split_links_string[0], TextType.TEXT))
            
            new_nodes.append(TextNode(link[0], TextType.LINKS, link[1]))

            tmp_node_text = split_links_string[1]

        if tmp_node_text != "":
            new_nodes.append(TextNode(tmp_node_text, TextType.TEXT))
            
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    split_nodes = []

    split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
    split_nodes = split_nodes_delimiter(split_nodes, "_", TextType.ITALIC_TEXT)
    split_nodes = split_nodes_delimiter(split_nodes, "`", TextType.CODE_TEXT)
    split_nodes = split_nodes_image(split_nodes)
    split_nodes = split_nodes_link(split_nodes)

    return split_nodes
