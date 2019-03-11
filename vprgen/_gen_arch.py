from future.utils import raise_from

from vprgen._xml import XMLGenerator
from jsonschema import validate
from json import load
import os

_model_schema = load(open(os.path.join(os.path.dirname(__file__), "schema", "model.schema.json")))

def gen_model(xmlgen, model):
    """Generate a <model> tag for the given ``model``.

    Args:
        xmlgen (`XMLGenerator`): the generator to be used
        model (:obj:`dict`): a `dict` satisfying the JSON schema 'schema/model.schema.json'
    """
    # 1. validate argument
    validate(instance = model, schema = _model_schema)
    # 2. generate tag
    with xmlgen.element("model", {"name": model["name"]}):
        input_ports = model.get("input_ports", None)
        if input_ports:
            with xmlgen.element("input_ports"):
                for port in input_ports:
                    attrs = {"name": port["name"]}
                    if port.get("is_clock", False):
                        attrs["is_clock"] = "1"
                    clock = port.get("clock", None)
                    if clock:
                        attrs["clock"] = clock
                    sink = " ".join(port.get("combinational_sink_ports", []))
                    if sink:
                        attrs["combinational_sink_ports"] = sink
                    xmlgen.element_leaf("port", attrs)
        output_ports = model.get("output_ports", None)
        if output_ports:
            with xmlgen.element("output_ports"):
                for port in output_ports:
                    attrs = {"name": port["name"]}
                    if port.get("is_clock", False):
                        attrs["is_clock"] = "1"
                    clock = port.get("clock", None)
                    if clock:
                        attrs["clock"] = clock
                    xmlgen.element_leaf("port", attrs)

def gen_arch_xml(ostream, delegate, pretty = True):
    """Stream generate VPR's architecture description XML.

    Args:
        ostream: a file-like object, like a `file` or a `StringIO`
        delegate (`ArchitectureDelegate`): the delegate which answers questions about what are in the architecture
        pretty (:obj:`bool`): if the output XML file should be nicely broken into multiple lines and indented
    """
    with XMLGenerator(ostream, pretty) as xg:
        with xg.element("architecture"):
            # 1. models
            with xg.element("models"):
                for model in delegate.iter_models():
                    gen_model(xg, model)
