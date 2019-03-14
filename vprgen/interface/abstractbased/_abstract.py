from future.utils import with_metaclass
from future.builtins import object

from typing import Optional, Iterable, Union
from abc import ABCMeta, abstractproperty, abstractmethod
from enum import Enum

_empty_iterable = tuple()

# ----------------------------------------------------------------------------
# -- Model-related Abstracts -------------------------------------------------
# ----------------------------------------------------------------------------
class AbstractModelOutputPort(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": str}

    # -- optional properties -------------------------------------------------
    @property
    def is_clock(self):
        return False
    # Python 2 and 3 compatible type checking
    is_clock.fget.__annotations__ = {"return": bool}

    @property
    def clock(self):
        return None
    # Python 2 and 3 compatible type checking
    clock.fget.__annotations__ = {"return": Optional[str]}

class AbstractModelInputPort(AbstractModelOutputPort):
    # -- optional properties -------------------------------------------------
    @property
    def combinational_sink_ports(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    combinational_sink_ports.fget.__annotations__ = {"return": Iterable[str]}

class AbstractModel(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": str}

    # -- optional properties -------------------------------------------------
    @property
    def input_ports(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    input_ports.fget.__annotations__ = {"return": Iterable[AbstractModelInputPort]}

    @property
    def output_ports(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    output_ports.fget.__annotations__ = {"return": Iterable[AbstractModelOutputPort]}

# ----------------------------------------------------------------------------
# -- Segment-related Abstracts -----------------------------------------------
# ----------------------------------------------------------------------------
class AbstractSegment(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": str}

    @abstractproperty
    def id_(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    id_.fget.__annotations__ = {"return": int}

    @abstractproperty
    def length(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    length.fget.__annotations__ = {"return": int}

    @abstractproperty
    def mux(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    mux.fget.__annotations__ = {"return": str}

    # -- optional properties -------------------------------------------------
    @property
    def freq(self):
        return 0.0
    # Python 2 and 3 compatible type checking
    freq.fget.__annotations__ = {"return": float}

    @property
    def Rmetal(self):
        return 0.0
    # Python 2 and 3 compatible type checking
    Rmetal.fget.__annotations__ = {"return": float}

    @property
    def Cmetal(self):
        return 0.0
    # Python 2 and 3 compatible type checking
    Cmetal.fget.__annotations__ = {"return": float}

    @property
    def sb(self):
        return None
    # Python 2 and 3 compatible type checking
    sb.fget.__annotations__ = {"return": Optional[Iterable[bool]]}

    @property
    def cb(self):
        return None
    # Python 2 and 3 compatible type checking
    cb.fget.__annotations__ = {"return": Optional[Iterable[bool]]}

# ----------------------------------------------------------------------------
# -- Switch-related Abstracts ------------------------------------------------
# ----------------------------------------------------------------------------
class AbstractSwitchTdel(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def num_inputs(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    num_inputs.fget.__annotations__ = {"return": int}

    @abstractproperty
    def delay(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    num_inputs.fget.__annotations__ = {"return": float}

class SwitchType(Enum):
    mux = 0
    tristate = 1
    pass_gate = 2
    short = 3
    buffer_ = 4

class AbstractSwitch(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": str}

    @abstractproperty
    def id_(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    id_.fget.__annotations__ = {"return": int}

    @abstractproperty
    def Tdel(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    Tdel.fget.__annotations__ = {"return": Union[float, Iterable[AbstractSwitchTdel]]}

    # -- optional properties -------------------------------------------------
    @property
    def type_(self):
        return SwitchType.mux
    # Python 2 and 3 compatible type checking
    type_.fget.__annotations__ = {"return": SwitchType}

    @property
    def R(self):
        return 0.0
    # Python 2 and 3 compatible type checking
    R.fget.__annotations__ = {"return": float}

    @property
    def Cin(self):
        return 0.0
    # Python 2 and 3 compatible type checking
    Cin.fget.__annotations__ = {"return": float}

    @property
    def Cout(self):
        return 0.0
    # Python 2 and 3 compatible type checking
    Cout.fget.__annotations__ = {"return": float}

# ----------------------------------------------------------------------------
# -- Direct-related Abstracts ------------------------------------------------
# ----------------------------------------------------------------------------
class AbstractDirect(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": str}

    @abstractproperty
    def from_pin(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    from_pin.fget.__annotations__ = {"return": str}

    @abstractproperty
    def to_pin(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    to_pin.fget.__annotations__ = {"return": str}

    @abstractproperty
    def switch_name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    switch_name.fget.__annotations__ = {"return": str}

    # -- optional properties -------------------------------------------------
    @property
    def x_offset(self):
        return 0
    # Python 2 and 3 compatible type checking
    x_offset.fget.__annotations__ = {"return": int}

    @property
    def y_offset(self):
        return 0
    # Python 2 and 3 compatible type checking
    y_offset.fget.__annotations__ = {"return": int}

    @property
    def z_offset(self):
        return 0
    # Python 2 and 3 compatible type checking
    z_offset.fget.__annotations__ = {"return": int}

# ----------------------------------------------------------------------------
# -- Pb_type-related Abstracts -----------------------------------------------
# ----------------------------------------------------------------------------
class AbstractDelayConstant(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def in_port(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    in_port.fget.__annotations__ = {"return": str}

    @abstractproperty
    def out_port(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    out_port.fget.__annotations__ = {"return": str}

    # -- optional properties -------------------------------------------------
    @property
    def min_(self):
        return None
    # Python 2 and 3 compatible type checking
    min_.fget.__annotations__ = {"return": Optional[float]}

    @property
    def max_(self):
        return None
    # Python 2 and 3 compatible type checking
    max_.fget.__annotations__ = {"return": Optional[float]}

class DelayMatrixType(Enum):
    min_ = 0
    max_ = 1

class AbstractDelayMatrix(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def type_(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    type_.fget.__annotations__ = {"return": DelayMatrixType}

    @abstractproperty
    def in_port(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    in_port.fget.__annotations__ = {"return": str}

    @abstractproperty
    def out_port(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    out_port.fget.__annotations__ = {"return": str}

    @abstractproperty
    def values(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    values.fget.__annotations__ = {"return": Iterable[Iterable[float]]}

class AbstractTSetupOrTHold(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def port(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    port.fget.__annotations__ = {"return": str}

    @abstractproperty
    def clock(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    clock.fget.__annotations__ = {"return": str}

    @abstractproperty
    def value(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    value.fget.__annotations__ = {"return": float}

class AbstractTClockToQ(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def port(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    port.fget.__annotations__ = {"return": str}

    @abstractproperty
    def clock(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    clock.fget.__annotations__ = {"return": str}

    # -- optional properties -------------------------------------------------
    @property
    def min_(self):
        return None
    # Python 2 and 3 compatible type checking
    min_.fget.__annotations__ = {"return": Optional[float]}

    @property
    def max_(self):
        return None
    # Python 2 and 3 compatible type checking
    max_.fget.__annotations__ = {"return": Optional[float]}

class LeafPbTypePortClass(Enum):
    lut_in = 0
    lut_out = 1
    clock = 2
    D = 3
    Q = 4
    address = 5
    write_en = 6
    data_in = 7
    data_out = 8
    address1 = 9
    write_en1 = 10
    data_in1 = 11
    data_out1 = 12
    address2 = 13
    write_en2 = 14
    data_in2 = 15
    data_out2 = 16

class AbstractPbTypePort(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": str}

    @abstractproperty
    def num_pins(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    num_pins.fget.__annotations__ = {"return": int}

class AbstractLeafPbTypePort(AbstractPbTypePort):
    # -- optional properties -------------------------------------------------
    @property
    def port_class(self):
        return None
    # Python 2 and 3 compatible type checking
    port_class.fget.__annotations__ = {"return": Optional[LeafPbTypePortClass]}

class LeafPbTypeClass(Enum):
    lut = 0
    flipflop = 1
    memory = 2

class _AbstractNonTopPbType(with_metaclass(ABCMeta, object)):
    """Forward declaration of abstract base classes for leaf pb_type and intermediate pb_type."""
    # -- required properties -------------------------------------------------
    @abstractproperty
    def name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": str}

    # -- optional properties -------------------------------------------------
    @property
    def num_pb(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    num_pb.fget.__annotations__ = {"return": int}

class AbstractLeafPbType(_AbstractNonTopPbType):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def blif_model(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    blif_model.fget.__annotations__ = {"return": str}

    # -- optional properties -------------------------------------------------
    @property
    def class_(self):
        return None
    # Python 2 and 3 compatible type checking
    class_.fget.__annotations__ = {"return": Optional[LeafPbTypeClass]}

    @property
    def input_(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    input_.fget.__annotations__ = {"return": Iterable[AbstractLeafPbTypePort]}

    @property
    def output(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    output.fget.__annotations__ = {"return": Iterable[AbstractLeafPbTypePort]}

    @property
    def clock(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    clock.fget.__annotations__ = {"return": Iterable[AbstractLeafPbTypePort]}

    @property
    def delay_constant(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    delay_constant.fget.__annotations__ = {"return": Iterable[AbstractDelayConstant]}

    @property
    def delay_matrix(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    delay_matrix.fget.__annotations__ = {"return": Iterable[AbstractDelayMatrix]}

    @property
    def T_setup(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    T_setup.fget.__annotations__ = {"return": Iterable[AbstractTSetupOrTHold]}

    @property
    def T_hold(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    T_hold.fget.__annotations__ = {"return": Iterable[AbstractTSetupOrTHold]}

    @property
    def T_clock_to_Q(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    T_clock_to_Q.fget.__annotations__ = {"return": Iterable[AbstractTClockToQ]}

class AbstractPackPattern(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": str}

    @abstractproperty
    def in_port(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    in_port.fget.__annotations__ = {"return": str}

    @abstractproperty
    def out_port(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    out_port.fget.__annotations__ = {"return": str}

class AbstractInterconnectItem(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": str}

    @abstractproperty
    def input_(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    input_.fget.__annotations__ = {"return": str}

    @abstractproperty
    def output(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    output.fget.__annotations__ = {"return": str}

    # -- optional properties -------------------------------------------------
    @property
    def pack_pattern(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    pack_pattern.fget.__annotations__ = {"return": Iterable[AbstractPackPattern]}

    @property
    def delay_constant(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    delay_constant.fget.__annotations__ = {"return": Iterable[AbstractDelayConstant]}

    @property
    def delay_matrix(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    delay_matrix.fget.__annotations__ = {"return": Iterable[AbstractDelayMatrix]}

class AbstractMode(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": str}

    # -- optional properties -------------------------------------------------
    @property
    def complete(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    complete.fget.__annotations__ = {"return": Iterable[AbstractInterconnectItem]}

    @property
    def mux(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    mux.fget.__annotations__ = {"return": Iterable[AbstractInterconnectItem]}

    @property
    def direct(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    direct.fget.__annotations__ = {"return": Iterable[AbstractInterconnectItem]}

    @property
    def pb_type(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    pb_type.fget.__annotations__ = {"return": Iterable[_AbstractNonTopPbType]}

class AbstractIntermediatePbType(_AbstractNonTopPbType):
    # -- optional properties -------------------------------------------------
    @property
    def input_(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    input_.fget.__annotations__ = {"return": Iterable[AbstractPbTypePort]}

    @property
    def output(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    output.fget.__annotations__ = {"return": Iterable[AbstractPbTypePort]}

    @property
    def clock(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    clock.fget.__annotations__ = {"return": Iterable[AbstractPbTypePort]}

    @property
    def complete(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    complete.fget.__annotations__ = {"return": Iterable[AbstractInterconnectItem]}

    @property
    def mux(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    mux.fget.__annotations__ = {"return": Iterable[AbstractInterconnectItem]}

    @property
    def direct(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    direct.fget.__annotations__ = {"return": Iterable[AbstractInterconnectItem]}

    @property
    def pb_type(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    pb_type.fget.__annotations__ = {"return": Iterable[_AbstractNonTopPbType]}

    @property
    def mode(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    mode.fget.__annotations__ = {"return": Iterable[AbstractMode]}

class TopPbTypePortEquivalent(Enum):
    full = 0
    instance = 1

class AbstractTopPbTypeOutputOrClockPort(AbstractPbTypePort):
    # -- optional properties -------------------------------------------------
    @property
    def equivalent(self):
        return None
    # Python 2 and 3 compatible type checking
    equivalent.fget.__annotations__ = {"return": Optional[TopPbTypePortEquivalent]}

class AbstractTopPbTypeInputPort(AbstractTopPbTypeOutputOrClockPort):
    # -- optional properties -------------------------------------------------
    @property
    def is_non_clock_global(self):
        return False
    # Python 2 and 3 compatible type checking
    is_non_clock_global.fget.__annotations__ = {"return": bool}

class FCType(Enum):
    abs_ = 0
    frac = 1

class AbstractFCOverride(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def fc_type(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    fc_type.fget.__annotations__ = {"return": FCType}

    @abstractproperty
    def port_name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    port_name.fget.__annotations__ = {"return": str}

    @abstractproperty
    def segment_name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    segment_name.fget.__annotations__ = {"return": str}

    @abstractproperty
    def fc_val(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    fc_val.fget.__annotations__ = {"return": Union[float, int]}

class AbstractFC(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @property
    def in_type(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    in_type.fget.__annotations__ = {"return": FCType}

    @abstractproperty
    def in_val(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    in_val.fget.__annotations__ = {"return": Union[float, int]}

    @property
    def out_type(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    out_type.fget.__annotations__ = {"return": FCType}

    @abstractproperty
    def out_val(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    out_val.fget.__annotations__ = {"return": Union[float, int]}

    # -- optional properties -------------------------------------------------
    @property
    def fc_override(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    fc_override.fget.__annotations__ = {"return": Iterable[AbstractFCOverride]}

class Side(Enum):
    left = 0
    right = 1
    bottom = 2
    top = 3

class AbstractPinLocationsLoc(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def side(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    side.fget.__annotations__ = {"return": Side}

    @abstractproperty
    def ports(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    ports.fget.__annotations__ = {"return": Iterable[str]}

    # -- optional properties -------------------------------------------------
    @property
    def xoffset(self):
        return 0
    # Python 2 and 3 compatible type checking
    xoffset.fget.__annotations__ = {"return": int}

    @property
    def yoffset(self):
        return 0
    # Python 2 and 3 compatible type checking
    yoffset.fget.__annotations__ = {"return": int}

class PinLocationsPattern(Enum):
    spread = 0
    perimeter = 1
    spread_inputs_perimeter_outputs = 2
    custom = 3

class AbstractPinLocations(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def pattern(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    pattern.fget.__annotations__ = {"return": PinLocationsPattern}

    # -- optional properties -------------------------------------------------
    @property
    def loc(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    loc.fget.__annotations__ = {"return": Iterable[AbstractPinLocationsLoc]}

class SbLocType(Enum):
    full = 0
    straight = 1
    turns = 2
    none = 3

class AbstractSbLoc(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def type_(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    type_.fget.__annotations__ = {"return": SbLocType}

    # -- optional properties -------------------------------------------------
    @property
    def xoffset(self):
        return 0
    # Python 2 and 3 compatible type checking
    xoffset.fget.__annotations__ = {"return": int}

    @property
    def yoffset(self):
        return 0
    # Python 2 and 3 compatible type checking
    yoffset.fget.__annotations__ = {"return": int}

    @property
    def switch_override(self):
        return None
    # Python 2 and 3 compatible type checking
    switch_override.fget.__annotations__ = {"return": Optional[str]}

class SwitchblockLocationsPattern(Enum):
    external_full_internal_straight = 0
    all_ = 1
    external = 2
    internal = 3
    none = 4
    custom = 5

class AbstractSwitchblockLocations(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def pattern(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    pattern.fget.__annotations__ = {"return": SwitchblockLocationsPattern}

    # -- optional properties -------------------------------------------------
    @property
    def sb_loc(self):
        return None
    # Python 2 and 3 compatible type checking
    sb_loc.fget.__annotations__ = {"return": Optional[Iterable[AbstractSbLoc]]}

class AbstractTopPbType(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def name(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": str}

    @abstractproperty
    def id_(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    id_.fget.__annotations__ = {"return": int}

    # -- optional properties -------------------------------------------------
    @property
    def capacity(self):
        return 1 
    # Python 2 and 3 compatible type checking
    capacity.fget.__annotations__ = {"return": int}

    @property
    def width(self):
        return 1 
    # Python 2 and 3 compatible type checking
    width.fget.__annotations__ = {"return": int}

    @property
    def height(self):
        return 1 
    # Python 2 and 3 compatible type checking
    height.fget.__annotations__ = {"return": int}

    @property
    def input_(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    input_.fget.__annotations__ = {"return": Iterable[AbstractTopPbTypeInputPort]}

    @property
    def output(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    output.fget.__annotations__ = {"return": Iterable[AbstractTopPbTypeOutputOrClockPort]}

    @property
    def clock(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    clock.fget.__annotations__ = {"return": Iterable[AbstractTopPbTypeOutputOrClockPort]}

    @property
    def complete(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    complete.fget.__annotations__ = {"return": Iterable[AbstractInterconnectItem]}

    @property
    def mux(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    mux.fget.__annotations__ = {"return": Iterable[AbstractInterconnectItem]}

    @property
    def direct(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    direct.fget.__annotations__ = {"return": Iterable[AbstractInterconnectItem]}

    @property
    def pb_type(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    pb_type.fget.__annotations__ = {"return": Iterable[_AbstractNonTopPbType]}

    @property
    def mode(self):
        return _empty_iterable
    # Python 2 and 3 compatible type checking
    mode.fget.__annotations__ = {"return": Iterable[AbstractMode]}

    @property
    def fc(self):
        return None
    # Python 2 and 3 compatible type checking
    fc.fget.__annotations__ = {"return": Optional[AbstractFC]}

    @property
    def pinlocations(self):
        return None
    # Python 2 and 3 compatible type checking
    pinlocations.fget.__annotations__ = {"return": Optional[AbstractPinLocations]}

    @property
    def switchblock_locations(self):
        return None
    # Python 2 and 3 compatible type checking
    switchblock_locations.fget.__annotations__ = {"return": Optional[AbstractSwitchblockLocations]}

# ----------------------------------------------------------------------------
# -- Tile-related Abstracts --------------------------------------------------
# ----------------------------------------------------------------------------
class AbstractTile(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def type_(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    type_.fget.__annotations__ = {"return": str}

    @abstractproperty
    def block_type_id(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    block_type_id.fget.__annotations__ = {"return": int}

    # -- optional properties -------------------------------------------------
    @property
    def xoffset(self):
        return 0
    # Python 2 and 3 compatible type checking
    xoffset.fget.__annotations__ = {"return": int}

    @property
    def yoffset(self):
        return 0
    # Python 2 and 3 compatible type checking
    yoffset.fget.__annotations__ = {"return": int}

# ----------------------------------------------------------------------------
# -- Node-related Abstracts --------------------------------------------------
# ----------------------------------------------------------------------------
class AbstractTiming(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def R(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    R.fget.__annotations__ = {"return": float}

    @abstractproperty
    def C(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    C.fget.__annotations__ = {"return": float}

class AbstractNodeLoc(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def xlow(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    xlow.fget.__annotations__ = {"return": int}

    @abstractproperty
    def ylow(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    ylow.fget.__annotations__ = {"return": int}

    @abstractproperty
    def ptc(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    ptc.fget.__annotations__ = {"return": int}

    # -- optional properties -------------------------------------------------
    @property
    def xhigh(self):
        return self.xlow
    # Python 2 and 3 compatible type checking
    xhigh.fget.__annotations__ = {"return": int}

    @property
    def yhigh(self):
        return self.ylow
    # Python 2 and 3 compatible type checking
    yhigh.fget.__annotations__ = {"return": int}

class _AbstractNode(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def id_(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    id_.fget.__annotations__ = {"return": int}

    # -- optional properties -------------------------------------------------
    @property
    def capacity(self):
        return 1 
    # Python 2 and 3 compatible type checking
    capacity.fget.__annotations__ = {"return": int}

    @property
    def timing(self):
        return None
    # Python 2 and 3 compatible type checking
    timing.fget.__annotations__ = {"return": Optional[AbstractTiming]}

class SourceSinkNodeType(Enum):
    SOURCE = 0
    SINK = 1

class AbstractSourceSinkNode(_AbstractNode):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def type_(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    type_.fget.__annotations__ = {"return": SourceSinkNodeType}

    @abstractproperty
    def loc(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    loc.fget.__annotations__ = {"return": AbstractNodeLoc}

class IpinOpinNodeType(Enum):
    IPIN = 0
    OPIN = 1

class AbstractIpinOpinNodeLoc(AbstractNodeLoc):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def side(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    side.fget.__annotations__ = {"return": Side}

class AbstractIpinOpinNode(_AbstractNode):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def type_(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    type_.fget.__annotations__ = {"return": SourceSinkNodeType}

    @abstractproperty
    def loc(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    loc.fget.__annotations__ = {"return": AbstractIpinOpinNodeLoc}

class ChanxChanyNodeType(Enum):
    CHANX = 0
    CHANY = 1

class SegmentDirection(Enum):
    INC_DIR = 0
    DEC_DIR = 1

class AbstractChanxChanyNode(_AbstractNode):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def type_(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    type_.fget.__annotations__ = {"return": ChanxChanyNodeType}

    @abstractproperty
    def direction(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    direction.fget.__annotations__ = {"return": SegmentDirection}

    @abstractproperty
    def loc(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    loc.fget.__annotations__ = {"return": AbstractNodeLoc}

    @abstractproperty
    def segment_id(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    segment_id.fget.__annotations__ = {"return": int}

# ----------------------------------------------------------------------------
# -- Edge-related Abstracts --------------------------------------------------
# ----------------------------------------------------------------------------
class AbstractEdge(with_metaclass(ABCMeta, object)):
    # -- required properties -------------------------------------------------
    @abstractproperty
    def src_node(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    src_node.fget.__annotations__ = {"return": int}

    @abstractproperty
    def sink_node(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    sink_node.fget.__annotations__ = {"return": int}

    @abstractproperty
    def switch_id(self):
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    switch_id.fget.__annotations__ = {"return": int}
