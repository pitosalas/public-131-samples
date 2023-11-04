"""
A simple memory magement simulation and demonstration app.
"""
import json
from mm_factory import MmFactory
from memory_managers import VarSegMm
from memory_managers import FixedSegMm

class Simulator:
    def __init__(self):
        pass

    def prepare_factory(self):
        self.factory = MmFactory()
        self.factory.register("var_seg", VarSegMm)
        self.factory.register("fixed_seg", FixedSegMm)

    def run(self):
        self.mmanager = VarSegMm(2)
        self.mmanager.allocate_k("p1", 512)
        self.mmanager.allocate_k("p2", 1024)
        self.mmanager.allocate_k("p3", 368)
        print(self.mmanager)

    def import_json_file(self, filename):
        with open(filename, "r") as f:
            self.data = json.load(f)

    def execute_command(self, command):
        if command["do"] == "allocate":
            self.mmanager.allocate_k(command["process"], command["k"])
        elif command["do"] == "deallocate": 
            self.mmanager.deallocate(command["process"])
        else:
            raise Exception(f"Invalid script file: {command['do']}")

    def interactive(self) -> None:
        self.prepare_factory()
        self.mmanager = self.factory.create("var_seg")(self.data["physical_g"])
        while True:
            command = input("Enter command: ")
            if command == "exit":
                break
            elif command == "allocate":
                process = input("Enter process name: ")
                size = int(input("Enter size in KB: "))
                self.mmanager.allocate_k(process, size)
            elif command == "deallocate":
                process = input("Enter process name: ")
                self.mmanager.deallocate(process)
            elif command == "print":
                print(self.mmanager)
            else:
                raise Exception("Invalid command")

    def batch(self):
        self.import_json_file("scripts/mm_fixed_seg_small.json")
        self.prepare_factory()
        algo = self.data["algo"]["name"]
        self.mmanager = self.factory.create(algo)(self.data["algo"]["memory"])
        for step in self.data["script"]:
            self.execute_command(step)
        print(self.mmanager)

if __name__ == "__main__":
    sim = Simulator()
    #   sim.run()
    # sim.interactive()
    sim.batch()
