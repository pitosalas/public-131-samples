from utils import PCB, convert_size_with_multiplier, pretty_mem_str


class Reporter:
    def __init__(self):
        self.trace: list[str] = []
        pass

    def info(self, scenario: str, algo: str, file_name: str):
        self.scenario = scenario
        self.algo = algo
        self.file_name = file_name
        self.phys_memory_stats = ""
        self.allocation_stats = ""

    def add_trace(self, step):
        self.trace.append(step)

    def add_allocations(self, allocs: list[PCB]) -> None:
        self.allocation_stats = "\n        ".join(
            str(alloc) for alloc in allocs.values()
        )

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
            strings.append(f"from seg {key[0]} to seg {key[1]}\n")
        return "        ".join(strings)

    def add_paged_memory_stats(self, memsize: int, pagesize: int, framecount: int):
        self.phys_memory_stats = f"Physical Memory\n        {pretty_mem_str(memsize)}, pagesize: {pretty_mem_str(pagesize)}, framecount: {framecount}"

    def report(self):
        print("----------------------------------------")
        print(f"SCENARIO: {self.scenario}")
        print("   STARTING CONDITIONS")
        print(f"      Memory Manager: {self.algo}")
        print(f"      Script file: {self.file_name}")
        print("   TRACE OF SIMULATION:")
        for step in self.trace:
            print(
                f"       '{step['process']}' {step['do']}s  {pretty_mem_str(convert_size_with_multiplier(step))}"
            )
        print("   AT COMPLETION:\n      Process Allocations:")
        print(f"        {self.allocation_stats}")
        print(f"      {self.phys_memory_stats}")
