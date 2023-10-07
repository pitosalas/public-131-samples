from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from rich.live import Live
from rich import box

# Mapping format strings to column headers

COLUMN_HEADERS = {
      "pid": "PID",
      "total_ime": "Total Time",
      "arrival_time": "Arrival Time",
      "burst_time": "Burst Time",
      "priority": "Priority",
      "start_time": "Start Time",
      "run_time": "Run Time",
      "wall_time": "Wall Time",
      "wait_time": "Wait Time",
      "status": "Status"
}

def generate_intro_rg(sim):
    line1 = Text(f"Algorithm: {sim.sched.print_name}", style="bold red")
    table = Table(show_header=True,
                  header_style="bold magenta", box=box.MINIMAL)
    table.add_column("PID", style="cyan", width=4)
    table.add_column(
        "Total Time\n(required by process)", justify="right", style="green")
    table.add_column(
        "Arrival Time\n(when process first arrives)", justify="right", style="green")
    table.add_column("Burst\n(average time of a CPU burst)",
                     justify="right")
    table.add_column("Priority\n(process priority",
                     justify="right")
    for pcb in sim.sched.new_queue._list:
        table.add_row(str(pcb.pid), str(pcb.arrival_time),
                      str(pcb.burst_time), str(pcb.total_time), str(pcb.priority))
    return Group(line1, table)

def print_status(sim) -> None:
    rg = generate_status_rg(sim)
    console = Console()
    console.print(rg)

def generate_status_rg(sim) -> Group:
    """
    Prints the current status of the operating system representing the terminated queue.
    """
    line1 = Text(f"Clock: {sim.clock.get_time()}", style="bold red")
    line2 = Text(f"Timeline: {sim.sched.progress}", style="bold red")
    table = Table(show_header=True, header_style="bold magenta")
    add_columns(table, sim.display["status"])
    add_rows(table, sim.sched.running, sim.display["status"])
    add_rows(table, sim.sched.ready_queue, sim.display["status"])
    add_rows(table, sim.sched.waiting_queue, sim.display["status"])
    add_rows(table, sim.sched.terminated_queue, sim.display["status"])
    add_rows(table, sim.sched.new_queue, sim.display["status"])
    return Group(line1, line2, table)

def add_rows(table, queue, columns):
    for pcb in queue._list:
        row = []
        for column in columns:
            value = getattr(pcb, column)
            row.append(str(value))
        table.add_row(*row)

def add_columns(table, columns):
    for column in columns:
        table.add_column(COLUMN_HEADERS[column], justify="right")


def print_summary(sim) -> None:
    rg = generate_summary_rg(sim)
    console = Console()
    console.print(rg)

def generate_summary_rg(sim):
    """
    Prints the summary of the operating system representing the terminated queue.
    """
    line1 = Text(f"Clock: {sim.clock.get_time()}", style="bold red")
    line2 = Text(
        f"Average Time spent Waiting: {sim.sched.get_average_wait_time()}", style="bold red")
    line3 = Text(
        f"Average waiting before starting: {sim.sched.get_average_start_time()}", style="bold red")
    return Group(line1, line2, line3)


def group_rg(sim):
    status_rg = generate_status_rg(sim)
    summary_rg = generate_summary_rg(sim)
    return Group(sim.intro_rg, status_rg, summary_rg)
