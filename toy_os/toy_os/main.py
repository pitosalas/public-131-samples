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
    
    def __repr__(self):
        return f"PCB({self.pid}, {self.arrival_time}, {self.burst_time}, {self.total_time})"


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
                pcb.burst_time), str(pcb.total_time), str(pcb.run_time), str(pcb.wall_time))
            pcb = pcb.next
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
            print(obj)
            obj.update(self.time)

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

    def all_processes_done(self):
        """
        Returns True if all processes are done, False otherwise.
        """
        return self.running.head == None and self.new_queue.head == None and self.ready_queue.head == None and self.waiting_queue.head == None

    def move_from_ready(self):
        # while there are still pcbs on new queue, remove them from new queue and add them to ready queue

        for pcb in self.new_queue._list:
            if pcb.arrival_time <= self.clock.get_time():
                self.new_queue.remove(pcb)
                self.ready_queue.add_at_end(pcb)

    def handle_done(self):
        # if there is a running process, check if it is done
        current_process = self.running.head
        if current_process is not None and current_process.run_time >= current_process.total_time:
        # if it is done, add it to the terminated queue and set running to None
            self.terminated_queue.add_at_end(self.running.remove(current_process))

    def schedule_next(self):
        # Return if no one to run
        if not self.running.empty() or self.ready_queue.empty():
            return
        process_to_run = self.ready_queue.remove_from_front()
        self.running.add_at_end(process_to_run)

    def update_running_process(self):
        # if there is a running process, increment its time
        if self.running.head is not None:
            self.running.head.run_time += 1

    def update(self, time):
        self.move_from_ready()
        self.handle_done()
        self.schedule_next()
        self.update_running_process()

    def __repr__(self):
        return "Scheduler({clock} )"

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
        console.clear()
        console.print(f"Clock: {self.clock.get_time()}", style="bold red")
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Operating System Status"
        table.add_column("Status", style="cyan")
        table.add_column("PID", style="cyan")
        table.add_column("Arrival", justify="right", style="green")
        table.add_column("Burst", justify="right", style="green")
        table.add_column("Total", justify="right", style="green")
        table.add_column("Current", justify="right", style="green")
        table.add_column("Wall Time", justify="right", style="green")

        self.sched.running.print(table)
        self.sched.ready_queue.print(table)
        self.sched.waiting_queue.print(table)
        self.sched.terminated_queue.print(table)
        self.sched.new_queue.print(table)
        console.print(table)

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
                    data['total_time']['from'], data['total_time']['to'])
                pcb = PCB(pid, arrival_time, burst_time, total_time)
                self.sched.new_queue.add_at_end(pcb)
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
