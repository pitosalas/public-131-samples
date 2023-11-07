"""
A simple memory magement simulation and demonstration app.
"""
import json
from mm_factory import MmFactory
from memory_managers import VarSegMm
from memory_managers import FixedSegMm
from reporter import Reporter
from utils import convert_size_with_multiplier

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

    def import_json_file(self, filename):
        with open(filename, "r") as f:
            self.data = json.load(f)

    def execute_command(self, command):
        if command["do"] == "allocate":
            self.mmanager.allocate_k(command["process"], convert_size_with_multiplier(command))
        elif command["do"] == "deallocate": 
            self.mmanager.deallocate(command["process"], convert_size_with_multiplier(command))
        else:
            raise Exception(f"Invalid script file: {command['do']}")

    def batch(self):
        file_name = "memsim/scripts/mm_fixed_seg_2.json"
        self.import_json_file(file_name)
        self.prepare_factory()
        algo = self.data["algo"]["name"]
        rep.info(self.data["scenario"], algo, file_name)
        self.mmanager = self.factory.create(algo)(self.data["algo"]["memory"])
        for step in self.data["script"]:
            rep.add_trace(step)
            self.execute_command(step)
        self.mmanager.report(rep)

if __name__ == "__main__":
    rep = Reporter()
    sim = Simulator(rep)
    sim.batch()
    rep.report()