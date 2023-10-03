from queue import Queue

class Scheduler:
    def __init__(self, simulation):
        self.new_queue = Queue("New", simulation)
        self.ready_queue = Queue("Ready Queue", simulation)
        self.waiting_queue = Queue("Waiting Queue", simulation)
        self.terminated_queue = Queue("Terminated", simulation)
        self.running = Queue("Running", simulation)
        self.simulation = simulation
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
        self.clock = self.simulation.clock
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

