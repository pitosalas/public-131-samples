from lib.utils import pretty_mem_str, collapse_contiguous_ranges

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
    
"""
We create this in its empty state. We allocate the outer page table with all None
to indicate that there are no inner page tables yet. When we need to allocate a
page, we allocate the inner page table, and then allocate the page within that
table. The outer page table is indexed by the outer page number. The inner page
table is indexed by the inner page number. The inner page number is the offset1
from the logical address. The outer page number is the offset2 from the logical
address.
"""
class TwoLevelPageTable:
    def __init__(self, pagesize: int, page_count: int):
        self.table: list[None | int] = [None] * page_count
        self.pagesize = pagesize
        self.page_count = page_count

    def get_frame(self, page_number: int) -> int | None:
        return self.table[page_number]
    
    def set_frame(self, page_number: int, frame_number: int):
        self.table[page_number] = frame_number
    
    def __str__(self):
        return f"TwoLevelPageTable:  {collapse_contiguous_ranges(self.table)}"

class PCB:
    def __init__(self, process: str, mapping: Block | PageTable):
        self.mapping: Block | PageTable | TwoLevelPageTable = mapping
        self.process = process

    def __str__(self):
        return f"{self.process}  {self.mapping}"
