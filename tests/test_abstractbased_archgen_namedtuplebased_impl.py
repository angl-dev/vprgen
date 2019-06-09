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
    with XMLGenerator(stream, skip_stringify=True) as xg:
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

def test_gen_segment():
    stream = StringIO()
    delegate = mock
    with XMLGenerator(stream, skip_stringify=True) as xg:
        delegate._gen_arch_segment(xg, Segment('L4', 1, 4, 'default'))
    back = parse(stream.getvalue(), encoding="ascii", dict_constructor=dict)
    gold = parse("""
    <segment name="L4" length="4" type="unidir" freq="0.0" Rmetal="0.0" Cmetal="0.0">
        <sb type="pattern">1 1 1 1 1</sb>
        <cb type="pattern">1 1 1 1</cb>
        <mux name="default"/>
    </segment>
    """, dict_constructor=dict)
    assert back == gold

def test_gen_switch():
    stream = StringIO()
    delegate = mock
    with XMLGenerator(stream, skip_stringify=True) as xg:
        delegate._gen_arch_switch(xg, Switch("default", 1, 120e-12))
    back = parse(stream.getvalue(), encoding="ascii", dict_constructor=dict)
    gold = parse("""
    <switch name="default" type="mux" R="0.0" Cin="0.0" Cout="0.0" Tdel="1.2e-10"/>
    """, dict_constructor=dict)

def test_gen_direct():
    stream = StringIO()
    delegate = mock
    with XMLGenerator(stream, skip_stringify=True) as xg:
        delegate._gen_direct(xg, Direct("adder_chain", "clb.cout", "clb.cin", "default",
            y_offset=1))
    back = parse(stream.getvalue(), encoding="ascii")
    gold = parse("""
    <direct name="adder_chain" from_pin="clb.cout" to_pin="clb.cin" x_offset="0" y_offset="1" z_offset="0" switch_name="default"/>
    """, dict_constructor=dict)

def test_gen_leaf_pb_type():
    stream = StringIO()
    delegate = mock
    with XMLGenerator(stream, skip_stringify=True) as xg:
        delegate._gen_leaf_pb_type(xg, LeafPbType('lut_inst', '.names',
            class_ = LeafPbTypeClass.lut,
            inputs = (LeafPbTypePort('in', 4, LeafPbTypePortClass.lut_in), ),
            outputs = (LeafPbTypePort('out', 1, LeafPbTypePortClass.lut_out), ),
            delay_matrices = (DelayMatrix(DelayMatrixType.min_, 'in', 'out',
                ((120e-12, ), ) * 4), ),
            metadata = {"fasm_type": "LUT", "fasm_lut": "lut_inst"},
            ))
    back = parse(stream.getvalue(), encoding="ascii", dict_constructor=dict)
    gold = parse("""
    <pb_type name="lut_inst" num_pb="1" blif_model=".names" class="lut">
        <input name="in" num_pins="4" port_class="lut_in"/>
        <output name="out" num_pins="1" port_class="lut_out"/>
        <delay_matrix type="min" in_port="in" out_port="out">
            1.2e-10
            1.2e-10
            1.2e-10
            1.2e-10
        </delay_matrix>
        <metadata>
            <meta name="fasm_type">LUT</meta>
            <meta name="fasm_lut">lut_inst</meta>
        </metadata>
    </pb_type>
    """, dict_constructor=dict)

def test_gen_intermediate_pb_type():
    stream = StringIO()
    delegate = mock
    with XMLGenerator(stream, skip_stringify=True) as xg:
        delegate._gen_intermediate_pb_type(xg, IntermediatePbType('extio',
            inputs = (PbTypePort('outpad', 1), ),
            outputs = (PbTypePort('inpad', 1), ),
            modes = (Mode('extio_i',
                pb_types = (LeafPbType('extio_i', '.input',
                    outputs = (LeafPbTypePort('inpad', 1), )), ),
                directs = (InterconnectItem('inpad', ('extio_i.inpad', ), ('extio.inpad', ),
                    delay_constants = (DelayConstant('extio_i.inpad', 'extio.inpad',
                        min_ = 0.0), )), ),
                metadata = {"fasm_features": "extio_i"}, ),
                    Mode('extio_o',
                pb_types = (LeafPbType('extio_o', '.output',
                    inputs = (LeafPbTypePort('outpad', 1), )), ),
                directs = (InterconnectItem('outpad', ('extio.outpad', ), ('extio_o.outpad', ),
                    delay_constants = (DelayConstant('extio.outpad', 'extio_o.outpad',
                        min_ = 0.0), )), ),
                metadata = {"fasm_features": "extio_o"}, ), ),
            metadata = {"fasm_prefix": "extio"}, ))
    back = parse(stream.getvalue(), encoding='ascii', dict_constructor=dict)
    gold = parse("""
	<pb_type name="extio" num_pb="1">
		<output name="inpad" num_pins="1"></output>
		<input name="outpad" num_pins="1"></input>
		<mode name="extio_i">
			<interconnect>
				<direct input="extio_i.inpad" name="inpad" output="extio.inpad">
					<delay_constant in_port="extio_i.inpad" min="0.0" out_port="extio.inpad"></delay_constant>
				</direct>
			</interconnect>
			<pb_type blif_model=".input" name="extio_i" num_pb="1">
				<output name="inpad" num_pins="1"></output>
			</pb_type>
            <metadata>
                <meta name="fasm_features">extio_i</meta>
            </metadata>
		</mode>
		<mode name="extio_o">
			<interconnect>
				<direct input="extio.outpad" name="outpad" output="extio_o.outpad">
					<delay_constant in_port="extio.outpad" min="0.0" out_port="extio_o.outpad"></delay_constant>
				</direct>
			</interconnect>
			<pb_type blif_model=".output" name="extio_o" num_pb="1">
				<input name="outpad" num_pins="1"></input>
			</pb_type>
            <metadata>
                <meta name="fasm_features">extio_o</meta>
            </metadata>
		</mode>
        <metadata>
            <meta name="fasm_prefix">extio</meta>
        </metadata>
	</pb_type>
    """, dict_constructor=dict)
    assert back == gold

