def gen_arch_xml(ostream, delegate):
    """Stream generate VPR's architecture description XML.

    Args:
        ostream: a file-like object, like a `file` or a `StringIO`
        delegate (`ArchitectureDelegate`): the delegate which answers questions about what are in the architecture
    """
    raise NotImplementedError
