from abc import ABC, abstractmethod
from lib.utils import pretty_mem_str, collapse_contiguous_ranges

WORD_LENGTH = 32
class MemoryMapping(ABC):
    def __init__(self, capacity_bytes):
        self.capacity_bytes = capacity_bytes

"""
We create this in its empty state. We allocate the outer page table with all None
to indicate that there are no inner page tables yet. When we need to allocate a
page, we allocate the inner page table, and then allocate the page within that
table. The outer page table is indexed by the outer page number. The inner page
table is indexed by the inner page number. The inner page number is the offset1
from the logical address. The outer page number is the offset2 from the logical
address.
"""
class TwoLevelPageTable(MemoryMapping):
    def __init__(self, page_size: int, entries_per_page_table: int):
        super().__init__(entries_per_page_table**2 * page_size)
        self.page_size = page_size
        self.page_table_size = entries_per_page_table
        self.table: list[None | list[int]] | None = [None] * entries_per_page_table
        if (page_size-1).bit_length() * 3 > WORD_LENGTH:
            raise ValueError(f"Page size {page_size} is too large for a two-level page table")

    # def access(self, logical_address: int) -> int | None:
    #     assert self.table is not None
    #     outer_page_number, inner_page_number, page_offset = self.extract_fields(logical_address)   
    #     if self.table[outer_page_number] is None:
    #         self.table[outer_page_number] = [None] * (self.page_size // 4)
    #     inner_page_table = self.table[outer_page_number]
    #     assert inner_page_table is not None
    #     if inner_page_table[inner_page_number] is None:
    #         inner_page_table[inner_page_number] = "allocated"
    #     return inner_page_table[inner_page_number] * self.page_size + page_offset
    

    def extract_fields(self, address: int) -> tuple[int, int, int]:
        # Calculate the number of bits needed for the page offset
        total_bits = WORD_LENGTH
        page_number_bits = self.page_size.bit_length()
        shift_right_to_outer = total_bits - page_number_bits
        shift_right_to_inner = shift_right_to_outer - page_number_bits
        mask_to_offset = (1 << 12) - 1
        page_offset = address & mask_to_offset
        
        # Calculate the number of bits needed for the inner page number
        # After having shifted the whole address to the right by the number of bits
        mask_to_inner = (1 << 10) - 1
        inner_page_number = (address >> shift_right_to_inner) & mask_to_inner
        outer_page_number = (address >> shift_right_to_outer)
        return outer_page_number, inner_page_number, page_offset
    
    def allocate(self, logical_address: int):
        outer_page_number, inner_page_number, _ = self.extract_fields(logical_address)
        assert self.table is not None
        if self.table[outer_page_number] is None:
            self.table[outer_page_number] = [None] * self.page_table_size
        inner_page_table = self.table[outer_page_number]
        assert inner_page_table is not None
        if inner_page_table[inner_page_number] is None:
            inner_page_table[inner_page_number] = "allocated"
    
    def total_allocated(self) -> int:
        assert self.table is not None
        return sum(len(x)*self.page_size for x in self.table if x is not None)

    def __str__(self):
        return f"""TwoLevelPageTable: {pretty_mem_str(self.total_allocated())} Bytes"""


   
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
    def __init__(self, pagesize: int):
        self.table: list[int | None] = []
        self.frame_count = 0
        self.pagesize = pagesize
        self.size: int | None = None
    
    def add_frame(self, frame: int):
        self.table.append(frame)
        self.frame_count += 1
        self.size = self.frame_count * self.pagesize

    def __str__(self):
        return f"PageTable:  {collapse_contiguous_ranges(self.table)}"
    
    def total_allocated(self) -> int:
        return self.frame_count * self.pagesize

class PCB:
    def __init__(self, process: str, mapping: Block | PageTable):
        self.mapping: Block | PageTable | TwoLevelPageTable = mapping
        self.process = process

    def __str__(self):

        return f"{self.process}  {self.mapping}"

