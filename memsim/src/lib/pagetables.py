from abc import ABC, abstractmethod
from lib.utils import pretty_mem_str, collapse_contiguous_ranges

WORD_LENGTH = 32
class MemoryMapping(ABC):
    def __init__(self, capacity_bytes):
        self.capacity_bytes = capacity_bytes

    @abstractmethod
    def access(self, logical_address):
        pass

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
    def __init__(self, page_size: int, capcity_bytes: int):
        super().__init__(capcity_bytes)
        self.page_size = page_size
        outer_page_count = capcity_bytes // page_size
        self.table: list[None | list[int]] = [None] * outer_page_count

    def access(self, logical_address: int) -> int | None:
        outer_page_number, inner_page_number, page_offset = self.extract_fields(logical_address)   
        if self.table[outer_page_number] is None:
            self.table[outer_page_number] = [None] * (self.page_size // 4)
        inner_page_table = self.table[outer_page_number]
        if inner_page_table[inner_page_number] is None:
            inner_page_table[inner_page_number] = "allocated"
        return inner_page_table[inner_page_number] * self.page_size + page_offset
    

    def extract_fields(self, address: int) -> tuple[int, int, int]:
        # Calculate the number of bits needed for the page offset
        total_bits = WORD_LENGTH
        page_number_bits = self.page_size.bit_length()
        offset_bits = total_bits - 2 * page_number_bits

        # Extract the fields from the address
        outer_page_number = address >> offset_bits
        inner_page_number = (address >> (offset_bits - page_number_bits)) & ((1 << page_number_bits) - 1)
        offset = address & ((1 << offset_bits) - 1)
        return outer_page_number, inner_page_number, offset

    def __str__(self):
        return f"TwoLevelPageTable:  {collapse_contiguous_ranges(self.table)}"


   
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
    

class PCB:
    def __init__(self, process: str, mapping: Block | PageTable):
        self.mapping: Block | PageTable | TwoLevelPageTable = mapping
        self.process = process

    def __str__(self):
        return f"{self.process}  {self.mapping}"

