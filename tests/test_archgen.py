from vprgen._xml import XMLGenerator
from vprgen._gen_arch import (gen_model, gen_segment, gen_switch, gen_direct, gen_leaf_pb_type, gen_block)

try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

from xmltodict import parse
from json import dumps

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

def test_gen_direct():
    stream = StringIO()
    with XMLGenerator(stream) as xg:
        gen_direct(xg, { "name": "adder_chain",
            "from_pin": "clb.cout",
            "to_pin": "clb.cin",
            "y_offset": 1,
            "switch_name": "default", })
    back = parse(stream.getvalue(), encoding="ascii")
    assert back == {"direct": {
        "@name": "adder_chain",
        "@from_pin": "clb.cout",
        "@to_pin": "clb.cin",
        "@x_offset": "0",
        "@y_offset": "1",
        "@z_offset": "0",
        "@switch_name": "default",
        }}

def test_gen_leaf_pb_type():
    stream = StringIO()
    with XMLGenerator(stream) as xg:
        gen_leaf_pb_type(xg, {
            "name": "lut_inst",
            "blif_model": ".names",
            "class": "lut",
            "input": [{ "name": "in",
                    "num_pins": 4,
                    "port_class": "lut_in",
                }],
            "output": [{ "name": "out",
                    "num_pins": 1,
                    "port_class": "lut_out",
                }],
            "delay_matrix": [{ "type": "min",
                "in_port": "in",
                "out_port": "out",
                "values": [[120e-12], [120e-12], [120e-12], [120e-12]],
                }],
            })
    back = parse(stream.getvalue(), encoding="ascii")
    assert back == {"pb_type": {
        "@name": "lut_inst",
        "@blif_model": ".names",
        "@num_pb": "1",
        "@class": "lut",
        "input": { "@name": "in",
            "@num_pins": "4",
            "@port_class": "lut_in", },
        "output": { "@name": "out",
            "@num_pins": "1",
            "@port_class": "lut_out", },
        "delay_matrix": { "@type": "min",
            "@in_port": "in",
            "@out_port": "out",
            "#text": "1.2e-10\n1.2e-10\n1.2e-10\n1.2e-10", },
        }}

def test_gen_block():

    stream = StringIO()
    with XMLGenerator(stream) as xg:
        gen_block(xg, {
            "name": "IO_TOP",
            "capacity": 2,
            "input": [{
                "name": "GPO",
                "num_pins": 1,
                }],
            "output": [{
                "name": "GPI",
                "num_pins": 1,
                }],
            "fc": {
                "in_type": "frac",
                "in_val": 1,
                "out_type": "frac",
                "out_val": 1,
                },
            "pinlocations": {
                "pattern": "custom",
                "loc": [{
                    "side": "bottom",
                    "ports": ["IO_TOP.GPO", "IO_TOP.GPI"],
                    }],
                },
            "pb_type": [{
                "name": "extio",
                "input": [{
                    "name": "outpad",
                    "num_pins": 1,
                    }],
                "output": [{
                    "name": "inpad",
                    "num_pins": 1,
                    }],
                "mode": [{
                    "name": "extio_i",
                    "pb_type": [{
                        "name": "extio_i",
                        "blif_model": ".input",
                        "output": [{
                            "name": "inpad",
                            "num_pins": 1,
                            }],
                        }],
                    "interconnect": {
                        "direct": [{
                            "input": "extio_i.inpad",
                            "name": "inpad",
                            "output": "extio.inpad",
                            "delay_constant": [{
                                "in_port": "extio_i.inpad",
                                "out_port": "extio.inpad",
                                "min": 0,
                                }],
                            }],
                        },
                    }, {
                        "name": "extio_o",
                        "pb_type": [{
                            "name": "extio_o",
                            "blif_model": ".output",
                            "input": [{
                                "name": "outpad",
                                "num_pins": 1,
                                }],
                            }],
                        "interconnect": {
                            "direct": [{
                                "output": "extio_o.outpad",
                                "name": "outpad",
                                "input": "extio.outpad",
                                "delay_constant": [{
                                    "out_port": "extio_o.outpad",
                                    "in_port": "extio.outpad",
                                    "min": 0,
                                    }],
                                }],
                            },
                        }],
                    }],
            "interconnect": {
                    "direct": [{
                        "input": "extio.inpad[0]",
                        "output": "IO_TOP.GPI[0]",
                        "name": "itx0",
                        "delay_constant": [{
                            "in_port": "extio.inpad[0]",
                            "out_port": "IO_TOP.GPI[0]",
                            "min": 0,
                            "max": 138.583e-12,
                            }],
                        }, {
                            "input": "IO_TOP.GPO[0]",
                            "name": "itx1",
                            "output": "extio.outpad[0]",
                            "delay_constant": [{
                                "in_port": "IO_TOP.GPO[0]",
                                "out_port": "extio.outpad[0]",
                                "min": 0,
                                "max": 200.269e-12,
                                }],
                            }],
                        },
            })
    back = parse(stream.getvalue(), encoding="ascii", dict_constructor=dict)
    gold =  parse("""
	<pb_type capacity="2" name="IO_TOP" width="1" height="1">
		<input name="GPO" num_pins="1"></input>
		<output name="GPI" num_pins="1"></output>
		<fc in_type="frac" in_val="1" out_type="frac" out_val="1"></fc>
		<pinlocations pattern="custom">
			<loc side="bottom" xoffset="0" yoffset="0">IO_TOP.GPO IO_TOP.GPI</loc>
		</pinlocations>
		<pb_type name="extio" num_pb="1">
			<output name="inpad" num_pins="1"></output>
			<input name="outpad" num_pins="1"></input>
			<mode name="extio_i">
				<interconnect>
					<direct input="extio_i.inpad" name="inpad" output="extio.inpad">
						<delay_constant in_port="extio_i.inpad" min="0" out_port="extio.inpad"></delay_constant>
					</direct>
				</interconnect>
				<pb_type blif_model=".input" name="extio_i" num_pb="1">
					<output name="inpad" num_pins="1"></output>
				</pb_type>
			</mode>
			<mode name="extio_o">
				<interconnect>
					<direct input="extio.outpad" name="outpad" output="extio_o.outpad">
						<delay_constant in_port="extio.outpad" min="0" out_port="extio_o.outpad"></delay_constant>
					</direct>
				</interconnect>
				<pb_type blif_model=".output" name="extio_o" num_pb="1">
					<input name="outpad" num_pins="1"></input>
				</pb_type>
			</mode>
		</pb_type>
		<interconnect>
			<direct input="extio.inpad[0]" name="itx0" output="IO_TOP.GPI[0]">
				<delay_constant in_port="extio.inpad[0]" max="1.38583e-10" min="0" out_port="IO_TOP.GPI[0]"></delay_constant>
			</direct>
			<direct input="IO_TOP.GPO[0]" name="itx1" output="extio.outpad[0]">
				<delay_constant in_port="IO_TOP.GPO[0]" max="2.00269e-10" min="0" out_port="extio.outpad[0]"></delay_constant>
			</direct>
		</interconnect>
	</pb_type>
    """, dict_constructor=dict)
    # print("back:")
    # print(dumps(back, indent = 2))
    # print("gold:")
    # print(dumps(gold, indent = 2))
    assert back == gold
