from vprgen._xml import XMLGenerator
from vprgen.abstractbased import ArchitectureDelegate
from vprgen.abstractbased.impl.namedtuplebased import *

try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

from xmltodict import parse
from collections import namedtuple
from json import dumps

class MockArchitecture(namedtuple('MockArchitecture', 'name width height x_channel_width y_channel_width'),
        ArchitectureDelegate):
    pass

mock = MockArchitecture('mock', 4, 4, 16, 16)

def test_gen_model():
    stream = StringIO()
    delegate = mock
    with XMLGenerator(stream) as xg:
        delegate._gen_model(xg, Model('single_port_ram',
            (ModelInputPort("we", clock="clk"),
                ModelInputPort("addr", clock="clk", combinational_sink_ports=["out"]),
                ModelInputPort("data", clock="clk", combinational_sink_ports=["out"]),
                ModelInputPort("clk", is_clock=True)),
            (ModelOutputPort("out", clock="clk"), )))
    back = parse(stream.getvalue(), encoding="ascii", dict_constructor=dict)
    gold = parse("""
    <model name="single_port_ram">
        <input_ports>
            <port name="we" clock="clk"/>
            <port name="addr" clock="clk" combinational_sink_ports="out"/>
            <port name="data" clock="clk" combinational_sink_ports="out"/>
            <port name="clk" is_clock="1"/>
        </input_ports>
        <output_ports>
            <port name="out" clock="clk"/>
        </output_ports>
    </model>
    """, dict_constructor=dict)
    assert back == gold
