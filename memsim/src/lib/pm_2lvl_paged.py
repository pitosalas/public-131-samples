from lib.pm_base import PhysMem, PageTableOrNone
from lib.reporter import Reporter
from lib.utils import convert_size_with_multiplier, find_free_sequence, set_sequence
from lib.pagetables import Block, PageTable, TwoLevelPageTable


class TwoLevelPagedPm(PhysMem):
    def __init__(self, memory_param: dict):
        super().__init__(memory_param)
        self.memparam = memory_param
        self.memsize = convert_size_with_multiplier(memory_param["memory"]["size"])
        self.pagesize = memory_param["algo"]["page_size"]
        if self.memsize % self.pagesize != 0:
            raise Exception("Memory size must be a multiple of page size")
        self.frame_count = self.memsize // self.pagesize
        self.freelist = [None] * self.frame_count
        self.page_tables = {}

    def __str__(self):
        return f"TwoLevelPagedPm = {self.memsize} MB"
    
    def launch(self, process: str, size: int) -> PageTableOrNone:
        required_frames = size // self.pagesize
        if size % self.pagesize != 0:
            required_frames += 1
        result = self.alloc(process, required_frames)
        if result is None:
            raise Exception("Allocation failed to find space")
        page_table =  TwoLevelPageTable(required_frames)
        self.page_tables[process] = page_table
        return page_table

    def alloc(self, marker: int, required_frames: int):
        target_frames = find_free_sequence(self.freelst, None, required_frames)
        if target_frames is None:
            return None
        set_sequence(self.freelist, target_frames, marker)
        return target_frames
 
    def terminate(self, mapping: PageTableOrNone) -> None:
        if mapping is None or not type(mapping) == TwoLevelPageTable:
            raise Exception("Invalid mapping")
        for frame in mapping.table:
            self.frame_table[frame] = None
        pass

    def build_page_dir(self, process: str, n_frames: int) -> PageTableOrNone:
        return None

    def report(self, rep: Reporter):
        rep.add_paged_memory_stats(self.memsize, self.pagesize, self.frame_count, self.frame_table)

    def touch(self, address: int) -> bool:
        return True
    
    def graph(self):
        print("Graph called in physmem")

    def reserve_free_frames(self, count: int):
        pass

    def allocate(self, process: str, size: int) -> Block | PageTable | None:
        pass

    def deallocate(self, process: str) -> None:
        pass

