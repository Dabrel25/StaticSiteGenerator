from textnode import TextType
from textnode import TextNode

def main():
    text = "baby_gurl"
    text_type = TextType.bold
    url = "https://www.google.com"

    print(TextNode(text, text_type, url))

main()

