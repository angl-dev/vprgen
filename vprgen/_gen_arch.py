from future.utils import raise_from
from future.builtins import range

try:
    from itertools import imap as map
except ImportError:
    pass

try:
    from collections.abc import Mapping, Sequence
except ImportError:
    from collections import Mapping, Sequence

from vprgen._xml import XMLGenerator
from jsonschema import validate
from json import load
import os

_model_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "model.schema.json")))
_segment_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "segment.schema.json")))
_switch_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "switch.schema.json")))
_direct_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "direct.schema.json")))
_block_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "block.schema.json")))

def gen_model(xmlgen, model):
    """Generate a <model> tag for the given ``model``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        model (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/model.schema.json'
    """
    # 1. validate argument
    validate(instance = model, schema = _model_schema)
    # 2. generate tag
    with xmlgen.element("model", {"name": model["name"]}):
        input_ports = model.get("input_ports", None)
        if input_ports:
            with xmlgen.element("input_ports"):
                for port in input_ports:
                    attrs = {"name": port["name"]}
                    if port.get("is_clock", False):
                        attrs["is_clock"] = "1"
                    clock = port.get("clock", None)
                    if clock:
                        attrs["clock"] = clock
                    sink = " ".join(port.get("combinational_sink_ports", []))
                    if sink:
                        attrs["combinational_sink_ports"] = sink
                    xmlgen.element_leaf("port", attrs)
        output_ports = model.get("output_ports", None)
        if output_ports:
            with xmlgen.element("output_ports"):
                for port in output_ports:
                    attrs = {"name": port["name"]}
                    if port.get("is_clock", False):
                        attrs["is_clock"] = "1"
                    clock = port.get("clock", None)
                    if clock:
                        attrs["clock"] = clock
                    xmlgen.element_leaf("port", attrs)

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
        "name": segment["name"],
        "length": segment["length"],
        "type": "unidir",
        "freq": segment.get("freq", 0),
        "Rmetal": segment.get("Rmetal", 0),
        "Cmetal": segment.get("Cmetal", 0),
        }):
        xmlgen.element_leaf("sb", {"type": "pattern"}, " ".join(map(lambda x: "1" if x else "0",
            segment.get("sb", (True, ) * (segment["length"] + 1)))))
        xmlgen.element_leaf("cb", {"type": "pattern"}, " ".join(map(lambda x: "1" if x else "0",
            segment.get("cb", (True, ) * segment["length"]))))
        xmlgen.element_leaf("mux", {"name": segment["mux"]})

def gen_switch(xmlgen, switch):
    """Generate a <switch> tag for the given ``switch``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        switch (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/switch.schema.json'
    """
    # 1. validate argument
    validate(instance = switch, schema = _switch_schema)
    # 2. generate tag
    Tdel = switch["Tdel"]
    attrs = { "type": switch.get("type", "mux"),
            "name": switch["name"],
            "R": switch.get("R", 0),
            "Cin": switch.get("Cin", 0),
            "Cout": switch.get("Cout", 0), }
    if isinstance(Tdel, Sequence):
        with xmlgen.element("switch", attrs):
            for item in Tdel:
                xmlgen.element_leaf("Tdel", item)
    else:
        attrs["Tdel"] = Tdel
        xmlgen.element_leaf("switch", attrs)

def gen_direct(xmlgen, direct):
    """Generate a <direct> tag for the given ``direct``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        direct (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/direct.schema.json'
    """
    # 1. validate argument
    validate(instance = direct, schema = _direct_schema)
    # 2. generate tag
    attrs = {"x_offset": 0, "y_offset": 0, "z_offset": 0}
    attrs.update(direct)
    xmlgen.element_leaf("direct", attrs)

def gen_delay_matrix(xmlgen, delay):
    """Generate a <delay_matrix> tag for the given ``delay``.
    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        delay (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/block.schema.json/definitions/delay_matrix'
    """
    values = delay['values']
    attrs = { "type": delay["type"],
            "in_port": delay["in_port"],
            "out_port": delay["out_port"], }
    text = ('\n' + '\n'.join(' '.join('{:g}'.format(v) for v in vector) for vector in values) + '\n')
    xmlgen.element_leaf("delay_matrix", attrs, text)

def gen_leaf_pb_type(xmlgen, pb_type):
    """Generate a leaf <pb_type> tag for the given ``pb_type``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        pb_type (:obj:`dict`): a `dict` satisfying the JSON schema
            'schema/block.schema.json/definitions/leaf_pb_type'
    """
    attrs = { "name": pb_type["name"],
            "blif_model": pb_type["blif_model"],
            "num_pb": pb_type.get("num_pb", 1), }
    cls = pb_type.get("class", None)
    if cls:
        attrs["class"] = cls
    with xmlgen.element("pb_type", attrs):
        for key in ("input", "output", "clock", "T_setup", "T_hold", "T_clock_to_Q", "delay_constant"):
            for item in pb_type.get(key, []):
                xmlgen.element_leaf(key, item)
        for delay_matrix in pb_type.get("delay_matrix", []):
            gen_delay_matrix(xmlgen, delay_matrix)

def gen_mode(xmlgen, mode):
    """Generate a <mode> tag for the given ``mode``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        mode (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/block.schema.json/definitions/mode'
    """
    pass

def gen_intermediate_pb_type(xmlgen, pb_type):
    """Generate an intermediate <pb_type> tag for the given ``pb_type``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        pb_type (:obj:`dict`): a `dict` satisfying the JSON schema
            'schema/block.schema.json/definitions/intermediate_pb_type'
    """
    pass

def gen_block(xmlgen, block):
    """Generate a top-level <pb_type> tag for the given ``block``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        block (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/block.schema.json'
    """
    pass

def gen_arch_xml(ostream, delegate, pretty = True):
    """Stream generate VPR's architecture description XML.

    Args:
        ostream: a file-like object, like a `file` or a `StringIO`
        delegate (`ArchitectureDelegate`): the delegate which answers questions about what are in the architecture
        pretty (:obj:`bool`): if the output XML file should be nicely broken into multiple lines and indented
    """
    with XMLGenerator(ostream, pretty) as xg:
        with xg.element("architecture"):
            # 1. models
            with xg.element("models"):
                for model in delegate.iter_models():
                    gen_model(xg, model)
            # 2. segments
            with xg.element("segmentlist"):
                for segment in delegate.iter_segments():
                    gen_segment(xg, segment)
            # 3. switches
            with xg.element("switchlist"):
                for switch in delegate.iter_switches():
                    gen_switch(xg, switch)
            # 4. fake device
            with xg.element("device"):
                xg.element_leaf("sizing", {"R_minW_nmos": 0, "R_minW_pmos": 0})
                xg.element_leaf("connection_block", {"input_switch_name": next(delegate.iter_switches())["name"]})
                xg.element_leaf("area", {"grid_logic_tile_area": 0})
                xg.element_leaf("switch_block", {"type": "wilton", "fs": 3})
                xg.element_leaf("default_fc", {"in_type": "frac", "in_val": 0.5, "out_type": "frac", "out_val": 0.5})
