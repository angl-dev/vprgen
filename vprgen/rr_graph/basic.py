#!/usr/bin/env python3

from collections import namedtuple

from .abc import Edge as EdgeABC
from .abc import ArchitectureDelegate as ArchitectureDelegateABC

# Implementation using namedtuple
Edge = namedtuple('Edge', ['src_node', 'sink_node', 'switch_id', 'metadata'])
EdgeABC.register(Edge)


class ArchitectureDelegate:
    def __init__(self):
        self.edges = []

    def add_edge(self, src_node, sink_node, switch_id, metadata={}):
        self.edges.append(Edge(src_node, sink_node, switch_id, metadata))

    def edges(self):
        return self.edges


ArchitectureDelegateABC.register(ArchitectureDelegate)
