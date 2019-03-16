from future.utils import iteritems

from typing import Iterable, Tuple, Any, Optional, Union
from vprgen.abstractbased._abstract import *
from collections import namedtuple, OrderedDict

_empty_iterable = tuple()

def _namedtuple(class_name, attributes = _empty_iterable, defaults = _empty_iterable):
    """Enhanced `namedtuple` with default values and type hints.

    Args:
        attributes: an iterable of 2-tuples. first element is the name of the attribute, second element is
            the type hint
        defaults: an iterable of 3-tuples. the first two elements are the same as in attributes, the third element is
            the default value
    """
    cls = namedtuple(class_name,
            ' '.join(attr for attr, _ in attributes) + ' ' + ' '.join(attr for attr, _0, _1 in defaults))
    cls.__new__.__annotations__ = {attr: type_ for attr, type_ in attributes}
    cls.__new__.__annotations__.update({attr: type_ for attr, type_, _ in defaults})
    cls.__new__.__defaults__ = tuple(default for _0, _1, default in defaults)
    return cls
# Python 2 and 3 compatible type checking
_namedtuple.__annotations__ = {"class_name": str,
        "attributes": Iterable[Tuple[str, type]],
        "defaults": Iterable[Tuple[str, type, Any]],
        "return": type}

class ModelOutputPort(_namedtuple('ModelOutputPort',
    attributes = (("name", str), ),
    defaults = (("is_clock", bool, False),
        ("clock", Optional[str], None), )),
    AbstractModelOutputPort):
    pass

class ModelInputPort(_namedtuple('ModelInputPort',
    attributes = (('name', str), ),
    defaults = (("is_clock", bool, False),
        ("clock", Optional[str], None),
        ("combinational_sink_ports", Iterable[str], _empty_iterable), )),
    AbstractModelInputPort):
    pass

class Model(_namedtuple('Model',
    attributes = (('name', str), ),
    defaults = (("input_ports", Iterable[AbstractModelInputPort], _empty_iterable),
        ("output_ports", Iterable[AbstractModelOutputPort], _empty_iterable), )),
    AbstractModel):
    pass

class Segment(_namedtuple('Segment',
    attributes = (('name', str),
        ('id_', int),
        ('length', int),
        ('mux', str)),
    defaults = (('freq', float, 0.0),
        ('Rmetal', float, 0.0),
        ('Cmetal', float, 0.0),
        ('sb', Optional[Iterable[bool]], None),
        ('cb', Optional[Iterable[bool]], None), )),
    AbstractSegment):
    pass

class SwitchTdel(_namedtuple('SwitchTdel',
    attributes = (('num_inputs', int),
        ('delay', float), )),
    AbstractSwitchTdel):
    pass

class Switch(_namedtuple('Switch',
    attributes = (('name', str),
        ('id_', int),
        ('Tdel', Union[float, Iterable[AbstractSwitchTdel]])),
    defaults = (('type_', SwitchType, SwitchType.mux),
        ('R', float, 0.0),
        ('Cin', float, 0.0),
        ('Cout', float, 0.0), )),
    AbstractSwitch):
    pass

class Direct(_namedtuple('Direct',
    attributes = (('name', str),
        ('from_pin', str),
        ('to_pin', str),
        ('switch_name', str), ),
    defaults = (('x_offset', int, 0),
        ('y_offset', int, 0),
        ('z_offset', int, 0), )),
    AbstractDirect):
    pass

class DelayConstant(_namedtuple('DelayConstant',
    attributes = (('in_port', str),
        ('out_port', str), ),
    defaults = (('min_', Optional[float], None),
        ('max_', Optional[float], None), )),
    AbstractDelayConstant):
    pass

class DelayMatrix(_namedtuple('DelayMatrix',
    attributes = (('type_', DelayMatrixType),
        ('in_port', str),
        ('out_port', str),
        ('values', Iterable[Iterable[float]]), )),
    AbstractDelayMatrix):
    pass

class TSetupOrHold(_namedtuple('TSetupOrHold',
    attributes = (('port', str),
        ('clock', str),
        ('value', float), )),
    AbstractTSetupOrTHold):
    pass

class TClockToQ(_namedtuple('TClockToQ',
    attributes = (('port', str),
        ('clock', str), ),
    defaults = (('min_', Optional[float], None),
        ('max_', Optional[float], None), )),
    AbstractTClockToQ):
    pass

class PbTypePort(_namedtuple('PbTypePort',
    attributes = (('name', str),
        ('num_pins', int), )),
    AbstractPbTypePort):
    pass

