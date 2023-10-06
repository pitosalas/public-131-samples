# The toy operating system will demonstrate different scheduling algorithms.
from simulation import Simulation

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
    * Start Time: Time(tics) when the process was first run

* When the simulation completes the following are calculated:
* Throughput: Average number of processes completed per tic
* Turnaround: Average number of tics used for a process (1/Througput)
"""

if __name__ == "__main__":
    s = Simulation()
    s.run()
#    s.run_animated()
