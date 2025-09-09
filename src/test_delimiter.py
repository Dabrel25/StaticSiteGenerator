from delimiter import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link
from delimiter import text_to_textnodes
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

def as_tuple_list(nodes):
    return [(n.text, n.text_type, getattr(n, "url", None)) for n in nodes]

def _tt(name):
    # adapt to your enum, e.g., TextType[name]
    return getattr(TextType, name)

def test_basic_mixed_content(self):
    text = (
        "This is **text** with an _italic_ word and a `code block` and an "
        "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
        "[link](https://boot.dev)"
    )
    nodes = text_to_textnodes(text)
    self.assertEqual(
        as_tuple_list(nodes),
        [
            ("This is ", _tt("TEXT"), None),
            ("text", _tt("BOLD"), None),
            (" with an ", _tt("TEXT"), None),
            ("italic", _tt("ITALIC"), None),
            (" word and a ", _tt("TEXT"), None),
            ("code block", _tt("CODE"), None),
            (" and an ", _tt("TEXT"), None),
            ("obi wan image", _tt("IMAGE"), "https://i.imgur.com/fJRm4Vk.jpeg"),
            (" and a ", _tt("TEXT"), None),
            ("link", _tt("LINK"), "https://boot.dev"),
        ],
    )

def test_mixed_example(self):
    text = (
        "This is **text** with an _italic_ word and a `code block` and an "
        "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
        "[link](https://boot.dev)"
    )
    nodes = text_to_textnodes(text)
    self.assertEqual(
        as_tuple_list(nodes),
        [
            ("This is ", _tt("TEXT"), None),
            ("text", _tt("BOLD"), None),
            (" with an ", _tt("TEXT"), None),
            ("italic", _tt("ITALIC"), None),
            (" word and a ", _tt("TEXT"), None),
            ("code block", _tt("CODE"), None),
            (" and an ", _tt("TEXT"), None),
            ("obi wan image", _tt("IMAGE"), "https://i.imgur.com/fJRm4Vk.jpeg"),
            (" and a ", _tt("TEXT"), None),
            ("link", _tt("LINK"), "https://boot.dev"),
        ],
    )

def test_code_shields_styling(self):
    text = "`**not bold** _not italic_` outside **bold**"
    nodes = text_to_textnodes(text)
    self.assertEqual(
        as_tuple_list(nodes),
        [
            ("**not bold** _not italic_", _tt("CODE"), None),
            (" outside ", _tt("TEXT"), None),
            ("bold", _tt("BOLD"), None),
        ],
    )

def test_links_and_images_before_styling(self):
    # underscores in URL/alt/text must NOT trigger italics
    text = "![alt_snake](http://img/a_b) and [li_nk](http://x_y) and _real_"
    nodes = text_to_textnodes(text)
    self.assertIn(("alt_snake", _tt("IMAGE"), "http://img/a_b"), as_tuple_list(nodes))
    self.assertIn(("li_nk", _tt("LINK"), "http://x_y"), as_tuple_list(nodes))
    self.assertIn(("real", _tt("ITALIC"), None), as_tuple_list(nodes))

def test_empty_string_returns_empty_list(self):
    self.assertEqual(text_to_textnodes(""), [])

def test_none_raises_valueerror(self):
    with self.assertRaisesRegex(ValueError, "must not be None"):
        text_to_textnodes(None)  # type: ignore

def test_newlines_preserved_in_parser(self):
    text = "Line1\nLine2 **bold**"
    nodes = text_to_textnodes(text)
    self.assertEqual(
        as_tuple_list(nodes),
        [
            ("Line1\nLine2 ", _tt("TEXT"), None),
            ("bold", _tt("BOLD"), None),
        ],
    )

def test_idempotency_pipeline(self):
    # Running the pipeline again should NOT change the result.
    text = "A `code **x**` and ![alt_x](http://x_y) and [li_nk](http://a_b) and **b _i_**"
    first = text_to_textnodes(text)
    # Re-run through text_to_textnodes by rejoining TEXT nodes (simulates round-trip)
    # NOTE: In a real parser you might not rejoin. This is a practical idempotency check.
    # We expect 'first' already split properly—re-joining TEXT parts should yield the same structure.
    reconstructed = ""
    for t, tt, url in as_tuple_list(first):
        if tt == _tt("TEXT"):
            reconstructed += t
        elif tt == _tt("CODE"):
            reconstructed += f"`{t}`"
        elif tt == _tt("BOLD"):
            reconstructed += f"**{t}**"
        elif tt == _tt("ITALIC"):
            reconstructed += f"_{t}_"
        elif tt == _tt("IMAGE"):
            reconstructed += f"![{t}]({url})"
        elif tt == _tt("LINK"):
            reconstructed += f"[{t}]({url})"
        else:
            # unknown type: treat as raw text
            reconstructed += t

    second = text_to_textnodes(reconstructed)
    self.assertEqual(as_tuple_list(first), as_tuple_list(second))

def test_no_empty_text_nodes_created(self):
    # Ensure parser doesn’t emit zero-length raw TEXT nodes
    text = "![a](http://x)![b](http://y)**c**_d_"
    nodes = text_to_textnodes(text)
    for t, tt, _ in as_tuple_list(nodes):
        self.assertFalse(tt == _tt("TEXT") and t == "")
