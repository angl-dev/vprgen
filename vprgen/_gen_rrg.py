def gen_rrg_xml(ostream, delegate, pretty = True):
    """Stream generate VPR's routing resource graph XML.

    Args:
        ostream: a file-like object, like a `file` or a `StringIO`
        delegate (`ArchitectureDelegate`): the delegate which answers questions about what are in the architecture
        pretty (:obj:`bool`): if the output XML file should be nicely broken into multiple lines and indented
    """
    raise NotImplementedError

