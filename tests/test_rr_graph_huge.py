#!/usr/bin/env python3

import sys

sys.path.insert(0, ".")

assert sys.argv[1]
exec("from vprgen.rr_graph import %s as rr_graph" % (sys.argv[1],))

d = rr_graph.ArchitectureDelegate()

for i in range(0, int(10000000)):
    d.add_edge(i, i+1, 0, {})


