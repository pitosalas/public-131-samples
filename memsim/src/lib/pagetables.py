from abc import ABC

from lib.utils import extract_fields, pretty_mem_str, collapse_contiguous_ranges

class MemoryMapping(ABC):
    def __init__(self, process: str, physmem_instance):
        self.physmem = physmem_instance
        self.process = process


class PageTable:
# A page table is an array, indexed by page number, that contains
# the frame number where that page is stored in memory.
    def __init__(self, process: str, physmem_instance):
        self.table: list[int | None] = []
        self.frame_count = 0
        self.size: int | None = None
        self.page_table_frame = physmem_instance.request_free_frame(f"{process}-page-table")
        if self.page_table_frame is None:
            raise ValueError(f"No free frames for process {process}'s page table")

    
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
    def __init__(self, process: str, physmem_instance, entries_per_page_table):
        super().__init__(process, physmem_instance)
        self.table: list[None | list[int]] | None = [None] * entries_per_page_table
        self.frame_count = 0
        self.size: int | None = None
        self.entries_per_page_table = entries_per_page_table
        self.page_table_frame = self.physmem.request_free_frame(f"{self.process}-outer-pt")
        if self.page_table_frame is None:
            raise ValueError(f"No free frames to allocate outer page table for {self.process}")
    
    def allocate(self, logical_address: int):
        pt_bits = (self.entries_per_page_table-1).bit_length()
        offset_bits = (self.physmem.pagesize-1).bit_length()
        outer_page_number, inner_page_number, _ = extract_fields(logical_address, pt_bits, pt_bits, offset_bits)
        assert self.table is not None
        if self.table[outer_page_number] is None:
            self.table[outer_page_number] = [None] * self.entries_per_page_table
            self.frame_count += 1
            self.page_table_frame = self.physmem.request_free_frame(f"{self.process}-inner-pt")

        inner_page_table = self.table[outer_page_number]
        assert inner_page_table is not None
        if inner_page_table[inner_page_number] is None:
            frame = self.physmem.request_free_frame(f"{self.process}")
            if frame is None:
                raise ValueError(f"No free frames to allocate another page for {self.process}")
            inner_page_table[inner_page_number] = frame
            self.frame_count += 1

    
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


class PCB:
    def __init__(self, process: str, mapping: Block | PageTable):
        self.mapping: Block | PageTable | TwoLevelPageTable = mapping
        self.process = process

    def __str__(self):
        return f"{self.process}  {self.mapping}"

