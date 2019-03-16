# VPRGEN: Python API for VPR Architecture Description and Routing Resource Graph Generation

## Usage

Users should inherit the `vprgen.{dict, abstract}based.ArchitectureDelegate`
class and implement required methods/properties. The class provides
`gen_arch_xml` and `gen_rrg_xml` which generates the architecture description
XML and routing resource graph XML, respectively.

## Design Choices

[Design Doc](https://docs.google.com/document/d/1Pd_ygB0PvSq_gPEYIm8sJEF-mYY2nk3kLsazLVL21uw/edit#)

### Validation
VPRGEN always produces valid XML file, but does not guarantee valid VPR
inputs. VPRGEN performs limited validation by using [JSON
schema](https://json-schema.org/).

### Layout
VPRGEN only supports fixed layout, i.e. the block physically placed at each
tile in the grid is known for sure. This is reasonable for real physical
devices.

### Segment
VPRGEN only supports uni-directional segments.

### Device
VPRGEN produces a fake `<device>` tag in the generated architecture
description XML, because the information defined under the tag is either not
useful for physical devices or overwritten by the routing resource graph XML.
`<switchblocklist>` tag is not supported for the same reason. All
switchblock patterns will be implemented as edges in the routing resource
graph XML.
