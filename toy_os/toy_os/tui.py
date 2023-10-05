from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from rich.live import Live
from rich import box


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


def gemerate_status_rg(sim):
    """
    Prints the current status of the operating system representing the terminated queue.
    """
    line1 = Text(f"Clock: {sim.clock.get_time()}", style="bold red")
    line2 = Text(f"Timeline: {sim.sched.progress}", style="bold red")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Status!", style="red")
    table.add_column("PID", style="cyan")
    table.add_column("Run Time\n(CPU consumed so far)",
                     justify="right", style="green")
    if sim.format == "full":
        table.add_column(
            "Wall Time\n(Elapsed time since first starting)", justify="right", style="green")
    table.add_column("Wait Time\n(Wating time until started)",
                     justify="right", style="green")
    if sim.format == "full":
        table.add_column(
            "Waiting Time\n(Time spent waiting overall)", justify="right", style="green")

    sim.sched.running.print(table)
    sim.sched.ready_queue.print(table)
    sim.sched.waiting_queue.print(table)
    sim.sched.terminated_queue.print(table)
    sim.sched.new_queue.print(table)
    return Group(line1, line2, table)


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
    status_rg = gemerate_status_rg(sim)
    summary_rg = generate_summary_rg(sim)
    return Group(sim.intro_rg, status_rg, summary_rg)
