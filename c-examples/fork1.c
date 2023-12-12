#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>


int main()
{
    char   buf[100];
    sprintf(buf, "Starting... \n");
    write(1, buf, strlen(buf));

    int pid = fork();
    if (pid == 0)
    {
        // Child Only
        sprintf(buf, ">>> (pid: %o) I am child process\n", getpid());
        write(1, buf, strlen(buf));
        exit(0);
    }
    else
    {
        // Parent only
        sprintf(buf, "(pid: %o) I am parent process. The new child is pid %o\n", getpid(), pid);
        write(1, buf, strlen(buf));

    }
    wait(NULL);
    sprintf(buf, "(pid: %o) I know that the child has completed.\n", getpid());
    write(1, buf, strlen(buf));

    exit(0);
}