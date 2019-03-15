from future.utils import iteritems

from typing import Iterable, Tuple, Any, Optional
from vprgen.abstractbased._abstract import *
from collections import namedtuple, OrderedDict

def _namedtuple(class_name, attributes = tuple(), defaults = tuple()):
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
        ("combinational_sink_ports", Iterable[str], tuple()), )),
    AbstractModelInputPort):
    pass

class Model(_namedtuple('Model',
    attributes = (('name', str), ),
    defaults = (("input_ports", Iterable[AbstractModelInputPort], tuple()),
        ("output_ports", Iterable[AbstractModelOutputPort], tuple()), )),
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
