from lib.pm_base import PhysMem, PageTableOrNone
from lib.reporter import Reporter
from lib.pagetables import TwoLevelPageTable
from lib.utils import convert_size_with_multiplier


class TwoLevelPagedPm(PhysMem):
    def __init__(self, memory_param: dict):
        super().__init__(memory_param)
        self.memparam = memory_param
        self.memsize = convert_size_with_multiplier(memory_param["memory"]["size"])
        self.pagesize = memory_param["algo"]["page_size"]
        if self.memsize % self.pagesize != 0:
            raise ValueError("Memory size must be a multiple of page size")
        self.frame_count = self.memsize // self.pagesize
        self.freelist = [None] * self.frame_count
        self.page_tables:dict[str, TwoLevelPageTable] = {}

    def __str__(self):
        return f"TwoLevelPagedPm = {self.memsize} MB"

    def launch(self, process: str, outer_page_table_entries: int) -> PageTableOrNone:
        page_table = TwoLevelPageTable(self.pagesize, outer_page_table_entries)
        self.page_tables[process] = page_table
        return page_table


    def allocate(self, process: str, address: int):
        page_table: TwoLevelPageTable = self.page_tables[process]
        if page_table is None:
            raise ValueError("Invalid mapping")
        page_table.allocate(address)
        

    def report(self, rep: Reporter):
        pass

    def graph(self):
        print("Graph called in physmem")

    def reserve_free_frames(self, count: int):
        pass


    def deallocate(self, process: str) -> None:
        pass
