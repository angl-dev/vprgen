from vprgen._xml import XMLGenerator
from vprgen._gen_arch import gen_model

try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

from xmltodict import parse

def test_gen_model():
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
    back = parse(stream.getvalue(), encoding="ascii")
    assert back == {"model": {
        "@name": "single_port_ram",
        "input_ports": {
            "port": [{ "@name": "we", "@clock": "clk" },
                { "@name": "addr", "@clock": "clk", "@combinational_sink_ports": "out" },
                { "@name": "data", "@clock": "clk", "@combinational_sink_ports": "out" },
                { "@name": "clk", "@is_clock": "1" }],
            },
        "output_ports": {
            "port": { "@name": "out", "@clock": "clk" },
            },
        }}
