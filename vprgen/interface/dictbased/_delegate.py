from future.builtins import range, object

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
from itertools import product
import os

_model_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "model.schema.json")))
_segment_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "segment.schema.json")))
_switch_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "switch.schema.json")))
_direct_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "direct.schema.json")))
_block_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "block.schema.json")))
_tile_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "tile.schema.json")))
_node_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "node.schema.json")))
_edge_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "edge.schema.json")))

# ----------------------------------------------------------------------------
# -- Architecture Delegate ---------------------------------------------------
# ----------------------------------------------------------------------------
class ArchitectureDelegate(object):
    """Delegate class which is able to answer questions about what are in the architecture."""

    # -- User-defined methods ------------------------------------------------
    def iter_models(self):
        """Iterate or generate data for the <model> tags under the <models> tag in VPR's architecture description XML.

        Each element in the returned iterator/generator should be a `dict` satisfying the JSON schema
        'schema/model.schema.json'.
        """
        return
        yield None  # mark this method as a generator

    def iter_blocks(self):
        """Iterate or generate blocks for the <pb_type> tags under the <complexblocklist> tag in VPR's architecture
        description XML and the <block_type> tags under the <block_types> tag in VPR's routing resource graph XML.

        Each element in the returned iterator/generator should be a `dict` satisfying the JSON schema
        'schema/block.schema.json'. The order of the ports will be used to determine the `pin_id` of each port.
        """
        return
        yield None  # mark this method as a generator

    def get_width(self):
        """Width of the FPGA grid."""
        raise NotImplementedError

    def get_height(self):
        """Height of the FPGA grid."""
        raise NotImplementedError

    def get_layout_name(self):
        """Name of the layout."""
        return "default"

    def get_tile(self, x, y):
        """Get the physical block at tile (x, y).

        The returned value should be None or a `dict` satisfying the JSON schema 'schema/tile.schema.json'. If None is
        returned, the tile is treated as "EMPTY".
        """
        return None

    def get_device(self):
        """Get the device information.

        The returned value should be a `dict` satisfying the JSON schema 'schema/device.schema.json'. If None is
        returned, a fake <device> tag will be generated and used.
        """
        return None

    def iter_segments(self):
        """Iterate or generate segments for the <segment> tags under the <segmentlist> tag in VPR's architecture
        description XML and the <segment> tag under the <segments> tag in VPR's routing resource graph XML.

        Each element in the returned iterator/generator should be a `dict` satisfying the JSON schema
        'schema/segment.schema.json'.
        """
        return
        yield None  # mark this method as a generator

    def iter_switches(self):
        """Iterate or generate switches for the <switch> tags under the <switchlist> tag in VPR's architecture
        description XML and the <switches> tag under the <switches> tag in VPR's routing resource graph XML.

        Each element in the returned iterator/generator should be a `dict` satisfying the JSON schema
        'schema/switch.schema.json'.
        """
        return
        yield None  # mark this method as a generator

    def iter_directs(self):
        """Iterate or generate directs for the <direct> tags under the <directlist> tag in VPR's architecture
        description XML.

        Each element in the returned iterator/generator should be a `dict` satisfying the JSON schema
        'schema/direct.schema.json'.
        """
        return
        yield None  # mark this method as a generator

    def get_x_channel_width(self):
        """Get the width of horizontal routing channels."""
        raise NotImplementedError

    def get_y_channel_width(self):
        """Get the width of vertical routing channels."""
        raise NotImplementedError

    def iter_nodes(self):
        """Iterate or generate routing nodes for the <node> tag under the <rr_nodes> tag in VPR's routing resource
        graph XML.

        Each element in the returned iterator/generator should be a `dict` satisfying the JSON schema
        'schema/source_sink.schema.json' or 'schema/ipin_opin.schema.json' or 'schema/chanx_chany.schema.json'.
        """
        return
        yield None  # mark this method as a generator

    def iter_edges(self):
        """Iterate or generate routing edges for the <edge> tag under the <rr_edges> tag in VPR's routing resource
        graph XML.

        Each element in the returned iterator/generator should be a `dict` satisfying the JSON schema
        'schema/edge.schema.json'.
        """
        return
        yield None  # mark this method as a generator

    # -- API -----------------------------------------------------------------
    def gen_arch_xml(self, ostream, pretty = True):
        """Stream generate VPR's architecture description XML.

        Args:
            ostream: a file-like object, like a `file` or a `StringIO`
            pretty (:obj:`bool`): if the output XML file should be nicely broken into multiple lines and indented
        """
        with XMLGenerator(ostream, pretty) as xmlgen:
            with xmlgen.element("architecture"):
                # 1. models
                with xmlgen.element("models"):
                    for model in self.iter_models():
                        self._gen_model(xmlgen, model)
                # 2. segments
                with xmlgen.element("segmentlist"):
                    for segment in self.iter_segments():
                        self._gen_arch_segment(xmlgen, segment)
                # 3. switches
                with xmlgen.element("switchlist"):
                    for switch in self.iter_switches():
                        self._gen_arch_switch(xmlgen, switch)
                # 4. blocks
                with xmlgen.element("complexblocklist"):
                    for block in self.iter_blocks():
                        self._gen_arch_block(xmlgen, block)
                # 5. layout
                with xmlgen.element("layout"), xmlgen.element("fixed_layout", {
                    "name": self.get_layout_name(),
                    "width": self.get_width(),
                    "height": self.get_height(), }):
                    for x, y in product(range(self.get_width()), range(self.get_height())):
                        tile = self.get_tile(x, y)
                        if tile:
                            self._gen_arch_tile(xmlgen, tile, x, y)
                # 6. directs
                with xmlgen.element("directlist"):
                    for direct in self.iter_directs():
                        self._gen_direct(xmlgen, direct)
                # 7. fake device
                with xmlgen.element("device"):
                    xmlgen.element_leaf("sizing", {"R_minW_nmos": 0, "R_minW_pmos": 0})
                    xmlgen.element_leaf("connection_block", {"input_switch_name": next(self.iter_switches())["name"]})
                    xmlgen.element_leaf("area", {"grid_logic_tile_area": 0})
                    xmlgen.element_leaf("switch_block", {"type": "wilton", "fs": 3})
                    xmlgen.element_leaf("default_fc", {"in_type": "frac", "in_val": 0.5, "out_type": "frac", "out_val": 0.5})

    def gen_rrg_xml(self, ostream, pretty = True):
        """Stream generate VPR's routing resource graph XML.

        Args:
            ostream: a file-like object, like a `file` or a `StringIO`
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
                        self._gen_rrg_segment(xmlgen, segment)
                # 3. switches
                with xmlgen.element("switches"):
                    for switch in delegate.iter_switches():
                        self._gen_rrg_switch(xmlgen, switch)
                # 4. blocks
                with xmlgen.element("block_types"):
                    xmlgen.element_leaf("block_type", {
                        "name": "EMPTY",
                        "id": 0,
                        "width": 1,
                        "height": 1, })
                    for block in delegate.iter_blocks():
                        self._gen_rrg_block(xmlgen, block)
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
                            self._gen_rrg_tile(xmlgen, tile)
                # 6. nodes
                with xmlgen.element("rr_nodes"):
                    for node in delegate.iter_nodes():
                        self._gen_node(xmlgen, node)
                # 7. edges
                with xmlgen.element("rr_edges"):
                    for node in delegate.iter_edges():
                        self._gen_edge(xmlgen, edge)

    # -- Private methods -----------------------------------------------------
    def _gen_model(self, xmlgen, model):
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

    def _gen_arch_segment(self, xmlgen, segment):
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
    
    def _gen_arch_switch(self, xmlgen, switch):
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
    
    def _gen_direct(self, xmlgen, direct):
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
    
    def _gen_delay_matrix(self, xmlgen, delay):
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
    
    def _gen_leaf_pb_type(self, xmlgen, pb_type):
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
                self._gen_delay_matrix(xmlgen, delay_matrix)
    
    def _gen_interconnect(self, xmlgen, interconnect):
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
                            self._gen_delay_matrix(xmlgen, delay_matrix)
    
    def _gen_mode(self, xmlgen, mode):
        """Generate a <mode> tag for the given ``mode``.
    
        Args:
            xmlgen (`XMLGenerator`): the generator to be used
            mode (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/block.schema.json/definitions/mode'
        """
        with xmlgen.element("mode", {"name": mode["name"]}):
            for pb_type in mode.get("pb_type", []):
                self._gen_intermediate_pb_type(xmlgen, pb_type)
            interconnect = mode.get("interconnect", None)
            if interconnect:
                self._gen_interconnect(xmlgen, interconnect)
    
    def _gen_intermediate_pb_type(self, xmlgen, pb_type):
        """Generate an intermediate <pb_type> tag for the given ``pb_type``.
    
        Args:
            xmlgen (`XMLGenerator`): the generator to be used
            pb_type (:obj:`dict`): a `dict` satisfying the JSON schema
                'schema/block.schema.json/definitions/intermediate_pb_type'
        """
        if "pb_type" not in pb_type and "mode" not in pb_type:
            self._gen_leaf_pb_type(xmlgen, pb_type)
            return
        with xmlgen.element("pb_type", {
            "name": pb_type["name"],
            "num_pb": pb_type.get("num_pb", 1), }):
            for key in ("input", "output", "clock"):
                for item in pb_type.get(key, []):
                    xmlgen.element_leaf(key, item)
            for mode in pb_type.get("mode", []):
                self._gen_mode(xmlgen, mode)
            for sub_pb in pb_type.get("pb_type", []):
                self._gen_intermediate_pb_type(xmlgen, sub_pb)
            interconnect = pb_type.get("interconnect", None)
            if interconnect:
                self._gen_interconnect(xmlgen, interconnect)
    
    def _gen_arch_block(self, xmlgen, block):
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
                self._gen_mode(xmlgen, mode)
            for pb_type in block.get("pb_type", []):
                self._gen_intermediate_pb_type(xmlgen, pb_type)
            interconnect = block.get("interconnect", None)
            if interconnect:
                self._gen_interconnect(xmlgen, interconnect)
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
    
    def _gen_arch_tile(self, xmlgen, tile, x, y):
        """Generate a <single> tag for the given ``tile``.
    
        Args:
            xmlgen (`XMLGenerator`): the generator to be used
            tile (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/tile.schema.json'
            x (:obj:`int`): the X position
            y (:obj:`int`): the Y position
        """
        if tile.get("xoffset", 0) == 0 and tile.get("yoffset", 0) == 0:
            xmlgen.element_leaf("single", {
                "type": tile["type"],
                "x": x,
                "y": y,
                "priority": 1})

    def _gen_rrg_segment(self, xmlgen, segment):
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
    
    def _gen_rrg_switch(self, xmlgen, switch):
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
    
    def _gen_rrg_block(self, xmlgen, block):
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
                                    "{}.{}[{}]".format(block["name"], port["name"], bit))
                            else:
                                xmlgen.element_leaf("pin", {
                                    "ptc": next(ptc_it), },
                                    "{}[{}].{}[{}]".format(block["name"], z, port["name"], bit))
    
    def _gen_rrg_tile(self, xmlgen, tile, x, y):
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
    
    def _gen_node(self, xmlgen, node):
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
    
    def _gen_edge(self, xmlgen, edge):
        """Generate a <edge> tag for the given ``edge``.
    
        Args:
            xmlgen (`XMLGenerator`): the generator to be used
            edge (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/edge.schema.json'
        """
        # 1. validate argument
        validate(instance = edge, schema = _edge_schema)
        # 2. generate tag
        xmlgen.element_leaf("edge", edge)
