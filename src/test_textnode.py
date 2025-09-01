import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a penis node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_equal_when_url_differs(self):
        node = TextNode("hi", TextType.LINKS, None)
        node2 = TextNode("hi", TextType.LINKS, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_repr_without_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_url(self):
        node = TextNode("link for cat", TextType.LINKS, "https://example.com")
        expected = "TextNode(link for cat, links, https://example.com)"
        self.assertEqual(repr(node), expected)





if __name__ == "__main__":
    unittest.main()