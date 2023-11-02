"""
A simple memory magement simulation and demonstration app.
"""
import json
from mm_factory import MmFactory
from var_seg_mm import VarSegMm
from fixed_seg_mm import FixedSegMm



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

    def interactive(self):
        self.mmanager = MemoryManager(2)
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
        self.import_json_file("mm_var_seg_1.json")
        self.prepare_factory()
        algo = self.data["algo"]
        physical_g = self.data["physical_g"]
        self.mmanager = self.factory.create(algo)(physical_g)
        for step in self.data["script"]:
            print(step)
            self.execute_command(step)
        print(self.mmanager)


if __name__ == "__main__":
    sim = Simulator()
    #   sim.run()
    # sim.interactive()
    sim.batch()
