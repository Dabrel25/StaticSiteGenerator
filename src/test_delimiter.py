from delimiter import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link
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

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is text with a [link](https://boot.dev)"
    )
    self.assertListEqual([("link", "https://boot.dev")], matches)
# python
def test_split_links_multiple(self):
    node = TextNode(
        "Check [Boot.dev](https://www.boot.dev) and then [YouTube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("Check ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and then ", TextType.TEXT),
            TextNode("YouTube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ],
        new_nodes,
    )
# python
def test_split_images_multiple(self):
    node = TextNode(
        "Here is ![cat](https://img/cat.png) and also ![dog](https://img/dog.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("Here is ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://img/cat.png"),
            TextNode(" and also ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "https://img/dog.png"),
        ],
        new_nodes,
    )
def test_split_link_single_middle(self):
    node = TextNode("Go to [Site](https://ex.com) now", TextType.TEXT)
    out = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("Go to ", TextType.TEXT),
            TextNode("Site", TextType.LINK, "https://ex.com"),
            TextNode(" now", TextType.TEXT),
        ],
        out,
    )

def test_split_link_start(self):
    node = TextNode("[Start](u) then text", TextType.TEXT)
    out = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("Start", TextType.LINK, "u"),
            TextNode(" then text", TextType.TEXT),
        ],
        out,
    )

def test_split_link_end(self):
    node = TextNode("text then [End](u)", TextType.TEXT)
    out = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("text then ", TextType.TEXT),
            TextNode("End", TextType.LINK, "u"),
        ],
        out,
    )
def test_split_link_none(self):
    node = TextNode("just text", TextType.TEXT)
    out = split_nodes_link([node])
    self.assertListEqual([TextNode("just text", TextType.TEXT)], out)

def test_split_image_single_middle(self):
    node = TextNode("See ![pic](https://ex.com/p.png) now", TextType.TEXT)
    out = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("See ", TextType.TEXT),
            TextNode("pic", TextType.IMAGE, "https://ex.com/p.png"),
            TextNode(" now", TextType.TEXT),
        ],
        out,
    )

def test_split_image_none(self):
    node = TextNode("just text", TextType.TEXT)
    out = split_nodes_image([node])
    self.assertListEqual([TextNode("just text", TextType.TEXT)], out)