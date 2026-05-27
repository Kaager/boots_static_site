from htmlnode import ParentNode, LeafNode, HTMLNode
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from otherfunctions import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    all_block_nodes = []
    
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        tag = get_tag(block_type, block)

        if block_type in (BlockType.ORDERED_LIST, BlockType.UNORDERED_LIST):
            block_node = list_to_html(block, tag)
        elif block_type == BlockType.CODE:
            block_node = code_to_html(block)
        else:
            cleaned_text = clean_block_text(block, block_type)
            children = text_to_children(cleaned_text)
            block_node = ParentNode(tag, children)

        all_block_nodes.append(block_node)
    return ParentNode("div", all_block_nodes)


def clean_block_text(block, block_type):
    if block_type == BlockType.HEADING:
        return block[get_heading_level(block) + 1:]
    elif block_type == BlockType.PARAGRAPH:
        return block.replace("\n", " ")
    elif block_type == BlockType.QUOTE:
        lines = block.split("\n")
        cleaned_lines = []
        for line in lines:
            cleaned_lines.append(line.removeprefix("> "))
        return "\n".join(cleaned_lines)



def get_tag(block_type, block):
    if block_type == BlockType.PARAGRAPH:
        return "p"
    elif block_type == BlockType.HEADING:
        return f"h{get_heading_level(block)}"
    elif block_type == BlockType.ORDERED_LIST:
        return "ol"
    elif block_type == BlockType.UNORDERED_LIST:
        return "ul"
    elif block_type == BlockType.QUOTE:
        return "blockquote"
    elif block_type == BlockType.CODE:
        return "pre"

    
def get_heading_level(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    return count


def list_to_html(block, tag):
    lines = block.split("\n")

    li_nodes = []
    for line in lines:
        if tag == "ul":
            item_text = line[2:]
        else:
            item_text = line.split(". ", 1)[1]
        item_children = text_to_children(item_text)
        li_nodes.append(ParentNode("li", item_children))
    
    return ParentNode(tag, li_nodes)


def code_to_html(block):
    code_syntax_removed = block[4:-3]
    code_text_node = TextNode(code_syntax_removed, TextType.TEXT)
    code_leaf = text_node_to_html_node(code_text_node)
    code_node = ParentNode("code", [code_leaf])
    return ParentNode("pre", [code_node])


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children