#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>

char buf[100];      // For printing
char buffer[100];  // Pipe Message
int pipe_info[2]; // Used to store two ends of first pipe

void l(char *msg) {
    sprintf(buf, "%s (pinf: %d, %d)\n", msg, pipe_info[0], pipe_info[1]);
    write(1, buf, strlen(buf));
}

void producer(int pipe_info[])
{
    l("producer...");
    write(pipe_info[1], "hello", 5);
    sprintf(buf, "** Producer sent: %s\n", "hello");
    write(1, buf, strlen(buf));
}

void consumer(int pipe_info[])
{
    l("consumer...");
    read(pipe_info[0], buffer, 100);
    sprintf(buf, "** Consumer received: %s\n", buffer);
    write(1, buf, strlen(buf));
}

int main()
{
    l("starting...");

    pipe(pipe_info);  // Creates a new pipe.  File descriptors for the two ends of the pipe are placed in pipefd.

    l("Pipe is built");

    int pid1 = fork();
    if (pid1 == 0)
    {
        // In Child 1, which will be the consumer
        consumer(pipe_info);
        exit(0);
    }
    else
    {
        // Still in parent process
        int pid2 = fork();
        sprintf(buf, "else: pids: %d %d\n", pid1, pid2);
        write(1, buf, strlen(buf));
        if (pid2 == 0)
        {
            // In Child 2, which will be the producer
            producer(pipe_info);
            exit(0);
        }
    }
    // Parent
    l("parent waiting...");

    wait(NULL);
    l("parent done waiting, exiting...");
    exit(0);
}

