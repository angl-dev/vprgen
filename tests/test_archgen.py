from vprgen._xml import XMLGenerator
from vprgen._gen_arch import gen_model

try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

def test_gen_model(self):
    stream = StringIO()
    with XMLGenerator(stream) as xg:
        gen_model(xg, {
            "name": "single_port_ram",
            "input_ports": [{"name": "we", "clock": "clk"},
                {"name": "addr", "clock": "clk", "combinational_sink_ports": ["out"]},
                {"name": "data", "clock": "clk", "combinational_sink_ports": ["out"]},
                {"name": "clk", "is_clock": True}],
            "output_ports": [{"name": "out", "clock": "clk"}],
            })
    assert stream.getvalue() == (b'<model name="single_port_ram"><input_ports>'
            b'<port name="we" clock="clk"></port>'
            b'<port name="addr" clock="clk" combinational_sink_ports="out"></port>'
            b'<port name="data" clock="clk" combinational_sink_ports="out"></port>'
            b'<port name="clk" is_clock="1"></port>'
            b'</input_ports><output_ports>'
            b'<port name="out" clock="clk"></port>'
            b'</output_ports></model>')
