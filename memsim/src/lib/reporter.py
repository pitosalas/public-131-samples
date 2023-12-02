from lib.pagetables import PCB
from lib.utils import pretty_mem_str

class Reporter:
    def __init__(self):
        self.trace = ""
        pass

    def info(self, scenario: str, algo: str, file_name: str, default_multiplier: int):
        self.scenario = scenario
        self.algo = algo
        self.file_name = file_name
        self.phys_memory_stats = ""
        self.allocation_stats = ""
        self.defailt_multiplier = default_multiplier

    def add_trace(self, step):
        if step[0] == "a":
            self.trace += f"       LOAD: {step[1]} (asks {pretty_mem_str(int(step[2])*self.defailt_multiplier)} bytes\n"
        elif step[0] == "d":
            self.trace += f"     UNLOAD: {step[1]}\n"
        else:
            raise Exception(f"Invalid script file: {step['do']}")

    def add_allocations(self, allocs: dict[str, PCB]) -> None:
        self.allocation_stats = "\n        ".join(
            str(alloc) for alloc in allocs.values()
        )

    def add_segmented_memory_stats(self, memsize, segsize):
        self.phys_memory_stats = f"Physical Memory\n           {pretty_mem_str(memsize)}, segment size: {pretty_mem_str(segsize)}"

    def add_free_segments(self, free_segments: list[int]) -> None:
        self.free_segments = free_segments
        strings = []
        for block in self.free_segments:
            strings.append(f"{str(block)}")
        print_string = f"Free Segments:\n        {strings}"
        self.phys_memory_stats = print_string

    def add_paged_memory_stats(self, memsize: int, pagesize: int, framecount: int, frame_table: list[bool]):
        self.phys_memory_stats = f"Physical Memory\n        {pretty_mem_str(memsize)}, pagesize: {pretty_mem_str(pagesize)}, framecount: {framecount}"
        frame_table_str = ""
        for i, frame in enumerate(frame_table):
            frame_table_str += f"{frame} "
            if i % 32 == 31:
                frame_table_str += "\n           "
        self.phys_memory_stats += f"\n        Frames (X means in use)\n           {frame_table_str}"

    def add_seg_mem_stats(self, memsize: int, segsize: int):
        self.phys_memory_stats = f"Physical Memory:\n           {pretty_mem_str(memsize)}, segment size: {pretty_mem_str(segsize)}"
        self.phys_memory_stats += "\n           Free segments: self.add_free_segments(self.free_segments)"

    def report(self):
        print("----------------------------------------")
        print(f"SCENARIO: {self.scenario}")
        print("   STARTING CONDITIONS")
        print(f"      Memory Manager: {self.algo}")
        print(f"      Script file: {self.file_name}")
        print(f"\n   TRACE OF SIMULATION:\n{self.trace}")
        print("   AT COMPLETION:\n      Process Allocations:")
        print(f"        {self.allocation_stats}")
        print(f"      {self.phys_memory_stats}")
