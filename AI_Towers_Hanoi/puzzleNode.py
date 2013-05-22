'''
This class represents a single node which we interpret as a puzzle state
Node is designed to be used in a tree structure, contain the state of an 8-puzzle 
in a list, know it's parent, know it's children, and contain a value "total_traversal"
which is used as a heuristic.  The value of total_traversal = parent's total_traversal + 
value associated with the new state. f(x) = g(x) + h(x); total = actual + estimated
'''

class Node(object):
    def __init__(self, data, parent, total_traversal):
        self.data = data
        self.children = []
        self.parent = parent
        self.total_traversal = total_traversal

    def add_child(self, obj):
        self.children.append(obj)
