from lib.pagetables import PageTable
from lib.pm_base import PhysMem
from lib.reporter import Reporter
from lib.utils import convert_size_with_multiplier


class PagedPm(PhysMem):
    def __init__(self, memory_param: dict):
        super().__init__(memory_param)
        self.memparam = memory_param
        self.pagesize = memory_param["algo"]["page_size"]
        self.memsize = convert_size_with_multiplier(memory_param["memory"]["size"])
        self.frame_count = self.memsize // self.pagesize
        self.frame_table: list[None | str] = [None] * self.frame_count
        if self.memsize % self.pagesize != 0:
            raise ValueError("Memory size must be a multiple of page size")

    def __str__(self):
        return f"PhysicalMemory = {self.memsize} MB"

    def launch(self, process: str, size: int) ->  PageTable | None:
        required_frames = size // self.pagesize
        if size % self.pagesize != 0:
            required_frames += 1
        return self.build_page_table(process, required_frames)

    def allocate(self, process: str, size: int) -> PageTable | None:
        return None

    def request_free_frame(self, process: str) -> int | None:
        for index, frame in enumerate(self.frame_table):
            if frame is None:
                self.frame_table[index] = process
                return index
        return None
    
    def deallocate(self, mapping: PageTable) -> None:
        for frame in mapping.table:
            if frame is not None:
                self.frame_table[frame] = None

    def __build_page_table(self, process: str, n_frames: int) -> PageTable | None:
        page_table = PageTable(self.pagesize)
        for index, frame in enumerate(self.frame_table):
            if frame is not None:
                continue
            page_table.add_frame(index)
            self.frame_table[index] = process
            n_frames -= 1
            if n_frames == 0:
                return page_table
        return None

    def report(self, rep: Reporter):
        rep.add_paged_memory_stats(
            self.memsize, self.pagesize, self.frame_count, self.frame_table
        )
    def graph(self):
        print("Graph called in physmem")

    def memory_to_frames(self, required_memory):
        fragment = 1 if required_memory % self.pagesize != 0 else 0
        return (required_memory // self.pagesize) + fragment
        
