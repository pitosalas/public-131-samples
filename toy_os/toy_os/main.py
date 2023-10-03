# The toy operating system will demonstrate different scheduling algorithms.
import json
import random
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.color import Color, ColorType
from rich.markdown import Markdown


DOC = """
# Important definitions:

* Simulation variables:
    * Time: Simulation time. Measured in 'tics'. Starts at zero.

* Each process is configured initially with
    * Arrival Time: When the process arrives to the scheduler for the first time
    * Burst Time: Total number CPU tics the process will use before it has to wait (for I/O etc.)
    * Total Time: Total number CPU tics the process will use until it exists

* Once the simulation starts, each process tracks the following
    * Run Time: Number of CPU tics the process has used so far
    * Wall Time: Number of tics since the process was first run
    * Wait Time: Total tics a process spends waiting (on ready and wait queues)
    * Response Time: Number of tics from when a process is first run until it starts running
    * Start Time: Time(tics) when the process was first run

* When the simulation completes the following are calculated:
* Throughput: Average number of processes completed per tic
* Turnaround: Average number of tics used for a process (1/Througput)
"""


class PCB:
    """
    Process Control Block (PCB) class represents a process in the operating system.
    It contains information about the process such as its process ID (pid), arrival time,
    burst time, priority, and completion time.
    """

    def __init__(self, pid, arrival_time, burst_time, total_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.total_time = total_time
        self.run_time = 0
        self.wall_time = None
        self.start_time = None
        self.wait_time = 0
        self.status = "New"

    def update(self, time):
        if self.status not in ("New", "Terminated"):
            self.wall_time = time

    def __repr__(self):
        return f"PCB({self.pid}, {self.arrival_time}, {self.burst_time}, {self.total_time}, {self.wait_time})"


class Queue:
    def __init__(self, name):
        self.name = name
        self._list = []

    def add_at_end(self, pcb):
        pcb.status = self.name
        self._list += [pcb]

    def remove_from_front(self):
        pcb = self._list[0]
        self._list = self._list[1:]
        return pcb

    def remove(self, pcb):
        self._list.remove(pcb)
        return pcb

    def empty(self):
        return len(self._list) == 0

    @property
    def head(self):
        if len(self._list) > 0:
            return self._list[0]
        else:
            return None

    def __repr__(self):
        return f"Queue(\"{self.name}\")"

    def print(self, table):
        for pcb in self._list:
            table.add_row(pcb.status, str(pcb.pid), str(pcb.arrival_time), str(
                pcb.burst_time), str(pcb.total_time), str(pcb.run_time), str(pcb.wall_time), str(pcb.start_time), str(pcb.wait_time))


class Clock:
    """
    A class representing a clock that can be incremented and observed by registered objects.
    """

    def __init__(self):
        self.watchers = []
        self.time = 0

    def increment(self):
        for obj in self.watchers:
            obj.update(self.time)
        self.time += 1

    def get_time(self):
        return self.time

    def register_object(self, obj):
        self.watchers.append(obj)

    def unregister_object(self, obj):
        self.watchers.remove(obj)


class Scheduler:
    def __init__(self, clock):
        self.new_queue = Queue("New")
        self.ready_queue = Queue("Ready Queue")
        self.waiting_queue = Queue("Waiting Queue")
        self.terminated_queue = Queue("Terminated")
        self.running = Queue("Running")
        self.clock = clock
        self.progress = ""

    def all_processes_done(self):
        """
        Returns True if all processes are done, False otherwise.
        """
        return self.running.head == None and self.new_queue.head == None and self.ready_queue.head == None and self.waiting_queue.head == None

    def move_to_ready(self):
        # while there are still pcbs on new queue, remove them from new queue and add them to ready queue
        to_move = []
        for pcb in self.new_queue._list:
            if pcb.arrival_time <= self.clock.get_time():
                to_move += [pcb]
        for pcb in to_move:
            pcb.wall_time = self.clock.get_time()
            self.ready_queue.add_at_end(self.new_queue.remove(pcb))

    def handle_done(self):
        # if there is a running process, check if it is done
        current_process = self.running.head
        if current_process is not None and current_process.run_time >= current_process.total_time:
            # if it is done, add it to the terminated queue and set running to None
            self.terminated_queue.add_at_end(
                self.running.remove(current_process))

    def schedule_next(self):
        # Return if no one to run
        if not self.running.empty() or self.ready_queue.empty():
            return
        process_to_run = self.ready_queue.remove_from_front()
        self.running.add_at_end(process_to_run)

    def update_running_process(self):
        # if there is a running process, increment its time
        running = self.running.head
        if running is None:
            return
        running.run_time += 1
        if running.start_time is None:
            running.start_time = self.clock.get_time()
        self.progress += f"{running.pid}|"

    def update_waiting_processes(self):
        for waiting in self.waiting_queue._list:
            waiting.wait_time += 1
        for ready in self.ready_queue._list:
            ready.wait_time += 1
            if ready.start_time is not None:
                ready.start_time = self.clock.get_time()

    def update(self, time):
        self.move_to_ready()
        self.handle_done()
        self.schedule_next()
        self.update_running_process()
        self.update_waiting_processes()

    def __repr__(self):
        return "Scheduler({clock} )"

    def get_average_wait_time(self):
        """
        Returns the average wait time of all processes.
        """
        total = 0
        for pcb in self.terminated_queue._list:
            total += pcb.wait_time
        if len(self.terminated_queue._list) == 0:
            return 0
        else: 
            return float(total) / len(self.terminated_queue._list)

    def get_average_start_time(self):
        """
        Returns the average time waiting  before starting
        """
        total = 0
        for pcb in self.terminated_queue._list:
            total += pcb.start_time
        if len(self.terminated_queue._list) == 0:
            0
        else:
            return float(total) / len(self.terminated_queue._list)


class Simulation:
    def __init__(self):
        self.clock = Clock()
        self.sched = Scheduler(self.clock)
        self.clock.register_object(self.sched)

    def print_status(self):
        """
        Prints the current status of the operating system representing the terminated queue.
        """
        console = Console()
        # console.clear()
        # md = Markdown(DOC)
        # console.print(md)

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
        table.add_column("Current CPU\n(CPU consumed so far)",
                         justify="right", style="green")
        table.add_column(
            "Wall Time\n(Elapsed time since first starting)", justify="right", style="green")
        table.add_column("Start Time\n(Wating time until started)",
                         justify="right", style="green")
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


# Function to ead the json file


    def import_json_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            allowed = {'sched_algorithm', 'time_slice', 'number_of_processes',
                       'arrival_time', 'burst_time', 'total_time', 'auto', 'manual'}
            if not all(key in allowed for key in data.keys()):
                print("Error: Invalid JSON file")
                exit()
# if there is a key "manual", then we generate each process separately. The auto key is followed by an array of
# zero or more process blocks. Each process block has a pid and a burst time. For each one we create a PCB and
# add it to the new queue. We also register the PCB with the clock so that it will be updated each time the clock.abs
# is incremented.
            for process in data["manual"]:
                pid = process['pid']
                arrival_time = process['arrival_time']
                burst_time = process['burst_time']
                total_time = process['total_time']
                pcb = PCB(pid, arrival_time, burst_time, total_time)
                self.sched.new_queue.add_at_end(pcb)
                self.clock.register_object(pcb)

# if there is a key "auto", then we generate the processes randomly. The number of processes is given by
# the number_of_processes key. The arrival_time, burst_time, and total_time keys are followed by a from and
# to key. We generate a random number between from and to for each process. We also register the PCB with
# #the clock so that it will be updated each time the clock is incremented.
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

    def stepper(self, count):
        for i in range(count):
            self.clock.increment()
        self.print_status()

    def run(self):
        # import the json file
        self.import_json_file("processes.json")
        while (not self.sched.all_processes_done()):
            self.print_status()
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


if __name__ == "__main__":
    s = Simulation()
    s.run()
