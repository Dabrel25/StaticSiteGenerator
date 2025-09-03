import unittest

from htmlnode import HTMLNode

def test_props_none():
    n = HTMLNode(tag="a")
    assert n.props_to_html() == ""

def test_props_single():
    n = HTMLNode(tag="a", props={"href":"https://x"})
    assert n.props_to_html() == ' href="https://x"'

def test_props_multi():
    n = HTMLNode(tag="a", props={"href":"https://x","target":"_blank"})
    out = n.props_to_html()
    assert out.startswith(" ")
    assert 'href="https://x"' in out and 'target="_blank"' in out
    assert out.count(" ") == 2  # 1 leading + 1 between




if __name__ == "__main__":
    unittest.main()