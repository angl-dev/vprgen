from future.utils import with_metaclass
from future.builtins import range, object

try:
    from itertools import imap as map
except ImportError:
    pass

try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

from vprgen.abstractbased._abstract import *
from vprgen._xml import XMLGenerator

from abc import ABCMeta, abstractproperty
from typing import Iterable, Union, Optional
from itertools import product

_empty_iterable = tuple()

# ----------------------------------------------------------------------------
# -- Architecture Delegate ---------------------------------------------------
# ----------------------------------------------------------------------------
class ArchitectureDelegate(with_metaclass(ABCMeta, object)):
    """Delegate class which is able to answer questions about what are in the architecture."""
    # -- required properties -------------------------------------------------
    @abstractproperty
    def name(self):
        """Name of the fixed layout."""
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": str}

    @abstractproperty
    def width(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    width.fget.__annotations__ = {"return": int}

    @abstractproperty
    def height(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    height.fget.__annotations__ = {"return": int}

    @abstractproperty
    def x_channel_width(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    x_channel_width.fget.__annotations__ = {"return": int}

    @abstractproperty
    def y_channel_width(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    y_channel_width.fget.__annotations__ = {"return": int}

    # -- optional properties -------------------------------------------------
    @property
    def models(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    models.fget.__annotations__ = {"return": Iterable[AbstractModel]}

    @property
    def complex_blocks(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    complex_blocks.fget.__annotations__ = {"return": Iterable[AbstractTopPbType]}

    @property
    def segments(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    segments.fget.__annotations__ = {"return": Iterable[AbstractSegment]}

    @property
    def switches(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    switches.fget.__annotations__ = {"return": Iterable[AbstractSwitch]}

    @property
    def directs(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    directs.fget.__annotations__ = {"return": Iterable[AbstractDirect]}

    @property
    def nodes(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    nodes.fget.__annotations__ = {"return": Iterable[AbstractNode]}

    @property
    def edges(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    edges.fget.__annotations__ = {"return": Iterable[AbstractEdge]}

    def get_tile(self, x, y):
        """Get the complex block at tile (x, y)."""
        return None
    # Python 2 and 3 compatible type checking
    get_tile.__annotations__ = {"x": int, "y": int, "return": Optional[AbstractTile]}

    # -- API -----------------------------------------------------------------
    def gen_arch_xml(self, ostream, pretty = True):
        """Stream generate VPR's architecture description XML.

        Args:
            ostream: a file-like object, like a `file` or a `StringIO`
            pretty (:obj:`bool`): if the output XML file should be nicely broken into multiple lines and indented
        """
        with XMLGenerator(ostream, pretty, True) as xmlgen:
            with xmlgen.element("architecture"):
                # 1. models
                with xmlgen.element("models"):
                    for model in self.models:
                        self._gen_model(xmlgen, model)
                # 2. segments
                with xmlgen.element("segmentlist"):
                    for segment in self.segments:
                        self._gen_arch_segment(xmlgen, segment)
                # 3. switches
                with xmlgen.element("switchlist"):
                    for switch in self.switches:
                        self._gen_arch_switch(xmlgen, switch)
                # 4. blocks
                with xmlgen.element("complexblocklist"):
                    for block in self.complex_blocks:
                        self._gen_arch_block(xmlgen, block)
                # 5. layout
                with xmlgen.element("layout"), xmlgen.element("fixed_layout", {
                    "name": self.name,
                    "width": str(self.width),
                    "height": str(self.height), }):
                    for x, y in product(range(self.width), range(self.height)):
                        tile = self.get_tile(x, y)
                        if tile:
                            self._gen_arch_tile(xmlgen, tile, x, y)
                # 6. directs
                with xmlgen.element("directlist"):
                    for direct in self.directs:
                        self._gen_direct(xmlgen, direct)
                # 7. fake device
                with xmlgen.element("device"):
                    xmlgen.element_leaf("sizing", {"R_minW_nmos": "0", "R_minW_pmos": "0"})
                    xmlgen.element_leaf("connection_block", {"input_switch_name": next(iter(self.switches)).name})
                    xmlgen.element_leaf("area", {"grid_logic_tile_area": "0"})
                    xmlgen.element_leaf("switch_block", {"type": "wilton", "fs": "3"})
                    xmlgen.element_leaf("default_fc", {"in_type": "frac", "in_val": "0.5",
                        "out_type": "frac", "out_val": "0.5"})

    def gen_rrg_xml(self, ostream, pretty = True):
        """Stream generate VPR's routing resource graph XML.

        Args:
            ostream: a file-like object, like a `file` or a `StringIO`
            pretty (:obj:`bool`): if the output XML file should be nicely broken into multiple lines and indented
        """
        raise NotImplementedError
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
        """Generate a <model> tag for the given ``model``."""
        with xmlgen.element("model", {"name": model.name}):
            if model.input_ports:
                with xmlgen.element("input_ports"):
                    for port in model.input_ports:
                        attrs = {"name": port.name}
                        if port.is_clock:
                            attrs["is_clock"] = "1"
                        if port.clock:
                            attrs["clock"] = port.clock
                        sink = " ".join(port.combinational_sink_ports)
                        if sink:
                            attrs["combinational_sink_ports"] = sink
                        xmlgen.element_leaf("port", attrs)
            if model.output_ports:
                with xmlgen.element("output_ports"):
                    for port in model.output_ports:
                        attrs = {"name": port.name}
                        if port.is_clock:
                            attrs["is_clock"] = "1"
                        if port.clock:
                            attrs["clock"] = port.clock
                        xmlgen.element_leaf("port", attrs)
    # Python 2 and 3 compatible type checking
    _gen_model.__annotations__ = {"xmlgen": XMLGenerator, "model": AbstractModel}

    def _gen_arch_segment(self, xmlgen, segment):
        """Generate a <segment> tag for the given ``segment``."""
        with xmlgen.element("segment", {
            "name": segment.name,
            "length": str(segment.length),
            "type": "unidir",
            "freq": str(segment.freq),
            "Rmetal": str(segment.Rmetal),
            "Cmetal": str(segment.Cmetal),
            }):
            xmlgen.element_leaf("sb", {"type": "pattern"}, " ".join(map(lambda x: "1" if x else "0",
                segment.sb or ((True, ) * (segment.length + 1)))))
            xmlgen.element_leaf("cb", {"type": "pattern"}, " ".join(map(lambda x: "1" if x else "0",
                segment.cb or ((True, ) * segment.length))))
            xmlgen.element_leaf("mux", {"name": segment.mux})
    # Python 2 and 3 compatible type checking
    _gen_arch_segment.__annotations__ = {"xmlgen": XMLGenerator, "segment": AbstractSegment}

    def _gen_arch_switch(self, xmlgen, switch):
        """Generate a <switch> tag for the given ``switch``."""
        attrs = { "type": "buffer" if switch.type_ is SwitchType.buffer_ else switch.type_.name,
                "name": switch.name,
                "R": str(switch.R),
                "Cin": str(switch.Cin),
                "Cout": str(switch.Cout), }
        if isinstance(switch.Tdel, Iterable):
            with xmlgen.element("switch", attrs):
                for item in switch.Tdel:
                    Tdel_attrs = { "num_inputs": str(item.num_inputs),
                            "delay": str(item.delay), }
                    xmlgen.element_leaf("Tdel", Tdel_attrs)
        else:
            attrs["Tdel"] = str(switch.Tdel)
            xmlgen.element_leaf("switch", attrs)
    # Python 2 and 3 compatible type checking
    _gen_arch_switch.__annotations__ = {"xmlgen": XMLGenerator, "switch": AbstractSwitch}

    def _gen_arch_combinational_timing(self, xmlgen, parent):
        """Generate a series of <delay_constant> and <delay_matrix> tags for the given ``parent``."""
        for delay_constant in parent.delay_constants:
            attrs = { "in_port": delay_constant.in_port,
                    "out_port": delay_constant.out_port, }
            if delay_constant.min_ is not None:  # in case min_ is 0.0
                attrs["min"] = str(delay_constant.min_)
            if delay_constant.max_ is not None:  # in case max_ is 0.0
                attrs["max"] = str(delay_constant.max_)
            xmlgen.element_leaf('delay_constant', attrs)
        for delay_matrix in parent.delay_matrices:
            xmlgen.element_leaf('delay_matrix', {
                "type": "max" if delay_matrix.type_ is DelayMatrixType.max_ else "min",
                "in_port": delay_matrix.in_port,
                "out_port": delay_matrix.out_port, },
                '\n' + '\n'.join(' '.join(str(v) for v in vector) for vector in delay_matrix.values))
    # Python 2 and 3 compatible type checking
    _gen_arch_combinational_timing.__annotations__ = {
            "xmlgen": XMLGenerator, "parent": Union[AbstractLeafPbType, AbstractInterconnectItem], }

    def _gen_arch_sequential_timing(self, xmlgen, parent):
        """Generate a series of <T_setup>, <T_hold> and <T_clock_to_Q> tags for the given ``parent``."""
        for tag, iterable in (("T_setup", parent.T_setups), ("T_hold", parent.T_holds)):
            for item in iterable:
                xmlgen.element_leaf(tag, {
                    "port": item.port,
                    "clock": item.clock,
                    "value": str(item.value), })
        for T_clock_to_Q in parent.T_clock_to_Qs:
            attrs = { "port": T_clock_to_Q.port,
                    "clock": T_clock_to_Q.clock, }
            if T_clock_to_Q.min_ is not None:  # in case min_ is 0.0
                attrs["min"] = str(T_clock_to_Q.min_)
            if T_clock_to_Q.max_ is not None:  # in case max_ is 0.0
                attrs["max"] = str(T_clock_to_Q.max_)
            xmlgen.element_leaf('T_clock_to_Q', attrs)
    # Python 2 and 3 compatible type checking
    _gen_arch_combinational_timing.__annotations__ = {
            "xmlgen": XMLGenerator, "parent": AbstractLeafPbType, }

    def _gen_leaf_pb_type(self, xmlgen, pb_type):
        """Generate a leaf <pb_type> tag for the given ``pb_type``."""
        attrs = { "name": pb_type.name,
                "blif_model": pb_type.blif_model,
                "num_pb": str(pb_type.num_pb), }
        if pb_type.class_:
            attrs["class"] = pb_type.class_.name
        with xmlgen.element("pb_type", attrs):
            for tag, iterable in (("input", pb_type.inputs),
                    ("output", pb_type.outputs),
                    ("clock", pb_type.clocks)):
                for port in iterable:
                    attrs = { "name": port.name,
                            "num_pins": str(port.num_pins), }
                    if port.port_class:
                        attrs["port_class"] = port.port_class.name
                    xmlgen.element_leaf(tag, attrs)
            self._gen_arch_sequential_timing(xmlgen, pb_type)
            self._gen_arch_combinational_timing(xmlgen, pb_type)
    # Python 2 and 3 compatible type checking
    _gen_arch_combinational_timing.__annotations__ = {
            "xmlgen": XMLGenerator, "parent": AbstractLeafPbType, }

    def _gen_interconnect(self, xmlgen, parent):
        """Generate a <interconnect> tag for the given ``parent``."""
        with xmlgen.element("interconnect"):
            for tag, iterable in (("complete", parent.completes),
                    ("direct", parent.directs),
                    ("mux", parent.muxes)):
                for item in iterable:
                    with xmlgen.element(tag, {
                        "name": item.name,
                        "input": ' '.join(item.inputs),
                        "output": ' '.join(item.outputs), }):
                        self._gen_arch_combinational_timing(xmlgen, item)
                        for pack_pattern in item.pack_patterns:
                            xmlgen.element_leaf("pack_pattern", {
                                "name": pack_pattern.name,
                                "in_port": pack_pattern.in_port,
                                "out_port": pack_pattern.out_port, })
    # Python 2 and 3 compatible type checking
    _gen_interconnect.__annotations__ = { "xmlgen": XMLGenerator,
            "parent": Union[AbstractMode, AbstractIntermediatePbType, AbstractTopPbType], }

    def _gen_mode(self, xmlgen, mode):
        """Generate a <mode> tag for the given ``mode``."""
        with xmlgen.element("mode", {"name": mode.name}):
            for pb_type in mode.pb_types:
                if isinstance(pb_type, AbstractLeafPbType):
                    self._gen_leaf_pb_type(xmlgen, pb_type)
                else:
                    self._gen_intermediate_pb_type(xmlgen, pb_type)
            self._gen_interconnect(xmlgen, mode)
    # Python 2 and 3 compatible type checking
    _gen_mode.__annotations__ = {"xmlgen": XMLGenerator, "mode": AbstractMode}

    def _gen_intermediate_pb_type(self, xmlgen, pb_type):
        """Generate an intermediate <pb_type> tag for the given ``pb_type``."""
        with xmlgen.element("pb_type", {
            "name": pb_type.name,
            "num_pb": str(pb_type.num_pb), }):
            for tag, iterable in (("input", pb_type.inputs),
                    ("output", pb_type.outputs),
                    ("clock", pb_type.clocks)):
                for port in iterable:
                    xmlgen.element_leaf(tag, {
                        "name": port.name,
                        "num_pins": str(port.num_pins), })
            got_modes = False
            for mode in pb_type.modes:
                got_modes = True
                self._gen_mode(xmlgen, mode)
            if got_modes:
                return
            for sub_pb in pb_type.pb_types:
                if isinstance(sub_pb, AbstractLeafPbType):
                    self._gen_leaf_pb_type(xmlgen, sub_pb)
                else:
                    self._gen_intermediate_pb_type(xmlgen, sub_pb)
            self._gen_interconnect(xmlgen, pb_type)
    # Python 2 and 3 compatible type checking
    _gen_mode.__annotations__ = {"xmlgen": XMLGenerator, "pb_type": AbstractIntermediatePbType}

    def _gen_arch_block(self, xmlgen, block):
        """Generate a top-level <pb_type> tag for the given ``block``."""
        with xmlgen.element("pb_type", {
            "name": block.name,
            "capacity": str(block.capacity),
            "width": str(block.width),
            "height": str(block.height), }):
            for input_ in block.inputs:
                attrs = { "name": input_.name,
                        "num_pins": str(input_.num_pins), }
                if input_.equivalent:
                    attrs["equivalent"] = input_.equivalent.name
                if input_.is_non_clock_global:
                    attrs["is_non_clock_global"] = "true"
                xmlgen.element_leaf("input", attrs)
            for output in block.outputs:
                attrs = { "name": output.name,
                        "num_pins": str(output.num_pins), }
                if output.equivalent:
                    attrs["equivalent"] = output.equivalent.name
                xmlgen.element_leaf("output", attrs)
            for clock in block.clocks:
                attrs = { "name": clock.name,
                        "num_pins": str(clock.num_pins), }
                if clock.equivalent:
                    attrs["equivalent"] = clock.equivalent.name
                xmlgen.element_leaf("clock", attrs)
            if block.fc:
                with xmlgen.element('fc', {
                    "in_type": "abs" if block.fc.in_type is FCType.abs_ else "frac",
                    "out_type": "abs" if block.fc.out_type is FCType.abs_ else "frac",
                    "in_val": str(block.fc.in_val),
                    "out_val": str(block.fc.out_val), }):
                    for fc_override in block.fc.fc_overrides:
                        xmlgen.element_leaf("fc_override", {
                            "fc_type": "abs" if block.fc.in_type is FCType.abs_ else "frac",
                            "port_name": fc_override.port_name,
                            "segment_name": fc_override.segment_name,
                            "fc_val": str(fc_override.fc_val), })
            if block.pinlocations:
                with xmlgen.element('pinlocations', {
                    "pattern": block.pinlocations.pattern.name, }):
                    for loc in block.pinlocations.locs:
                        xmlgen.element_leaf("loc", {
                            "side": loc.side.name,
                            "xoffset": str(loc.xoffset),
                            "yoffset": str(loc.yoffset), },
                            " ".join(loc.ports))
            if block.switchblock_locations:
                with xmlgen.element("switchblock_locations", {
                    "pattern": ("all" if block.switchblock_locations.pattern is SwitchblockLocationsPattern.all_ else
                        block.switchblock_locations.pattern.name), }):
                        for loc in block.switchblock_locations.sb_locs:
                            attrs = {
                                "type": loc.type_.name,
                                "xoffset": str(loc.xoffset),
                                "yoffset": str(loc.yoffset), }
                            if loc.switch_override:
                                attrs['switch_override'] = loc.switch_override
                            xmlgen.element_leaf("sb_loc", attrs)
            got_modes = False
            for mode in block.modes:
                got_modes = True
                self._gen_mode(xmlgen, mode)
            if got_modes:
                return
            for sub_pb in block.pb_types:
                if isinstance(sub_pb, AbstractLeafPbType):
                    self._gen_leaf_pb_type(xmlgen, sub_pb)
                else:
                    self._gen_intermediate_pb_type(xmlgen, sub_pb)
            self._gen_interconnect(xmlgen, block)
    # Python 2 and 3 compatible type checking
    _gen_arch_block.__annotations__ = {"xmlgen": XMLGenerator, "block": AbstractTopPbType}
    
    def _gen_arch_tile(self, xmlgen, tile, x, y):
        """Generate a <single> tag for the given ``tile``."""
        if tile.xoffset == 0 and tile.yoffset == 0:
            xmlgen.element_leaf("single", {
                "type": tile.type_,
                "x": str(x),
                "y": str(y),
                "priority": str(1)})
    # Python 2 and 3 compatible type checking
    _gen_arch_tile.__annotations__ = {"xmlgen": XMLGenerator, "tile": AbstractTile, "x": int, "y": int}
    
    def _gen_direct(self, xmlgen, direct):
        """Generate a <direct> tag for the given ``direct``."""
        xmlgen.element_leaf("direct", {
            "name": direct.name,
            "from_pin": direct.from_pin,
            "to_pin": direct.to_pin,
            "switch_name": direct.switch_name,
            "x_offset": str(direct.x_offset),
            "y_offset": str(direct.y_offset),
            "z_offset": str(direct.z_offset), })
    # Python 2 and 3 compatible type checking
    _gen_direct.__annotations__ = {"xmlgen": XMLGenerator, "direct": AbstractDirect}
