from src.textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes,delimiter,text_type):
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            nodes.append(old_node)

        else:
            split_nodes = old_node.text.split(delimiter)
            new_nodes = []
            if len(split_nodes)%2 == 0:
                raise Exception("The delimiter is not balanced")
            for i in range(len(split_nodes)):
                if split_nodes[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_nodes[i],TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_nodes[i],text_type))
            nodes.extend(new_nodes)
    return nodes




