from future.utils import with_metaclass
from future.builtins import object

from typing import Optional, Sequence
from abc import ABCMeta, abstractproperty, abstractmethod

_empty_sequence = tuple()

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
        return _empty_sequence
    # Python 2 and 3 compatible type checking
    combinational_sink_ports.fget.__annotations__ = {"return": Sequence[str]}

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
        return _empty_sequence
    # Python 2 and 3 compatible type checking
    input_ports.fget.__annotations__ = {"return": Sequence[AbstractModelInputPort]}

    @property
    def output_ports(self):
        return _empty_sequence
    # Python 2 and 3 compatible type checking
    output_ports.fget.__annotations__ = {"return": Sequence[AbstractModelOutputPort]}

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
    sb.fget.__annotations__ = {"return": Optional[Sequence[bool]]}

    @property
    def cb(self):
        return None
    # Python 2 and 3 compatible type checking
    cb.fget.__annotations__ = {"return": Optional[Sequence[bool]]}
