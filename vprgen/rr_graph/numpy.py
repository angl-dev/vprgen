#!/usr/bin/env python3

import numpy as np

from .abc import Edge as EdgeABC
from .abc import ArchitectureDelegate as ArchitectureDelegateABC

"""Implementation using numpy."""

Edge = np.dtype([
  ('src_node', '=i8'),  # 64bit int
  ('sink_node', '=i8'), # 64bit int
  ('switch_id', '=i2'), # 16bit int
  ('metadata',  'O'),   # dict {}
])

#EdgeABC.register(Edge)


class ArchitectureDelegate:
    def __init__(self, hint=10485760):
        self.i = 0
        self.edges_mem_owner = np.zeros(hint, dtype=Edge)
        self.edges = self.edges_mem_owner.view(np.recarray)

    def add_edge(self, src_node, sink_node, switch_id, metadata={}):
        l = len(self.edges)
        if self.i == l:
            print("Doubling edges size", l, "->", l*2)
            del self.edges
            self.edges_mem_owner.resize(l*2)
            self.edges = self.edges_mem_owner.view(np.recarray)

        e = self.edges[self.i]
        e.src_node = src_node
        e.sink_node = sink_node
        e.switch_id = switch_id
        e.metadata = metadata
        self.i += 1

    def edges(self):
        return self.edges[:self.i]


ArchitectureDelegateABC.register(ArchitectureDelegate)
