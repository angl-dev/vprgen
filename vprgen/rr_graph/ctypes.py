#!/usr/bin/env python3

from ctypes import *

from .abc import Edge as EdgeABC
from .abc import ArchitectureDelegate as ArchitectureDelegateABC


"""Implementation using ctypes."""

class Edge(Structure):
    _fields_ = [
        ("src_node", c_ulonglong),
        ("sink_node", c_ulonglong),
        ("switch_id", c_int),
        ("metadata", py_object),
    ]


def array_resize(a, new_size):
    assert new_size > a._length_, (new_size, a._length_)
    resize(a, sizeof(a._type_)*new_size)
    return (a._type_*new_size).from_address(addressof(a))


class ArchitectureDelegate:
    def __init__(self):
        self.i = 0
        self.s = sizeof(Edge)

        self.edges_l = 10
        self.edges_mem_owner = (Edge * 10)()
        self.edges = self.edges_mem_owner

    def add_edge(self, src_node, sink_node, switch_id, metadata={}):
        if self.i == self.edges_l:
            print("Doubling edges size", self.edges_l, "->", self.edges_l*2)
            self.edges_l *= 2
            self.edges = array_resize(self.edges_mem_owner, self.edges_l)
        e = self.edges[self.i]
        e.src_node = src_node
        e.sink_node = sink_node
        e.switch_id = switch_id
        e.metadata = metadata
        self.i += 1

    def edges(self):
        return self.edges[:self.i]


ArchitectureDelegateABC.register(ArchitectureDelegate)
