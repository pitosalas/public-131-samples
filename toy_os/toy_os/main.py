# The toy operating system will demonstrate different scheduling algorithms.
import json
import random
from rich.table import Table
from rich.console import Console


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
        self.wall_time = 0
        self.next = None
        self.status = "New"

    def update(self, time):
        if self.status not in ("New", "Terminated"):
            self.wall_time += 1


class Queue:
    """
    A class representing a queue data structure.

    Attributes:
    - head: The first element in the queue.
    - tail: The last element in the queue.
    - name: The name of the queue.

    Methods:
    - add(pcb): Adds a Process Control Block (pcb) to the end of the queue.
    - remove(): Removes and returns the first element in the queue.
    - print(): Prints all the elements in the queue.
    """

    def __init__(self, name):
        self.head = None
        self.tail = None
        self.name = name

    def add(self, pcb):
        pcb.status = self.name
        if self.head == None:
            self.head = pcb
            self.tail = pcb
            pcb.next = None
        else:
            self.tail.next = pcb
            self.tail = pcb

    def remove(self):
        if self.head == None:
            return None
        else:
            pcb = self.head
            self.head = self.head.next
            pcb.next = None
            return pcb

    def print(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.title = self.name
        table.add_column("Status", style="cyan")
        table.add_column("PID", style="cyan")
        table.add_column("Arrival", justify="right", style="green")
        table.add_column("Burst", justify="right", style="green")
        table.add_column("Total", justify="right", style="green")
        table.add_column("Current", justify="right", style="green")
        table.add_column("Wall Time", justify="right", style="green")

        pcb = self.head
        while pcb != None:
            table.add_row(pcb.status, str(pcb.pid), str(pcb.arrival_time), str(
                pcb.burst_time), str(pcb.total_time), str(pcb.run_time), str(pcb.wall_time))
            pcb = pcb.next
        console.print(table)

class Clock:
    """
    A class representing a clock that can be incremented and observed by registered objects.
    """
    def __init__(self):
        self.watchers = []
        self.time = 0

    def increment(self):
        self.time += 1
        for obj in self.watchers:
            obj.update(self.time)

    def get_time(self):
        return self.time

    def register_object(self, obj):
        self.watchers.append(obj)

    def unregister_object(self, obj):
        self.watchers.remove(obj)


class Scheduler:
    def __init__(self):
        self.new_queue = Queue("New")
        self.ready_queue = Queue("Ready Queue")
        self.waiting_queue = Queue("Waiting Queue")
        self.terminated_queue = Queue("Terminated")
        self.running = Queue("Running")

    def all_processes_done(self):
        """
        Returns True if all processes are done, False otherwise.
        """
        return self.running.head == None and self.new_queue.head == None and self.ready_queue.head == None and self.waiting_queue.head == None

    def update(self, time):
        # while there are still pcbs on new queue, remove them from new queue and add them to ready queue
        while self.new_queue.head != None:
            pcb = self.new_queue.remove()
            self.ready_queue.add(pcb)
        # if there is a running process, check if it is done
        if self.running.head is not None and self.running.head.run_time == self.running.head.total_time:
            # if it is done, add it to the terminated queue and set running to None
            self.terminated_queue.add(self.running.remove())
        # if there is no running process, remove the first process from the ready queue and run it
        if self.running.head == None and self.ready_queue.head != None:
            self.running.add(self.ready_queue.remove())
        # if there is a running process, increment its time
        if self.running.head is not None:
            self.running.head.run_time += 1


class Simulation:
    def __init__(self):
        self.sched = Scheduler()
        self.clock = Clock()
        self.clock.register_object(self.sched)

    def print_status(self):
        """
        Prints the current status of the operating system representing the terminated queue.
        """
        console = Console()
        console.clear()
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Operating System Status"
        table.add_column("", style="cyan")
        table.add_column("Value", justify="right", style="green")
        table.add_row("Time", str(self.clock.get_time()))
        console.print(table)
        self.sched.running.print()
        self.sched.ready_queue.print()
        self.sched.waiting_queue.print()
        self.sched.terminated_queue.print()
        self.sched.new_queue.print()

    # Function to ead the json file

    def import_json_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            allowed = {'sched_algorithm', 'time_slice', 'number_of_processes',
                       'arrival_time', 'burst_time', 'total_time'}
            if not all(key in allowed for key in data.keys()):
                print("Error: Invalid JSON file")
                exit()

    # loop for as mamny processes as specified in the json file
            for i in range(data['number_of_processes']):
                pid = i + 1
                arrival_time = random.randint(
                    data['arrival_time']['from'], data['arrival_time']['to'])
                burst_time = random.randint(
                    data['burst_time']['from'], data['burst_time']['to'])
                total_time = random.randint(
                    data['total_time']['from'], data['burst_time']['to'])
                pcb = PCB(pid, arrival_time, burst_time, total_time)
                self.sched.new_queue.add(pcb)
                self.clock.register_object(pcb)

    def run(self):
        # import the json file
        self.import_json_file("processes.json")
        while (not self.sched.all_processes_done()):
            response = input("[n(ext),s(top): ")
            if response == 's':
                break
            elif response == 'n':
                self.clock.increment()
                self.print_status()
            else:
                print("Invalid response. Try again.")


if __name__ == "__main__":
    s = Simulation()
    s.run()
