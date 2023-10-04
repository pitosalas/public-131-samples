from clock import Clock
import json
from pcb import PCB
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
import scheduler
from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from pathlib import Path


class Simulation:
    def __init__(self):
        self.clock = Clock()
        self.format = "full"

    def stepper(self, count):
        for i in range(count):
            self.clock.increment()
            if self.sched.all_processes_done():
                break
        self.print_status()

    def run_old(self):
        filename = self.prompt_for_filename()
        self.import_json_file(filename)
        self.construct_scheduler()
        self.clock.register_object(self.sched)
        self.configure_scheduler(self.data)
        intro_rg = self.generate_intro_render_group()

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
        status_rg = generate_status_rg()
        summary_rg = generate_summary_rg()
        console.print(Group)

    def construct_scheduler(self):
        """
        Constructs the scheduler based on the algorithm specified in the JSON file.
        """
        algo = self.data["sched_algorithm"]
        if algo == "FCFS":
            self.sched = scheduler.FCFS(self)
            print(self.sched.print_name)
        elif algo == "SJF":
            self.sched = scheduler.SJF(self)
        elif algo == "RR":
            self.sched = scheduler.RR(self)
        elif algo == "Priority":
            self.sched = scheduler.Priority(self)
        else:
            print("Invalid algorithm. Try again.")

    def prompt_for_filename(self):
        files = [f.name for f in Path('.').glob('*.json')]

        print("[bold]Select a file:[/bold]")
        for i, f in enumerate(files, 1):
            print(f"[{i}] {f}")
        choice = input("Enter your choice: ")
        choice = int(choice) if choice else 1
        return files[choice-1]

    def generate_intro_render_group(self):

        line1 = Text(f"Algorithm: {self.sched.print_name}", style="bold red")

        col_width = 8
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("PID", style="cyan", width=4)
        table.add_column(
            "Total Time\n(required by process)", justify="right", style="green", width=col_width)
        table.add_column(
            "Arrival Time\n(when process first arrives)", justify="right", style="green", width=col_width)
        table.add_column("Burst\n(average time of a CPU burst)",
                         justify="right", width=col_width)
        table.add_column("Priority\n(process priority",
                         justify="right", width=col_width)
        for pcb in self.sched.new_queue._list:
            table.add_row(str(pcb.pid), str(pcb.arrival_time),
                          str(pcb.burst_time), str(pcb.total_time), str(pcb.priority))
        return Group(line1, table)

    def gemerate_status_rg(self):
        """
        Prints the current status of the operating system representing the terminated queue.
        """
        line1 = text(f"Clock: {self.clock.get_time()}", style="bold red")
        line2 = text(f"Timeline: {self.sched.progress}", style="bold red")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Status!", style="red")
        table.add_column("PID", style="cyan")
        # table.add_column(
        #    "Arrival Time\n(when process first arrives)", justify="right", style="green")
        # table.add_column("Burst\n(average time of a CPU burst)",
        #                  justify="right")
        # table.add_column("Total CPU\n(Total CPU Time required)",
        #                  justify="right", style="green")
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
        return Group(line1, line2, table)

    def generate_summary_rg(self):
        """
        Prints the summary of the operating system representing the terminated queue.
        """
        line1 = Text(f"Clock: {self.clock.get_time()}", style="bold red")
        line2 = Text(
            f"Average Time spent Waiting: {self.sched.get_average_wait_time()}", style="bold red")
        line3 = Text(
            f"Average waiting before starting: {self.sched.get_average_start_time()}", style="bold red")
        return Group(line1, line2, line3)

# Function to read the json file
    def import_json_file(self, filename):
        with open(filename, 'r') as f:
            self.data = json.load(f)
            allowed = {'sched_algorithm', 'time_slice', 'number_of_processes',
                       'arrival_time', 'burst_time', 'total_time', 'auto', 'manual',
                       "format", "basic"
                       }
            if not all(key in allowed for key in self.data.keys()):
                print("Error: Invalid JSON file")
                exit()

    def configure_scheduler(self, data):
        self.format = data["format"]
        self.quantum = data["time_slice"]
        self.sched_algorithm = data["sched_algorithm"]

# if there is a key "manual", then we generate each process separately.
        for process in data["manual"]:
            pid = process['pid']
            arrival_time = process['arrival_time']
            burst_time = process['burst_time']
            total_time = process['total_time']
            priority = process['priority']
            pcb = PCB(pid, arrival_time, burst_time, total_time, priority)
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
