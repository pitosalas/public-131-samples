from abc import ABC, abstractmethod
from lib.reporter import Reporter
from diag.diag import Diagram


class MemoryManager(ABC):
    """Keeps track of each Job that it has given memory to in the dict allocations. The key is the name of the job and the value is a MemoryAllocation object."""

    @abstractmethod
    def __init__(self, memory_param: dict):
        pass

    @abstractmethod
    def launch(self, process: str, size: int):
        pass

    @abstractmethod
    def terminate(self, process: str):
        pass

    @abstractmethod
    def allocate(self, process: str, address: int):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def report(self, rep: Reporter):
        pass

    @abstractmethod
    def graph(self, dg: Diagram):
        pass


"""
A memory manager factory, to create instances of the right kind of memory manager based on the user input.
"""
class MmFactory:
    def __init__(self) -> None:
        self.memory_manager_classes: dict = {}

    def register(self, name, memory_manager_class):
        self.memory_manager_classes[name] = memory_manager_class

    def create(self, name):
        if clazz := self.memory_manager_classes.get(name):
            return clazz
        else:
            raise ValueError(name)