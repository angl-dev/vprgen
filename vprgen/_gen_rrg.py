from future.builtins import range

try:
    from collections.abc import Mapping, Sequence
except ImportError:
    from collections import Mapping, Sequence

from vprgen._xml import XMLGenerator
from jsonschema import validate
from json import load
import os

_segment_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "segment.schema.json")))
_switch_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "switch.schema.json")))
_node_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "node.schema.json")))
_edge_scgema = load(open(os.path.join(os.path.dirname(__file__), "schema", "edge.schema.json")))

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
