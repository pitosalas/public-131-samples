class Queue:
    def __init__(self, name: str, simulation):
        self.name = name
        self.simulation = simulation
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
            format = self.simulation.format
            if format == "full":
                table.add_row(pcb.status, str(pcb.pid), str(
                    pcb.run_time), str(pcb.wall_time), str(pcb.start_time), str(pcb.wait_time))
            elif format == "basic":
                table.add_row(pcb.status, str(pcb.pid), str(
                    pcb.run_time), str(pcb.start_time))
