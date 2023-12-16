"""
A simple memory magement simulation and demonstration app.
"""
import json
from diag.diag import Diagram
from lib.mm_2lvl_paged import TwoLvlPagedMm
from lib.mm_fixed_seg import FixedSegMm
from lib.mm_base import MemoryManager, MmFactory
from lib.mm_paged import PagedMm
from lib.reporter import Reporter
from lib.mm_var_seg import VarSegMm

SCRIPT_FILE = "segvar3.json"

class Simulator:
    def __init__(self, reporter: Reporter, diag: Diagram):
        self.rep = reporter
        self.dg = diag
        self.factory = None
        self.mmanager: MemoryManager | None = None
        self.data = None

    def prepare_factory(self):
        self.factory: MmFactory = MmFactory() 
        self.factory.register("var_seg", VarSegMm)
        self.factory.register("fixed_seg", FixedSegMm)
        self.factory.register("paged", PagedMm)
        self.factory.register("twolevel", TwoLvlPagedMm)

    def import_json_file(self, filename):
        with open(filename, "r") as f:
            self.config_file = json.load(f)

    # available commands: l, t, a, d
    # l: launch (process, pointers per page table)
    # t: touch (process, start, end)
    # a: allocate (process, address)
    #   allocate a block of memory at the address
    # d: deallocate (process)
    #   deallocate a block of memory at the address
    
    def execute_command(self, command):
        self.rep.add_trace(command)
        assert self.mmanager is not None
        if command[0] == "l":
            self.mmanager.launch(command[1], int(command[2]))
        elif command[0] == "t":
            self.mmanager.terminate(command[1])
        elif command[0] == "a":
            self.mmanager.allocate(command[1], int(command[2]) * self.def_mult)
        else:
            raise ValueError(f"Invalid script file: {command}")

    def batch(self):
        file_name = f"scripts/{SCRIPT_FILE}"
        self.import_json_file(file_name)
        self.def_mult = eval(self.config_file["default_multiplier"])
        self.prepare_factory()
        algo = self.config_file["algo"]["name"]
        rep.info(self.config_file["scenario"], algo, file_name, self.def_mult)
        clazz = self.factory.create(algo)
        self.mmanager = clazz(self.config_file)
        for step in self.config_file["script"]:
            self.execute_command(step)
        self.mmanager.report(self.rep)
        self.mmanager.graph(self.dg)

if __name__ == "__main__":
    rep = Reporter()
    dg = Diagram(f"graphs/{SCRIPT_FILE}", "LR")
    sim = Simulator(rep, dg)
    sim.batch()
    rep.report()
    dg.generate_diagram()
