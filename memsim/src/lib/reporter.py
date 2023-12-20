from lib.pagetables import PCB
from lib.utils import pretty_mem_str


class Reporter:
    def __init__(self):
        self.trace = ""

    def info(self, scenario: str, algo: str, file_name: str, default_multiplier: int):
        self.scenario = scenario
        self.algo = algo
        self.file_name = file_name
        self.phys_memory_stats = ""
        self.allocation_stats = ""
        self.defailt_multiplier = default_multiplier

    def add_trace(self, step):
        if step[0] == "l":
            self.trace += f"       LNCH {step[1]}, {int(step[2])}\n"
        elif step[0] == "t":
            self.trace += f"       TERM: {step[1]}, {int(step[2])}\n"
        elif step[0] == "a":
            self.trace += f"       ALOC: {step[1]}, {int(step[2])}\n"
        else:
            raise ValueError(f"Invalid script file: {step[0]}")

    def add_allocations(self, allocs: dict[str, PCB]) -> None:
        self.allocation_stats = ""
        for pcb in allocs.values():
            self.allocation_stats += f"       {pcb}\n"

    def add_segmented_memory_stats(self, memsize, segsize):
        self.phys_memory_stats = f"Physical Memory\n           {pretty_mem_str(memsize)}, segment size: {pretty_mem_str(segsize)}"

    def add_free_segments(self, free_segments: list[int]) -> None:
        self.free_segments = free_segments
        strings = [f"{str(block)}" for block in self.free_segments]
        print_string = f"Free Segments:\n        {strings}"
        self.phys_memory_stats = print_string

    def add_paged_memory_stats(
        self, memsize: int, pagesize: int, framecount: int, frame_table: list[bool]
    ):
        self.phys_memory_stats = f"   PHYS MEM:\n        {pretty_mem_str(memsize)}, pagesize: {pretty_mem_str(pagesize)}, framecount: {framecount}"

        copy_frame_table = frame_table
        while copy_frame_table and copy_frame_table[-1] is None:
            copy_frame_table.pop()
        frame_table_list = map(lambda x: str(x) if x is not None else "x", copy_frame_table)
        frame_table_str = ", ".join(frame_table_list)+"..."
        self.phys_memory_stats += (
            f"\n        Frames:\n           {frame_table_str}")

    def add_seg_mem_stats(self, memsize: int, segsize: int):
        self.phys_memory_stats = f"PHYS MEM:\n           {pretty_mem_str(memsize)}, segment size: {pretty_mem_str(segsize)}"
        self.phys_memory_stats += (
            "\n           Free segments: self.add_free_segments(self.free_segments)"
        )

    def report(self):
        print("----------------------------------------")
        print(f"SCENARIO: {self.scenario}")
        print("   STARTING CONDITIONS")
        print(f"      Memory Manager: {self.algo}")
        print(f"      Script file: {self.file_name}")
        print(f"\n   TRACE OF SIMULATION:\n{self.trace}")
        print("   AT COMPLETION:\n      Process Allocations:")
        print(f"{self.allocation_stats}")
        print(f"{self.phys_memory_stats}")
