from redbaron import AssignmentNode, Node, RedBaron


def get_assignment_name(node: AssignmentNode) -> str:
    return node.target.dumps()


def replace_right_side(node: Node, value: str) -> None:
    """
    >>> from redbaron import RedBaron
    >>> node = RedBaron('x = 5')[0]
    >>> node
    x = 5
    >>> replace_right_side(node, '10')
    >>> node
    x = 10
    """
    node.value = value


def prepend(red: RedBaron, node: Node, text: str) -> None:
    red.insert(get_line_num(node), text + node.dumps())
    red.remove(node)


def get_line_num(node: Node) -> int:
    line_num = node.absolute_bounding_box.top_left.line
    return line_num


def get_node_at_start_of_line(red: RedBaron, node: Node) -> Node:
    line_num = get_line_num(node)
    start_node = red.at(line_num)
    return start_node
