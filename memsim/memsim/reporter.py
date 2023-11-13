from dotgen import Dotgen
from utils import PCB, pretty_mem_str

class Reporter:
    def __init__(self):
        self.trace = ""
        self.dg = Dotgen("memsim.gv")
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

    def add_allocations(self, allocs: list[PCB]) -> None:
        self.allocation_stats = "\n        ".join(
            str(alloc) for alloc in allocs.values()
        )
        for procs in allocs.values():
            self.dg.add_process(procs.process, procs.mapping)

    def add_segmented_memory_stats(self, memsize, segsize):
        self.phys_memory_stats = f"Physical Memory\n           {pretty_mem_str(memsize)}, segment size: {pretty_mem_str(segsize)}"

    def add_free_segments(self, free_segments: list[int]) -> None:
        self.free_segments = free_segments

    def render_allocs(self) -> str:
        strings = []
        for key in self.allocs:
            strings.append(f"{str(self.allocs[key])}\n")
        return "        ".join(strings)

    def render_free_segments(self) -> str:
        strings = []
        for key in self.free_segments:
            strings.append(f"[{key[0]}..{key[1]}]")
        return ", ".join(strings)

    def add_paged_memory_stats(self, memsize: int, pagesize: int, framecount: int, frame_table: list[bool]):
        self.phys_memory_stats = f"Physical Memory\n        {pretty_mem_str(memsize)}, pagesize: {pretty_mem_str(pagesize)}, framecount: {framecount}"
        frame_table_str = ""
        for i, frame in enumerate(frame_table):
            frame_table_str += f"{frame} "
            if i % 32 == 31:
                frame_table_str += "\n           "
            self.dg.paged_mem_frame(i, frame)
        self.phys_memory_stats += f"\n        Frames (X means in use)\n           {frame_table_str}"
        self.dg.paged_mem_complete()

    def add_seg_mem_stats(self, memsize: int, segsize: int):
        self.phys_memory_stats = f"Physical Memory:\n           {pretty_mem_str(memsize)}, segment size: {pretty_mem_str(segsize)}"
        self.phys_memory_stats += f"\n           Free segments: {self.render_free_segments()}"
        # self.dg.seg_mem_complete()




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
        self.dot_generate()

    def dot_generate(self):
        self.dg.generate()
