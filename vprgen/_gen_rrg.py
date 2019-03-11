def gen_rrg_xml(ostream, delegate):
    """Stream generate VPR's routing resource graph XML.

    Args:
        ostream: a file-like object, like a `file` or a `StringIO`
        delegate (`ArchitectureDelegate`): the delegate which answers questions about what are in the architecture
    """
    raise NotImplementedError