class LeafPbTypePort(_namedtuple('LeafPbTypePort',
    attributes = (('name', str),
        ('num_pins', int), ),
    defaults = (('port_class', Optional[LeafPbTypePortClass], None), )),
    AbstractLeafPbTypePort):
    pass

class LeafPbType(_namedtuple('LeafPbType',
    attributes = (('name', str),
        ('blif_model', str), ),
    defaults = (('num_pb', int, 1),
        ('class_', Optional[LeafPbTypeClass], None),
        ('inputs', Iterable[AbstractLeafPbTypePort], _empty_iterable),
        ('outputs', Iterable[AbstractLeafPbTypePort], _empty_iterable),
        ('clocks', Iterable[AbstractLeafPbTypePort], _empty_iterable),
        ('delay_constants', Iterable[AbstractDelayConstant], _empty_iterable),
        ('delay_matrices', Iterable[AbstractDelayMatrix], _empty_iterable),
        ('T_setups', Iterable[AbstractTSetupOrTHold], _empty_iterable),
        ('T_holds', Iterable[AbstractTSetupOrTHold], _empty_iterable),
        ('T_clock_to_Qs', Iterable[AbstractTClockToQ], _empty_iterable), )),
    AbstractLeafPbType):
    pass

class PackPattern(_namedtuple('PackPattern',
    attributes = (('name', str),
        ('in_port', str),
        ('out_port', str), )),
    AbstractPackPattern):
    pass

class InterconnectItem(_namedtuple('InterconnectItem',
    attributes = (('name', str),
        ('inputs', Iterable[str]),
        ('outputs', Iterable[str]), ),
    defaults = (('pack_patterns', Iterable[AbstractPackPattern], _empty_iterable),
        ('delay_constants', Iterable[AbstractDelayConstant], _empty_iterable),
        ('delay_matrices', Iterable[AbstractDelayMatrix], _empty_iterable), )),
    AbstractInterconnectItem):
    pass

class Mode(_namedtuple('Mode',
    attributes = (('name', str), ),
    defaults = (('completes', Iterable[AbstractInterconnectItem], _empty_iterable),
        ('muxes', Iterable[AbstractInterconnectItem], _empty_iterable),
        ('directs', Iterable[AbstractInterconnectItem], _empty_iterable),
        ('pb_types', Iterable[Union[AbstractLeafPbType, AbstractIntermediatePbType]], _empty_iterable), )),
    AbstractMode):
    pass

class IntermediatePbType(_namedtuple('IntermediatePbType', 
    attributes = (('name', str), ),
    defaults = (('num_pb', int, 1),
        ('inputs', Iterable[AbstractPbTypePort], _empty_iterable),
        ('outputs', Iterable[AbstractPbTypePort], _empty_iterable),
        ('clocks', Iterable[AbstractPbTypePort], _empty_iterable),
        ('modes', Iterable[AbstractMode], _empty_iterable),
        ('pb_types', Iterable[Union[AbstractLeafPbType, AbstractIntermediatePbType]], _empty_iterable),
        ('completes', Iterable[AbstractInterconnectItem], _empty_iterable),
        ('muxes', Iterable[AbstractInterconnectItem], _empty_iterable),
        ('directs', Iterable[AbstractInterconnectItem], _empty_iterable), )),
    AbstractIntermediatePbType):
    pass

class TopPbTypeOutputOrClockPort(_namedtuple('TopPbTypeOutputOrClockPort',
    attributes = (('name', str),
        ('num_pins', int), ),
    defaults = (('equivalent', Optional[TopPbTypePortEquivalent], None), )),
    AbstractTopPbTypeOutputOrClockPort):
    pass

class TopPbTypeInputPort(_namedtuple('TopPbTypeInputPort',
    attributes = (('name', str),
        ('num_pins', int), ),
    defaults = (('equivalent', Optional[TopPbTypePortEquivalent], None),
        ('is_non_clock_global', bool, False), )),
    AbstractTopPbTypeInputPort):
    pass

class FCOverride(_namedtuple('FCOverride',
    attributes = (('fc_type', FCType),
        ('port_name', str),
        ('segment_name', str),
        ('fc_val', Union[float, int]), )),
    AbstractFCOverride):
    pass

class FC(_namedtuple('FC',
    attributes = (('in_type', FCType),
        ('in_val', Union[float, int]),
        ('out_type', FCType),
        ('out_val', Union[float, int]), ),
    defaults = (('fc_overrides', Iterable[AbstractFCOverride], _empty_iterable), )),
    AbstractFC):
    pass

