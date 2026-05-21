from textnode import TextNode, TextType


def main():
    some_textnode_object = TextNode("This is some anchor text", TextType.LINKS, "https://boot.dev")
    print(some_textnode_object)

main()