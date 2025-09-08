from delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

def test_split_nodes_delimiter_code(self):
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    expected = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ]
    self.assertEqual(new_nodes, expected)

def test_split_nodes_delimiter_bold(self):
    node = TextNode("This is **bold** text", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    expected = [
        TextNode("This is ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" text", TextType.TEXT),
    ]
    self.assertEqual(new_nodes, expected)

def test_split_nodes_delimiter_italic(self):
    node = TextNode("This is *italic* text", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

    expected = [
        TextNode("This is ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" text", TextType.TEXT),
    ]
    self.assertEqual(new_nodes, expected)

def test_split_nodes_delimiter_no_delimiters(self):
    node = TextNode("This is text without any delimiters", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    expected = [
        TextNode("This is text without any delimiters", TextType.TEXT)
    ]
    self.assertEqual(new_nodes, expected)
def test_split_nodes_delimiter_multiple_delimiters(self):
    node = TextNode("This `code1` and `code2` text", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    expected = [
        TextNode("This ", TextType.TEXT),
        TextNode("code1", TextType.CODE),
        TextNode(" and ", TextType.TEXT),
        TextNode("code2", TextType.CODE),
        TextNode(" text", TextType.TEXT),
    ]
    self.assertEqual(new_nodes, expected)
def test_split_nodes_delimiter_unmatched(self):
    node = TextNode("This `unmatched text", TextType.TEXT)
    with self.assertRaises(Exception):
        split_nodes_delimiter([node], "`", TextType.CODE)

def test_split_nodes_delimiter_non_text_nodes(self):
    node = TextNode("Already bold", TextType.BOLD)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    expected = [
        TextNode("Already bold", TextType.BOLD)  # Should remain unchanged
    ]
    self.assertEqual(new_nodes, expected)