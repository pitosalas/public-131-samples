#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>

unsigned long buffer[100]; // Pipe Message
int mypipe[2];   // Used to store two ends of first pipe

void l(char *msg)
{
    char buf[100];   // For printing
    sprintf(buf, "%s\n", msg);
    write(1, buf, strlen(buf));
}

unsigned long factorial(unsigned long n)
{
    if (n == 0)
    {
        return 1;
    }
    return n * factorial(n - 1);
}

void worker(int jobs[], int njobs, int pipe)
{
    l("Worker starts...");
    // iterate over jobs
    for (int i = 0; i < njobs; i++)
    {
        unsigned long f[1];
        f[0] = factorial(jobs[i]);
        write(pipe, f, 8);
    }
}

int main()
{
    l("starting...");
    pipe(mypipe); // Creates a new pipe.  File descriptors for the two ends of the pipe are placed in pipefd.

    int pid1 = fork();
    if (pid1 == 0)
    {
        int arg1[] = {12, 19, 11, 15, 17, 20};
        worker(arg1, 6, mypipe[1]);
        exit(0);
    }
    else
    {
        // Still in parent process
        int pid2 = fork();
        if (pid2 == 0)
        {
            // In Child 2, which will be the producer
            int arg2[] = {20, 18, 12, 19, 18, 13};
            worker(arg2, 6, mypipe[1]);
            exit(0);
        }
    }
    // Parent
    l("parent waiting...");
    for (int i = 0; i < 12; i++) {
        int n = read(mypipe[0], buffer, 8);
        char buf[100];      // For printing
        sprintf(buf, "Parent received: %lu", buffer[0]);
        l(buf);
    }

    wait(NULL);
    l("parent done, exiting...");
    exit(0);
}
