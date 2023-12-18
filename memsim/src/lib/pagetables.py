from abc import ABC

from lib.utils import extract_fields, pretty_mem_str, collapse_contiguous_ranges

class MemoryMapping(ABC):
    def __init__(self, capacity_bytes):
        self.capacity_bytes = capacity_bytes

class TwoLevelPageTable(MemoryMapping):
    """
    Two-level page table implementation.

    Args:
        page_size (int): The size of each page in bytes.
        entries_per_page_table (int): The number of entries per page table.

    Attributes:
        page_size (int): The size of each page in bytes.
        entries_per_page_table (int): The number of entries per page table.
        table (list[None | list[int]] | None): The two-level page table.

    Methods:
        allocate(logical_address: int) -> None:
            Allocates a page in the two-level page table for the given logical address.

        get_statistics() -> tuple[int, int]:
            Returns the number of inner page tables and data pages in the two-level page table.

        outer_pt_str() -> str:
            Returns a string representation of the outer page table.

        inner_pt_str() -> str:
            Returns a string representation of the inner page tables.

        __str__() -> str:
            Returns a string representation of the TwoLevelPageTable object.
    """
    def __init__(self, page_size: int, entries_per_page_table: int):
        super().__init__(entries_per_page_table**2 * page_size)
        self.page_size = page_size
        self.entries_per_page_table = entries_per_page_table
        self.table: list[None | list[int]] | None = [None] * entries_per_page_table
    
    def allocate(self, logical_address: int):
        pt_bits = (self.entries_per_page_table-1).bit_length()
        offset_bits = (self.page_size-1).bit_length()
        outer_page_number, inner_page_number, _ = extract_fields(logical_address, pt_bits, pt_bits, offset_bits)
        assert self.table is not None
        if self.table[outer_page_number] is None:
            self.table[outer_page_number] = [None] * self.entries_per_page_table
        inner_page_table = self.table[outer_page_number]
        assert inner_page_table is not None
        if inner_page_table[inner_page_number] is None:
            inner_page_table[inner_page_number] = "allocated"
    
    def get_statistics(self) -> tuple[int, int]:
        inner_pt_count = 0
        data_page_count = 0
        for inner_pt in self.table:
            if inner_pt is not None:
                inner_pt_count += 1
                for page in inner_pt:
                    if page is not None:
                        data_page_count += 1
        return inner_pt_count, data_page_count
    
    def outer_pt_str(self) -> str:
        result = "".join("." if entry is None else "x" for entry in self.table)
        return result.rstrip(".")+"......"

    def inner_pt_str(self) -> str:
        result = ""
        for i, inner_pt in enumerate(self.table):
            if inner_pt is not None:
                inner_result = "".join("." if entry is None else "x" for entry in inner_pt)
                result += f"                         Inner Page Table {i}: {inner_result.rstrip(".")}...\n"
        return result

    def __str__(self):
        inner_pt, data_page = self.get_statistics()
        return f"""2Lvl: {inner_pt} inner page tables, {data_page} data pages
                      Outer Page Table: {self.outer_pt_str()}
{self.inner_pt_str()}"""
        
class Block:
    def __init__(self, start: int, size: int):
        self.physical_address = start
        self.size = size

    def __str__(self):
        return f"start {pretty_mem_str(self.physical_address)}, size {pretty_mem_str(self.size)}"
    
    def contains(self, logical_address: int) -> bool:
        return logical_address <= self.size

class PageTable:
# A page table is an array, indexed by page number, that contains
# the frame number where that page is stored in memory.
    def __init__(self, process: str, physical_memory):
        self.table: list[int | None] = []
        self.frame_count = 0
        self.size: int | None = None
        self.phys_mem = physical_memory
        self.process = process
        page_table_frame = physical_memory.request_free_frame(process)
        if page_table_frame is None:
            raise ValueError(f"No free frames for process {process}'s page table")
        self.page_table_frame = page_table_frame

    
    def allocate(self, required_memory: int):
        required_frames = self.phys_mem.memory_to_frames(required_memory)
        for _ in range(required_frames):
            frame = self.phys_mem.request_free_frame(self.process)
            if frame is None:
                raise ValueError(f"No free frames to allocate another page for {self.process}")
            self.table.append(frame)
            self.frame_count += 1

    def __str__(self):
        return f"PageTable:  {collapse_contiguous_ranges(self.table)}"
    
class PCB:
    def __init__(self, process: str, mapping: Block | PageTable):
        self.mapping: Block | PageTable | TwoLevelPageTable = mapping
        self.process = process

    def __str__(self):
        return f"{self.process}  {self.mapping}"

