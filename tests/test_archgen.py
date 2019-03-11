from vprgen._xml import XMLGenerator
from vprgen._gen_arch import gen_model, gen_segment, gen_switch

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

def test_gen_segment():
    stream = StringIO()
    with XMLGenerator(stream) as xg:
        gen_segment(xg, {
            "name": "L4",
            "length": 4,
            "id": 1,
            "mux": "default",
            })
    back = parse(stream.getvalue(), encoding="ascii")
    assert back == {"segment": {
        "@name": "L4",
        "@length": "4",
        "@type": "unidir",
        "@freq": "0",
        "@Rmetal": "0",
        "@Cmetal": "0",
        "sb": {"@type": "pattern", "#text": "1 1 1 1 1"},
        "cb": {"@type": "pattern", "#text": "1 1 1 1"},
        "mux": {"@name": "default"},
        }}

def test_gen_switch():
    stream = StringIO()
    with XMLGenerator(stream) as xg:
        gen_switch(xg, { "name": "default",
            "id": 0,
            "Tdel": 120e-12, })
    back = parse(stream.getvalue(), encoding="ascii")
    assert back == {"switch": {
        "@type": "mux",
        "@name": "default",
        "@R": "0",
        "@Cin": "0",
        "@Cout": "0",
        "@Tdel": "1.2e-10",
        }}
