from lib.pagetables import Block, PageTable, TwoLevelPageTable
from abc import ABC, abstractmethod

PageTableOrNone = PageTable | TwoLevelPageTable | Block | None

class PhysMem(ABC):
    def __init__(self, args):
        pass
        
    @abstractmethod
    def __str__(self):
        return "Default memory manager string"

    @abstractmethod
    def allocate(self, process: str, size: int) -> Block | PageTable | TwoLevelPageTable | None:
        pass

    @abstractmethod
    def deallocate(self, process: str) -> None:
        pass

    @abstractmethod
    def launch(self, process: str, size: int) -> Block | PageTable | TwoLevelPageTable | None:
        return None


    @abstractmethod
    def report(self, rep):
        pass

    
