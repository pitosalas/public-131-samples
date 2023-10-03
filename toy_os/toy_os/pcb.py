class PCB:
    """
    Process Control Block (PCB) class represents a process in the operating system.
    It contains information about the process such as its process ID (pid), arrival time,
    burst time, priority, and completion time.
    """

    def __init__(self, pid: str, arrival_time: int, burst_time: int, total_time: int):
        self.pid: str = pid
        self.arrival_time: int = arrival_time
        self.burst_time = burst_time
        self.total_time = total_time
        self.run_time = 0
        self.wall_time = None
        self.start_time = None
        self.wait_time = 0
        self.status = "New"

    def update(self, time: int):
        if self.status not in ("New", "Terminated"):
            self.wall_time = time

    def __repr__(self):
        return f"PCB({self.pid}, {self.arrival_time}, {self.burst_time}, {self.total_time}, {self.wait_time})"
