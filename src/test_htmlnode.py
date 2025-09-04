import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_renders_p(self):
        self.assertEqual(LeafNode("p", "Hello").to_html(), "<p>Hello</p>")

    def test_leaf_raw_text(self):
        self.assertEqual(LeafNode(None, "Hello").to_html(), "Hello")

    def test_leaf_to_attrs(self):
        node = LeafNode("a", "Click", {"href": "https://boot.dev","target": "_blank"})
        html = node.to_html()
        self.assertIn('<a ', html)
        self.assertIn('href="https://boot.dev"', html)
        self.assertIn('target="_blank"', html)
        self.assertTrue(html.startswith("<a "))
        self.assertTrue(html.endswith(">Click</a>"))

    def test_leaf_raises_without_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_leaf_empty_props(self):
        self.assertEqual(LeafNode("span", "x", {}).to_html(), "<span>x</span>")

    def test_leaf_various_tags(self):
        self.assertEqual(LeafNode("strong", "b").to_html(), "<strong>b</strong>")
        self.assertEqual(LeafNode("em", "i").to_html(), "<em>i</em>")

if __name__ == "__main__":
    unittest.main()
