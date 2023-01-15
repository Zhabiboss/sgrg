import sys

def readfile(filename):
    with open(filename, "r") as file:
        return file.read().split("\n")

def convert():
    filename = sys.argv[1]
    content = readfile(filename)
    nodes = []
    node = []
    for idx, el in enumerate(content):
        node.append(el)
        if (idx + 1) % 4 == 0 and idx != 0:
            nodes.append(node)
            node = []

    print(nodes)
    
    res = ""
    
    for node in nodes:
        #if self.ticks_passed == 60:
        #    self.nodes.append(Node(100, 500, 120))
        #if self.ticks_passed == 120:
        #    self.nodes.append(Node(10, 56, 120))
        res += f"if self.ticks_passed == {node[2]}:\n\tself.nodes.append(Node({node[0]}, {node[1]}, {node[3]}))\n"

    print(res)

convert()