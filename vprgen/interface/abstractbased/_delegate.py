from future.utils import with_metaclass
from future.builtins import object

from vprgen.interface.abstractbased._abstract import *

from abc import ABCMeta, abstractproperty
from typing import Iterable, Union, Optional

_empty_iterable = tuple()

# ----------------------------------------------------------------------------
# -- Architecture Delegate ---------------------------------------------------
# ----------------------------------------------------------------------------
class ArchitectureDelegate(with_metaclass(ABCMeta, object)):
    """Delegate class which is able to answer questions about what are in the architecture."""
    # -- required properties -------------------------------------------------
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
    def name(self):
        """Name of the fixed layout."""
        raise NotImplementedError
    # Python 2 and 3 compatible type checking
    name.fget.__annotations__ = {"return": int}

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
    nodes.fget.__annotations__ = {"return": Iterable[Union[AbstractSourceSinkNode, AbstractIpinOpinNode,
        AbstractChanxChanyNode]]}

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
