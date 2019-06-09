#!/usr/bin/env python3

import abc
from typing import Any, Dict, Iterable, Union


class Edge(abc.ABC):
    @property
    @abc.abstractmethod
    def src_node(self) -> int:
        raise NotImplemented

    @property
    @abc.abstractmethod
    def sink_node(self) -> int:
        raise NotImplemented

    @property
    @abc.abstractmethod
    def switch_id(self) -> int:
        raise NotImplemented

    @property
    @abc.abstractmethod
    def metadata(self) -> Union[Dict[str, Any], None]:
        """Metadata for edge."""
        raise NotImplemented


class Node(abc.ABC):
    pass


class ArchitectureDelegate(abc.ABC):
    @abc.abstractmethod
    def edges(self) -> Iterable[Edge]:
        raise NotImplemented

