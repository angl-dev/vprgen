class ArchitectureDelegate(object):
    """Delegate class which is able to answer questions about what are in the architecture."""

    def iter_models(self):
        """Iterate or generate data for the <model> tags under the <models> tag in VPR's architecture description XML.

        Each element in the returned iterator/generator should be a `dict` satisfying the JSON schema
        'schema/model.schema.json'.
        """
        return
        yield None  # mark this method as a generator

    def iter_blocks(self):
        """Iterate or generate blocks for the <pb_type> tags under the <complexblocklist> tag in VPR's architecture
        description XML and the <block_type> tags under the <block_types> tag in VPR's routing resource graph XML.

        Each element in the returned iterator/generator should be a `dict` satisfying the JSON schema
        'schema/block.schema.json'. The order of the ports will be used to determine the `pin_id` of each port.
        """
        return
        yield None  # mark this method as a generator

    def get_width(self):
        """Width of the FPGA grid."""
        raise NotImplementedError

    def get_height(self):
        """Height of the FPGA grid."""
        raise NotImplementedError

    def get_layout_name(self):
        """Name of the layout."""
        return "default"

    def get_tile(self, x, y):
        """Get the physical block at tile (x, y).

        The returned value should be None or a `dict` satisfying the JSON schema 'schema/tile.schema.json'. If None is
        returned, the tile is treated as "EMPTY".
        """
        return None

    def get_device(self):
        """Get the device information.

        The returned value should be a `dict` satisfying the JSON schema 'schema/device.schema.json'. If None is
        returned, a fake <device> tag will be generated and used.
        """
        return None

    def iter_segments(self):
        """Iterate or generate segments for the <segment> tags under the <segmentlist> tag in VPR's architecture
        description XML and the <segment> tag under the <segments> tag in VPR's routing resource graph XML.

        Each element in the returned iterator/generator should be a `dict` satisfying the JSON schema
        'schema/segment.schema.json'.
        """
        return
        yield None  # mark this method as a generator

    def iter_switches(self):
        """Iterate or generate switches for the <switch> tags under the <switchlist> tag in VPR's architecture
        description XML and the <switches> tag under the <switches> tag in VPR's routing resource graph XML.

        Each element in the returned iterator/generator should be a `dict` satisfying the JSON schema
        'schema/switch.schema.json'.
        """
        return
        yield None  # mark this method as a generator

    def iter_directs(self):
        """Iterate or generate directs for the <direct> tags under the <directlist> tag in VPR's architecture
        description XML.

        Each element in the returned iterator/generator should be a `dict` satisfying the JSON schema
        'schema/direct.schema.json'.
        """
        return
        yield None  # mark this method as a generator