def test_gen_top_pb_type():
    stream = StringIO()
    delegate = mock
    with XMLGenerator(stream, skip_stringify=True) as xg:
        delegate._gen_arch_block(xg, TopPbType('CLB', 1,
            inputs = (TopPbTypeInputPort('I', 4), ),
            outputs = (TopPbTypeOutputOrClockPort('O', 1), ),
            clocks = (TopPbTypeOutputOrClockPort('CLK', 1), ),
            fc = FC(FCType.frac, 1.0, FCType.frac, 1.0),
            pinlocations = PinLocations(PinLocationsPattern.custom,
                (PinLocationsLoc(Side.right, ('CLB.O', )),
                    PinLocationsLoc(Side.bottom, ('CLB.CLK', )),
                    PinLocationsLoc(Side.left, ('CLB.I', )), )),
            pb_types = (LeafPbType('LUT', '.names', 
                class_ = LeafPbTypeClass.lut,
                inputs = (LeafPbTypePort('in', 4, port_class=LeafPbTypePortClass.lut_in), ),
                outputs = (LeafPbTypePort('out', 1, port_class=LeafPbTypePortClass.lut_out), ),
                delay_constants = (DelayConstant('LUT.in[0]', 'LUT.out[0]', max_=1.74732e-10),
                    DelayConstant('LUT.in[1]', 'LUT.out[0]', max_=1.14172e-10),
                    DelayConstant('LUT.in[2]', 'LUT.out[0]', max_=2.17193e-10),
                    DelayConstant('LUT.in[3]', 'LUT.out[0]', max_=1.33005e-10), ), ),
                LeafPbType('FF', '.latch',
                    class_ = LeafPbTypeClass.flipflop,
                    inputs = (LeafPbTypePort('D', 1, port_class=LeafPbTypePortClass.D), ),
                    outputs = (LeafPbTypePort('Q', 1, port_class=LeafPbTypePortClass.Q), ),
                    clocks = (LeafPbTypePort('clk', 1, port_class=LeafPbTypePortClass.clock), ),
                    T_setups = (TSetupOrHold('FF.D[0]', 'clk', 2.05278e-10), ),
                    T_clock_to_Qs = (TClockToQ('FF.Q[0]', 'clk', max_=1.10051e-10), ),
                    ), ),
            muxes = (InterconnectItem('itx0', ('LUT.out[0]', 'FF.Q[0]'), ('CLB.O[0]', ),
                delay_constants = (DelayConstant('LUT.out[0]', 'CLB.O[0]', max_=1.25929e-10),
                    DelayConstant('FF.Q[0]', 'CLB.O[0]', max_=2.21582e-10), ), ), ),
            directs = (InterconnectItem('itx2', ('CLB.I[0]', ), ('LUT.in[0]', ),
                delay_constants = (DelayConstant('CLB.I[0]', 'LUT.in[0]', max_=1.01326e-10), ), ),
                InterconnectItem('itx3', ('CLB.I[1]', ), ('LUT.in[1]', ),
                    delay_constants = (DelayConstant('CLB.I[1]', 'LUT.in[1]', max_=1.73948e-10), ), ),
                InterconnectItem('itx4', ('CLB.I[2]', ), ('LUT.in[2]', ),
                    delay_constants = (DelayConstant('CLB.I[2]', 'LUT.in[2]', max_=2.43900e-10), ), ),
                InterconnectItem('itx5', ('CLB.I[3]', ), ('LUT.in[3]', ),
                    delay_constants = (DelayConstant('CLB.I[3]', 'LUT.in[3]', max_=2.17652e-10), ), ),
                InterconnectItem('itx6', ('CLB.CLK[0]', ), ('FF.clk[0]', ),
                    delay_constants = (DelayConstant('CLB.CLK[0]', 'FF.clk[0]', max_=1.7592e-10), ), ),
                InterconnectItem('itx7', ('LUT.out[0]', ), ('FF.D[0]', ),
                    pack_patterns = (PackPattern('pack0', 'LUT.out[0]', 'FF.D[0]'), ),
                    delay_constants = (DelayConstant('LUT.out[0]', 'FF.D[0]', max_=2.34841e-10), ), ), ), ))
    back = parse(stream.getvalue(), encoding="ascii", dict_constructor=dict)
    gold = parse("""
		<pb_type height="1" name="CLB" width="1" capacity="1">
			<input name="I" num_pins="4"></input>
			<output name="O" num_pins="1"></output>
			<clock name="CLK" num_pins="1"></clock>
			<fc in_type="frac" in_val="1.0" out_type="frac" out_val="1.0"></fc>
			<pinlocations pattern="custom">
				<loc side="right" xoffset="0" yoffset="0">CLB.O</loc>
				<loc side="bottom" xoffset="0" yoffset="0">CLB.CLK</loc>
				<loc side="left" xoffset="0" yoffset="0">CLB.I</loc>
			</pinlocations>
			<pb_type blif_model=".names" class="lut" name="LUT" num_pb="1">
				<input name="in" num_pins="4" port_class="lut_in"></input>
				<output name="out" num_pins="1" port_class="lut_out"></output>
				<delay_constant in_port="LUT.in[0]" max="1.74732e-10" out_port="LUT.out[0]"></delay_constant>
				<delay_constant in_port="LUT.in[1]" max="1.14172e-10" out_port="LUT.out[0]"></delay_constant>
				<delay_constant in_port="LUT.in[2]" max="2.17193e-10" out_port="LUT.out[0]"></delay_constant>
				<delay_constant in_port="LUT.in[3]" max="1.33005e-10" out_port="LUT.out[0]"></delay_constant>
			</pb_type>
			<pb_type blif_model=".latch" class="flipflop" name="FF" num_pb="1">
				<clock name="clk" num_pins="1" port_class="clock"></clock>
				<input name="D" num_pins="1" port_class="D"></input>
				<output name="Q" num_pins="1" port_class="Q"></output>
				<T_setup clock="clk" port="FF.D[0]" value="2.05278e-10"></T_setup>
				<T_clock_to_Q clock="clk" max="1.10051e-10" port="FF.Q[0]"></T_clock_to_Q>
			</pb_type>
			<interconnect>
				<mux input="LUT.out[0] FF.Q[0]" name="itx0" output="CLB.O[0]">
					<delay_constant in_port="LUT.out[0]" max="1.25929e-10" out_port="CLB.O[0]"></delay_constant>
					<delay_constant in_port="FF.Q[0]" max="2.21582e-10" out_port="CLB.O[0]"></delay_constant>
				</mux>
				<direct input="CLB.I[0]" name="itx2" output="LUT.in[0]">
					<delay_constant in_port="CLB.I[0]" max="1.01326e-10" out_port="LUT.in[0]"></delay_constant>
				</direct>
				<direct input="CLB.I[1]" name="itx3" output="LUT.in[1]">
					<delay_constant in_port="CLB.I[1]" max="1.73948e-10" out_port="LUT.in[1]"></delay_constant>
				</direct>
				<direct input="CLB.I[2]" name="itx4" output="LUT.in[2]">
					<delay_constant in_port="CLB.I[2]" max="2.439e-10" out_port="LUT.in[2]"></delay_constant>
				</direct>
				<direct input="CLB.I[3]" name="itx5" output="LUT.in[3]">
					<delay_constant in_port="CLB.I[3]" max="2.17652e-10" out_port="LUT.in[3]"></delay_constant>
				</direct>
				<direct input="CLB.CLK[0]" name="itx6" output="FF.clk[0]">
					<delay_constant in_port="CLB.CLK[0]" max="1.7592e-10" out_port="FF.clk[0]"></delay_constant>
				</direct>
				<direct input="LUT.out[0]" name="itx7" output="FF.D[0]">
					<delay_constant in_port="LUT.out[0]" max="2.34841e-10" out_port="FF.D[0]"></delay_constant>
					<pack_pattern in_port="LUT.out[0]" name="pack0" out_port="FF.D[0]"></pack_pattern>
				</direct>
            </interconnect>
        </pb_type>
    """, dict_constructor = dict)
    assert back == gold
