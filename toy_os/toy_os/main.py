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
        self.time = 0
        self.next = None

    def __str__(self):
    

        return "PID: " + str(self.pid) + " Arrival Time: " + str(self.arrival_time) + " Burst Time: " + str(self.burst_time) + " Total Time: " + str(self.total_time)



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
        if self.head == None:
            self.head = pcb
            self.tail = pcb
        else:
            self.tail.next = pcb
            self.tail = pcb

    def remove(self):
        if self.head == None:
            return None
        else:
            pcb = self.head
            self.head = self.head.next
            return pcb

    def print(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.title = self.name
        table.add_column("PID", style="cyan")
        table.add_column("Arrival", justify="right", style="green") 
        table.add_column("Burst", justify="right", style="green") 
        table.add_column("Total", justify="right", style="green") 
        table.add_column("Current", justify="right", style="green") 

        pcb = self.head
        while pcb != None:
            table.add_row(str(pcb.pid), str(pcb.arrival_time), str(pcb.burst_time), str(pcb.total_time), str(pcb.time))
            pcb = pcb.next
        console.print(table)

# I clock class will control the simulation time. It will have a method to increment the
# time. That incrementing of the time will be communicated to all PCBs and classes so they
# can maintain their state. Whenever a new object is created that needs to be aware of the time,
# it registers itself with the clock object


class Clock:
    def __init__(self):
        self.time = 0

    def increment(self):
        self.time += 1

    def get_time(self):
        return self.time

    def register_object(self, obj):
        obj.clock = self

class Simulation:
    def __init__(self):
        print("contructor")
        self.clock = Clock()
        self.new_queue = Queue("New Queue")
        self.ready_queue = Queue("Ready Queue")
        self.waiting_queue = Queue("Waiting Queue")
        self.terminated_queue = Queue("Terminated Queue")

    def print_status(self):
        """
        Prints the current status of the operating system representing the terminated queue.
        """
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Operating System Status"
        table.add_column("Variable", style="cyan")
        table.add_column("Value", justify="right", style="green") 
        table.add_row("Time", str(self.clock.get_time()))
        console.print(table)
        self.new_queue.print()
        self.ready_queue.print()
        self.waiting_queue.print()
        self.terminated_queue.print()
        

    # Function to ead the json file
    def import_json_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            allowed = {'sched_algorithm', 'time_slice', 'number_of_processes',
                        'arrival_time', 'burst_time', 'total_time'}
            if not all(key in allowed for key in data.keys()):
                print("Error: Invalid JSON file")
                return
   
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
                self.new_queue.add(pcb)
                self.clock.register_object(pcb)

    def run(self):
        # import the json file
        self.import_json_file("processes.json")
        self.print_status()


if __name__ == "__main__":
    s = Simulation()
    s.run()
