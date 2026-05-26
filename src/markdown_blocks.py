from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []

    for block in blocks:
        s_block = block.strip()
        if s_block != "":
            stripped_blocks.append(s_block)

    return stripped_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if len(lines) > 1 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    elif block[0] == ">":
        for line in lines:
            if line[0] != ">":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block[:2] == "- ":
        for line in lines:
            if line[:2] != "- ":
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block[:3] == "1. ":
        for line_index in range(len(lines)):
            if not lines[line_index].startswith(f"{line_index + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    elif block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    return BlockType.PARAGRAPH