class PinLocationsLoc(_namedtuple('PinLocationsLoc',
    attributes = (('side', Side),
        ('ports', Iterable[str]), ),
    defaults = (('xoffset', int, 0),
        ('yoffset', int, 0), )),
    AbstractPinLocationsLoc):
    pass

class PinLocations(_namedtuple('PinLocations',
    attributes = (('pattern', PinLocationsPattern), ),
    defaults = (('locs', Iterable[AbstractPinLocationsLoc], _empty_iterable), )),
    AbstractPinLocations):
    pass

class SbLoc(_namedtuple('SbLoc',
    attributes = (('type_', SbLocType), ),
    defaults = (('xoffset', int, 0),
        ('yoffset', int, 0),
        ('switch_override', Optional[str], None), )),
    AbstractSbLoc):
    pass

class SwitchblockLocations(_namedtuple('SwitchblockLocations',
    attributes = (('pattern', SwitchblockLocationsPattern), ),
    defaults = (('sb_locs', Optional[Iterable[AbstractSbLoc]], None), )),
    AbstractSwitchblockLocations):
    pass

class TopPbType(_namedtuple('TopPbType',
    attributes = (('name', str),
        ('id_', int), ),
    defaults = (('capacity', int, 1),
        ('width', int, 1),
        ('height', int, 1),
        ('inputs', Iterable[AbstractTopPbTypeInputPort], _empty_iterable),
        ('outputs', Iterable[AbstractTopPbTypeOutputOrClockPort], _empty_iterable),
        ('clocks', Iterable[AbstractTopPbTypeOutputOrClockPort], _empty_iterable),
        ('modes', Iterable[AbstractMode], _empty_iterable),
        ('completes', Iterable[AbstractInterconnectItem], _empty_iterable),
        ('muxes', Iterable[AbstractInterconnectItem], _empty_iterable),
        ('directs', Iterable[AbstractInterconnectItem], _empty_iterable),
        ('pb_types', Iterable[Union[AbstractLeafPbType, AbstractIntermediatePbType]], _empty_iterable),
        ('fc', Optional[FC], None),
        ('pinlocations', Optional[PinLocations], None),
        ('switchblock_locations', Optional[SwitchblockLocations], None), )),
    AbstractTopPbType):
    pass

class Tile(_namedtuple('Tile',
    attributes = (('type_', str),
        ('block_type_id', int), ),
    defaults = (('xoffset', int, 0),
        ('yoffset', int, 0), )),
    AbstractTile):
    pass

class Timing(_namedtuple('Timing',
    attributes = (('R', float),
        ('C', float), )),
    AbstractTiming):
    pass

# Use conventional `namedtuple` because the default values for `xhigh` and `yhigh` are dependent on other arguments
class NodeLoc(namedtuple('NodeLoc', 'xlow ylow ptc xhigh yhigh side'), AbstractNodeLoc):
    def __new__(cls, xlow, ylow, ptc, xhigh = None, yhigh = None, side = None):
        return super(NodeLoc, cls).__new__(cls, xlow, ylow, ptc,
                xlow if xhigh is None else xhigh,
                ylow if yhigh is None else yhigh,
                side)
    __new__.__annotations__ = {'xlow': int, 'ylow': int, 'ptc': int,
            'xhigh': Optional[int], 'yhigh': Optional[int], 'side': Optional[Side]}

    @property
    def side(self):
        s = super(NodeLoc, self).side
        if s is None:
            raise NotImplementedError
        return s

class Node(_namedtuple('Node',
    attributes = (('id_', int),
        ('type_', NodeType),
        ('locs', AbstractNodeLoc), ),
    defaults = (('direction', Optional[SegmentDirection], None),
        ('segment_id', Optional[int], None),
        ('capacity', Optional[int], None),
        ('timing', Optional[AbstractTiming], None), )),
    AbstractNode):

    @property
    def direction(self):
        d = super(Node, self).direction
        if d is None:
            raise NotImplementedError
        return d

    @property
    def segment_id(self):
        i = super(Node, self).segment_id
        if i is None:
            raise NotImplementedError
        return i

    @property
    def capacity(self):
        c = super(Node, self).capacity
        if c is None:
            raise NotImplementedError
        return c

class Edge(_namedtuple('Edge',
    attributes = (('src_node', int),
        ('sink_node', int),
        ('switch_id', int), )),
    AbstractEdge):
    pass
