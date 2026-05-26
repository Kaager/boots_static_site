

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []

    for block in blocks:
        s_block = block.strip()
        if s_block != "":
            stripped_blocks.append(s_block)

    return stripped_blocks