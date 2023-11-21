"""
A simple memory magement simulation and demonstration app.
"""
import json
from diag.diag import Diagram
from utils import MmFactory
from memory_managers import MemoryManager, PagedMm, VarSegMm
from memory_managers import FixedSegMm
from reporter import Reporter

SCRIPT_FILE="paged0.json"

class Simulator:
    def __init__(self, reporter: Reporter, diag: Diagram):
        self.rep = reporter
        self.dg = diag
        self.factory = None
        self.mmanager: MemoryManager = None
        self.data = None

    def prepare_factory(self):
        self.factory: MmFactory = MmFactory()
        self.factory.register("var_seg", VarSegMm)
        self.factory.register("fixed_seg", FixedSegMm)
        self.factory.register("paged", PagedMm)

    def import_json_file(self, filename):
        with open(filename, "r") as f:
            self.config_file = json.load(f)

    # available commands: a, d
    # a: allocate (process, size)
    # d: deallocate (process)
    # l: load (process, maxsize)
    # t: touch (process, start, end)

    def execute_command(self, command):
        self.rep.add_trace(command)
        if command[0] == "a":
            self.mmanager.allocate(command[1], int(command[2]) * self.def_mult)
        elif command[0] == "d":
            self.mmanager.deallocate(command[1])
        elif command[0] == "l":
            self.mmanager.load(command[1], int(command[2] * self.def_mult))
        elif command[0] == "t":
            self.mmanager.touch(command[1], int(command[2]), int(command[3]))
        else:
            raise Exception(f"Invalid script file: {command['do']}")

    def batch(self):
        file_name = f"memsim/scripts/{SCRIPT_FILE}"
        self.import_json_file(file_name)
        self.def_mult = eval(self.config_file["default_multiplier"])
        self.prepare_factory()
        algo = self.config_file["algo"]["name"]
        rep.info(self.config_file["scenario"], algo, file_name, self.def_mult)
        self.mmanager = self.factory.create(algo)(self.config_file)
        for step in self.config_file["script"]:
            self.execute_command(step)
        self.mmanager.report(self.rep)
        self.mmanager.graph(self.dg)

if __name__ == "__main__":
    rep = Reporter()
    dg = Diagram(f"memsim/graphs/{SCRIPT_FILE}", "LR")
    sim = Simulator(rep, dg)
    sim.batch()
    rep.report()
    dg.generate_diagram()
