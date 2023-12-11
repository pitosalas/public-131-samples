from lib.pagetables import Block, PageTable
from lib.pm_base import PhysMem
from lib.reporter import Reporter
from lib.utils import collapse_contiguous_ranges, convert_size_with_multiplier, find_and_remove

class FixedSegPhysMem(PhysMem):
    def __init__(self, args: dict):
        super().__init__(args)
        self.memsize = convert_size_with_multiplier(args["memory"]["size"])
        self.segsize = convert_size_with_multiplier(args["memory"]["seg"])
        self.seg_count = self.memsize // self.segsize
        if self.memsize % self.segsize != 0:
            raise ValueError("Memory size must be a multiple of segment size")
        self.free_segments = list(range(self.seg_count))
        self.seg_table: list[None | str] = [None] * self.seg_count

    def __str__(self):
        return str(collapse_contiguous_ranges(self.free_segments))

    def allocate(self, process: str,  size: int) -> Block | None:
        segments = self.find_contiguous_segments(size, self.free_segments)
        if segments is None:
            return None
        self.free_segments = segments[1]
        for seg in segments[0]:
            self.seg_table[seg] = process
        self.seg_table[segments[0][0]] = process
        return Block(segments[0][0]*self.segsize, size)
        
    def find_contiguous_segments(self, size, free_list) -> list[list[int]] | None:
        segs_needed = size // self.segsize
        return find_and_remove(free_list, segs_needed)
        
    def deallocate(self, block: Block) -> None:
        for i in range(block.size// self.segsize):
            self.free_segments.append(block.physical_address//self.segsize + i)
            self.seg_table[block.physical_address//self.segsize + i] = None
        self.free_segments.sort()

    def report(self, rep: Reporter):
        flattened = collapse_contiguous_ranges(self.free_segments)
        rep.add_free_segments(flattened)
        rep.add_seg_mem_stats(self.memsize, self.segsize)

    def touch(self, process: str, address: int) -> bool:
        return True

    def launch(self, size):
        pass

    def terminate(self, mapping: Block | PageTable):
        pass