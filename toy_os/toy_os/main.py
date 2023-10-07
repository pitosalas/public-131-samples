# The toy operating system will demonstrate different scheduling algorithms.
from simulation import Simulation

DOC = """
# Important definitions:

* Simulation variables:
    * Time: Simulation time. Measured in 'tics'. Starts at zero.

* Each process is configured initially with
    * A burst pattern shows the process's state at each tic ("burst_pattern"
        * New: The process has not yet arrived to the scheduler
        * Ready: The process is ready to run
        * Wait: The process is waiting for I/O or other resources
        * Terminated: The process has completed
    * Alternatively a process can be configured with a burst time and total time ("burst" and "total")
        * Total Time: Number of tics the process will run before it terminates
        * Arrival Time: When the process arrives to the scheduler for the first time
    * Alternatively we can probabilistically generate processes using:
        * Burst time: Average number of tics a process will run ("burst")

* Once the simulation starts, each process tracks the following
    * Run Time: Number of CPU tics the process has used so far ("run")
    * Wall Time: Number of tics since the process was first run until it terminates ("wall")
    * Wait Time: Total tics a process spends waiting (on ready and wait queues) ("wait)
    * Start Time: Time(tics) when the process was first run ("start")

* When the simulation completes the following are calculated:
* Throughput: Average number of processes completed per tic
* Turnaround: Average number of tics used for a process (1/Througput)
"""

if __name__ == "__main__":
    s = Simulation()
    //s.run()
    s.run_animated()
