"""
A simple memory magement simulation and demonstration app.
"""
import json
from utils import MmFactory
from memory_managers import PagedMm, VarSegMm
from memory_managers import FixedSegMm
from reporter import Reporter

class Simulator:
    def __init__(self, reporter: Reporter):
        self.reporter = reporter
        self.factory = None
        self.mmanager = None
        self.data = None

    def prepare_factory(self):
        self.factory = MmFactory()
        self.factory.register("var_seg", VarSegMm)
        self.factory.register("fixed_seg", FixedSegMm)
        self.factory.register("paged", PagedMm)

    def import_json_file(self, filename):
        with open(filename, "r") as f:
            self.config_file = json.load(f)

    # def execute_command(self, command):
    #     if command["do"] == "allocate":
    #         self.mmanager.allocate_k(command["process"], convert_size_with_multiplier(command))
    #     elif command["do"] == "deallocate": 
    #         self.mmanager.deallocate(command["process"])
    #     else:
    #         raise Exception(f"Invalid script file: {command['do']}")

    def execute_command(self, command):
        if command[0] == "a":
            self.mmanager.allocate(command[1], command[2])
        elif command[0] == "d": 
            self.mmanager.deallocate(command[1])
        else:
            raise Exception(f"Invalid script file: {command['do']}")
    def batch(self):
        file_name = "memsim/scripts/mm_paged_5.json"
        self.import_json_file(file_name)
        self.prepare_factory()
        algo = self.config_file["algo"]["name"]
        rep.info(self.config_file["scenario"], algo, file_name, eval(self.config_file["default_multiplier"]))
        self.mmanager = self.factory.create(algo)(self.config_file)
        for step in self.config_file["script"]:
            rep.add_trace(step)
            self.execute_command(step)
        self.mmanager.report(rep)

if __name__ == "__main__":
    rep = Reporter()
    sim = Simulator(rep)
    sim.batch()
    rep.report()