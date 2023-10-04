import time

from rich.live import Live
from rich.table import Table
from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

table1 = Table()
table1.add_column("Row ID")
table1.add_column("Description")
table1.add_column("Level")

table2 = Text(f"Algorithm: xxx", style="bold red")
table0 = Text(f"Algorithm: xxx", style="bold red")
table3 = Text(f"Algorithm: xxx", style="bold red")

rg = Group(table2, table0, table3)

table_group = Group(rg, table1)


with Live(table_group, refresh_per_second=4):  # update 4 times a second to feel fluid
    for row in range(12):
        time.sleep(0.4)  # arbitrary delay
        # update the renderable internally
        table1.add_row(f"{row}", f"description {row}", "[red]ERROR")
