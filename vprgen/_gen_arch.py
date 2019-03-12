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

def gen_interconnect(xmlgen, interconnect):
    """Generate a <interconnect> tag for the given ``interconnect``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        interconnect (:obj:`dict`): a `dict` satisfying the JSON schema
            'schema/block.schema.json/definitions/interconnect'
    """
    with xmlgen.element("interconnect"):
        for itx_type in ("complete", "direct", "mux"):
            for itx in interconnect.get(itx_type, []):
                with xmlgen.element(itx_type, {
                    "name": itx["name"],
                    "input": itx["input"],
                    "output": itx["output"], }):
                    for key in ("pack_pattern", "delay_constant"):
                        for item in itx.get(key, []):
                            xmlgen.element_leaf(key, item)
                    for delay_matrix in itx.get("delay_matrix", []):
                        gen_delay_matrix(xmlgen, delay_matrix)

def gen_mode(xmlgen, mode):
    """Generate a <mode> tag for the given ``mode``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        mode (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/block.schema.json/definitions/mode'
    """
    with xmlgen.element("mode", {"name": mode["name"]}):
        for pb_type in mode.get("pb_type", []):
            gen_intermediate_pb_type(xmlgen, pb_type)
        interconnect = mode.get("interconnect", None)
        if interconnect:
            gen_interconnect(xmlgen, interconnect)

def gen_intermediate_pb_type(xmlgen, pb_type):
    """Generate an intermediate <pb_type> tag for the given ``pb_type``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        pb_type (:obj:`dict`): a `dict` satisfying the JSON schema
            'schema/block.schema.json/definitions/intermediate_pb_type'
    """
    if "pb_type" not in pb_type and "mode" not in pb_type:
        gen_leaf_pb_type(xmlgen, pb_type)
        return
    with xmlgen.element("pb_type", {
        "name": pb_type["name"],
        "num_pb": pb_type.get("num_pb", 1), }):
        for key in ("input", "output", "clock"):
            for item in pb_type.get(key, []):
                xmlgen.element_leaf(key, item)
        for mode in pb_type.get("mode", []):
            gen_mode(xmlgen, mode)
        for sub_pb in pb_type.get("pb_type", []):
            gen_intermediate_pb_type(xmlgen, sub_pb)
        interconnect = pb_type.get("interconnect", None)
        if interconnect:
            gen_interconnect(xmlgen, interconnect)

def gen_block(xmlgen, block):
    """Generate a top-level <pb_type> tag for the given ``block``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        block (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/block.schema.json'
    """
    with xmlgen.element("pb_type", {
        "name": block["name"],
        "capacity": block.get("capacity", 1),
        "width": block.get("width", 1),
        "height": block.get("height", 1), }):
        for input_ in block.get("input", []):
            attrs = {
                "name": input_["name"],
                "num_pins": input_["num_pins"], }
            equivalent = input_.get("equivalent", None)
            if equivalent:
                attrs["equivalent"] = equivalent
            is_non_clock_global = input_.get("is_non_clock_global", False)
            if is_non_clock_global:
                attrs["is_non_clock_global"] = "true"
            xmlgen.element_leaf("input", attrs)
        for key in ("output", "clock"):
            for item in block.get(key, []):
                xmlgen.element_leaf(key, item)
        for mode in block.get("mode", []):
            gen_mode(xmlgen, mode)
        for pb_type in block.get("pb_type", []):
            gen_intermediate_pb_type(xmlgen, pb_type)
        interconnect = block.get("interconnect", None)
        if interconnect:
            gen_interconnect(xmlgen, interconnect)
        fc = block.get("fc", None)
        if fc:
            with xmlgen.element("fc", {
                "in_type": fc["in_type"],
                "in_val": fc["in_val"],
                "out_type": fc["out_type"],
                "out_val": fc["out_val"], }):
                for fc_override in fc.get("fc_override", []):
                    xmlgen.element_leaf("fc_override", fc_override)
        pinlocations = block.get("pinlocations", None)
        if pinlocations:
            with xmlgen.element("pinlocations", {
                "pattern": pinlocations["pattern"], }):
                for loc in pinlocations.get("loc", []):
                    xmlgen.element_leaf("loc", {
                        "side": loc["side"],
                        "xoffset": loc.get("xoffset", 0),
                        "yoffset": loc.get("yoffset", 0), },
                        " ".join(loc["ports"]))
        switchblock_locations = block.get("switchblock_locations", None)
        if switchblock_locations:
            with xmlgen.element("switchblock_locations", {
                "pattern": switchblock_locations["pattern"], }):
                for sb_loc in switchblock_locations.get("sb_loc", []):
                    attrs = { "type": sb_loc["type"],
                            "xoffset": sb_loc.get("xoffset", 0),
                            "yoffset": sb_loc.get("yoffset", 0), }
                    switch_override = sb_loc.get("switch_override", None)
                    if switch_override:
                        attrs["switch_override"] = switch_override
                    xmlgen.element_leaf("sb_loc", attrs)

def gen_arch_xml(ostream, delegate, pretty = True):
    """Stream generate VPR's architecture description XML.

    Args:
        ostream: a file-like object, like a `file` or a `StringIO`
        delegate (`ArchitectureDelegate`): the delegate which answers questions about what are in the architecture
        pretty (:obj:`bool`): if the output XML file should be nicely broken into multiple lines and indented
    """
    with XMLGenerator(ostream, pretty) as xmlgen:
        with xmlgen.element("architecture"):
            # 1. models
            with xmlgen.element("models"):
                for model in delegate.iter_models():
                    gen_model(xmlgen, model)
            # 2. segments
            with xmlgen.element("segmentlist"):
                for segment in delegate.iter_segments():
                    gen_segment(xmlgen, segment)
            # 3. switches
            with xmlgen.element("switchlist"):
                for switch in delegate.iter_switches():
                    gen_switch(xmlgen, switch)
            # 4. blocks
            with xmlgen.element("complexblocklist"):
                for block in delegate.iter_blocks():
                    gen_block(xmlgen, block)
            # 5. fake device
            with xmlgen.element("device"):
                xmlgen.element_leaf("sizing", {"R_minW_nmos": 0, "R_minW_pmos": 0})
                xmlgen.element_leaf("connection_block", {"input_switch_name": next(delegate.iter_switches())["name"]})
                xmlgen.element_leaf("area", {"grid_logic_tile_area": 0})
                xmlgen.element_leaf("switch_block", {"type": "wilton", "fs": 3})
                xmlgen.element_leaf("default_fc", {"in_type": "frac", "in_val": 0.5, "out_type": "frac", "out_val": 0.5})
