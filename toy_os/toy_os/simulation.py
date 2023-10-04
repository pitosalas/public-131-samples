from clock import Clock
import json
from pcb import PCB
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
import scheduler
from rich import print
from pathlib import Path


class Simulation:
    def __init__(self):
        self.clock = Clock()
        self.format = "full"
        self.sched = scheduler.RRP(self)
        self.clock.register_object(self.sched)

    def stepper(self, count):
        for i in range(count):
            self.clock.increment()
            if self.sched.all_processes_done():
                break
        self.print_status()

    def run(self):
        filename = self.prompt_for_filename()
        self.import_json_file(filename)
        while (not self.sched.all_processes_done()):
            response = input("[s(tep),q(uit), g(o): ")
            if response == 'q':
                break
            elif response == 's':
                self.stepper(1)
            elif response == 'g':
                self.stepper(100)
                break
            else:
                print("Invalid response. Try again.")
        self.clock.increment()
        self.print_status()
        self.print_summary()

    def prompt_for_filename(self):
        files = [f.name for f in Path('.').glob('*.json')]

        print("[bold]Select a file:[/bold]")
        for i, f in enumerate(files, 1):
            print(f"[{i}] {f}")
        choice = input("Enter your choice: ")
        choice = int(choice) if choice else 1
        return files[choice-1]

    def print_status(self):
        """
        Prints the current status of the operating system representing the terminated queue.
        """
        print(self.clock.get_time())
        print(self.sched.progress)
        console = Console()
        console.clear()
        console.print(f"Clock: {self.clock.get_time()}", style="bold red")
        console.print(f"Timeline: {self.sched.progress}", style="bold red")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Status!", style="red")
        table.add_column("PID", style="cyan")
        table.add_column(
            "Arrival Time\n(when process first arrives)", justify="right", style="green")
        table.add_column("Burst\n(average time of a CPU burst)",
                         justify="right")

        table.add_column("Total CPU\n(Total CPU Time required)",
                         justify="right", style="green")
        table.add_column("Run Time\n(CPU consumed so far)",
                         justify="right", style="green")
        if self.format == "full":
            table.add_column(
                "Wall Time\n(Elapsed time since first starting)", justify="right", style="green")
        table.add_column("Wait Time\n(Wating time until started)",
                         justify="right", style="green")
        if self.format == "full":
            table.add_column(
                "Waiting Time\n(Time spent waiting overall)", justify="right", style="green")

        self.sched.running.print(table)
        self.sched.ready_queue.print(table)
        self.sched.waiting_queue.print(table)
        self.sched.terminated_queue.print(table)
        self.sched.new_queue.print(table)
        console.print(table)

    def print_summary(self):
        """
        Prints the summary of the operating system representing the terminated queue.
        """
        console = Console()
        console.print(f"Clock: {self.clock.get_time()}", style="bold red")
        console.print(
            f"Average Time spent Waiting: {self.sched.get_average_wait_time()}", style="bold red")
        console.print(
            f"Average waiting before starting: {self.sched.get_average_start_time()}", style="bold red")

# Function to read the json file
    def import_json_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            allowed = {'sched_algorithm', 'time_slice', 'number_of_processes',
                       'arrival_time', 'burst_time', 'total_time', 'auto', 'manual',
                       "format", "basic"
                       }
            if not all(key in allowed for key in data.keys()):
                print("Error: Invalid JSON file")
                exit()
            self.format = data["format"]
            self.quantum = data["time_slice"]

# if there is a key "manual", then we generate each process separately.
            for process in data["manual"]:
                pid = process['pid']
                arrival_time = process['arrival_time']
                burst_time = process['burst_time']
                total_time = process['total_time']
                pcb = PCB(pid, arrival_time, burst_time, total_time)
                self.sched.new_queue.add_at_end(pcb)
                self.clock.register_object(pcb)

# if there is a key "auto", then we generate the processes randomly.
            pid = 0
            auto = data["auto"]
            if auto is not None:
                for i in range(auto['number_of_processes']):
                    pid = i + 1
                    arrival_time = random.randint(
                        auto['arrival_time']['from'], auto['arrival_time']['to'])
                    burst_time = random.randint(
                        auto['burst_time']['from'], auto['burst_time']['to'])
                    total_time = random.randint(
                        auto['total_time']['from'], auto['total_time']['to'])
                    pcb = PCB(pid, arrival_time, burst_time, total_time)
                    self.sched.new_queue.add_at_end(pcb)
                    self.clock.register_object(pcb)
