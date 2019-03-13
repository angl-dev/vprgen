from future.builtins import range

try:
    from collections.abc import Mapping, Sequence
except ImportError:
    from collections import Mapping, Sequence

from vprgen._xml import XMLGenerator
from jsonschema import validate
from json import load
from itertools import count, product
import os

_segment_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "segment.schema.json")))
_switch_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "switch.schema.json")))
_block_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "block.schema.json")))
_tile_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "tile.schema.json")))
_node_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "node.schema.json")))
_edge_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "edge.schema.json")))

def gen_segment(xmlgen, segment):
    """Generate a <segment> tag for the given ``segment``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        segment (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/segment.schema.json'
    """
    # 1. validate argument
    validate(instance = segment, schema = _segment_schema)
    # 2. generate tag
    with xmlgen.element("segment", {
        "id": segment["id"],
        "name": segment["name"], }):
        xmlgen.element_leaf("timing", {
            "R_per_meter": segment.get("Rmetal", 0),
            "C_per_meter": segment.get("Cmetal", 0), })

def gen_switch(xmlgen, switch):
    """Generate a <switch> tag for the given ``switch``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        switch (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/switch.schema.json'
    """
    # 1. validate argument
    validate(instance = switch, schema = _switch_schema)
    # 2. generate tag
    with xmlgen.element("switch", {
        "buffered": 1 if switch["type"] in ["mux", "tristate", "buffer"] else 0,
        "configurable": 1 if switch["type"] in ["mux", "tristate", "pass_gate"] else 0,
        "id": switch["id"],
        "name": switch["name"],
        "type": switch["type"], }):
        xmlgen.element_leaf("sizing", {
            "buf_size": 0,
            "mux_trans_size": 0, })
        if isinstance(switch["Tdel"], Mapping):
            raise NotImplementedError("rr_graph with a list of <Tdel> tags not supported yet")
        xmlgen.element_leaf("timing", {
            "Cin": switch.get("Cin", 0),
            "Cout": switch.get("Cout", 0),
            "R": switch.get("R", 0),
            "Tdel": switch["Tdel"], })

def gen_block(xmlgen, block):
    """Generate a <block_type> tag for the given ``block``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        block (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/block.schema.json'
    """
    # 1. validate argument
    validate(instance = block, schema = _block_schema)
    # 2. generate tag
    with xmlgen.element("block_type", {
        "name": block["name"],
        "id": block["id"],
        "width": block.get("width", 1),
        "height": block.get("height", 1), }):
        ptc_it = count()
        capacity = block.get("capacity", 1)
        for z, key in product(range(capacity), ("input", "output", "clock")):
            for port in block.get(key, []):
                for bit in range(port["num_pins"]):
                    with xmlgen.element("pin_class", {
                        "type": "OUTPUT" if key == "output" else "INPUT", }):
                        if capacity == 1:
                            xmlgen.element_leaf("pin", {
                                "ptc": next(ptc_it), },
                                "{}.{}[{}]".format(block["name"], port["name"], bit), })
                        else:
                            xmlgen.element_leaf("pin", {
                                "ptc": next(ptc_it), },
                                "{}[{}].{}[{}]".format(block["name"], z, port["name"], bit), })

def gen_tile(xmlgen, tile, x, y):
    """Generate a <grid_loc> tag for the given ``tile``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        tile (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/tile.schema.json'
        x (:obj:`int`): the X position
        y (:obj:`int`): the Y position
    """
    # 1. validate argument
    validate(instance = tile, schema = _tile_schema)
    # 2. generate tag
    xmlgen.element_leaf("grid_loc", {
        "block_type_id": tile["block_type_id"],
        "x": x,
        "y": y,
        "width_offset": tile.get("xoffset", 0),
        "height_offset": tile.get("yoffset", 0), })

def gen_node(xmlgen, node):
    """Generate a <node> tag for the given ``node``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        node (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/node.schema.json'
    """
    # 1. validate argument
    validate(instance = node, schema = _node_schema)
    # 2. generate tag
    attrs = { "capacity": node.get("capacity", 1),
            "id": node["id"],
            "type": node["type"], }
    if node["type"] in ("CHANX", "CHANY"):
        attrs["direction"] = node["direction"]
    with xmlgen.element("node", attrs):
        timing = {"R": 0, "C": 0}
        timing.update(node.get("timing", {}))
        xmlgen.element_leaf("timing", timing)
        xmlgen.element_leaf("loc", node["loc"])
        if node["type"] in ("CHANX", "CHANY"):
            xmlgen.element_leaf("segment", {
                "segment_id": node["segment_id"], })

def gen_edge(xmlgen, edge):
    """Generate a <edge> tag for the given ``edge``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        edge (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/edge.schema.json'
    """
    # 1. validate argument
    validate(instance = edge, schema = _edge_schema)
    # 2. generate tag
    xmlgen.element_leaf("edge", edge)

def gen_rrg_xml(ostream, delegate, pretty = True):
    """Stream generate VPR's routing resource graph XML.

    Args:
        ostream: a file-like object, like a `file` or a `StringIO`
        delegate (`ArchitectureDelegate`): the delegate which answers questions about what are in the architecture
        pretty (:obj:`bool`): if the output XML file should be nicely broken into multiple lines and indented
    """
    with XMLGenerator(ostream, pretty) as xmlgen:
        with xmlgen.element("rr_graph"):
            # 1. channels
            with xmlgen.element("channels"):
                xmlgen.element_leaf("channel", {
                    "chan_width_max": max(delegate.get_x_channel_width(),
                        delegate.get_y_channel_width()),
                    "x_max": delegate.get_x_channel_width(),
                    "x_min": delegate.get_x_channel_width(),
                    "y_max": delegate.get_y_channel_width(),
                    "y_min": delegate.get_y_channel_width(), })
                for y in range(delegate.get_height()):
                    xmlgen.element_leaf("x_list", {
                        "index": y,
                        "info": delegate.get_x_channel_width(), })
                for x in range(delegate.get_width()):
                    xmlgen.element_leaf("y_list", {
                        "index": x,
                        "info": delegate.get_y_channel_width(), })
            # 2. segments
            with xmlgen.element("segments"):
                for segment in delegate.iter_segments():
                    gen_segment(xmlgen, segment)
            # 3. switches
            with xmlgen.element("switches"):
                for switch in delegate.iter_switches():
                    gen_switch(xmlgen, switch)
            # 4. blocks
            with xmlgen.element("block_types"):
                xmlgen.element_leaf("block_type", {
                    "name": "EMPTY",
                    "id": 0,
                    "width": 1,
                    "height": 1, })
                for block in delegate.iter_blocks():
                    gen_block(xmlgen, block)
            # 5. grid
            with xmlgen.element("grid"):
                for x, y in product(range(delegate.get_width()), range(delegate.get_height())):
                    tile = delegate.get_tile(x, y)
                    if tile is None:
                        xmlgen.element_leaf("grid_loc", {
                            "block_type_id": 0,
                            "height_offset": 0,
                            "width_offset": 0,
                            "x": x,
                            "y": y, })
                    else:
                        gen_tile(xmlgen, tile)
            # 6. nodes
            with xmlgen.element("rr_nodes"):
                for node in delegate.iter_nodes():
                    gen_node(xmlgen, node)
            # 7. edges
            with xmlgen.element("rr_edges"):
                for node in delegate.iter_edges():
                    gen_edge(xmlgen, edge)
