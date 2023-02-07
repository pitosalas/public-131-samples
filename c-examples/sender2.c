#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdlib.h>
#include <string.h>
#include "queue.h"

void report_and_exit(const char* msg) {
  printf("%s", msg);
  exit(0);
}

int main() {
  key_t key = ftok(PathName, ProjectId);
  if (key < 0) report_and_exit("couldn't get key...");

  int qid = msgget(key, 0666 | IPC_CREAT);
  if (qid < 0) report_and_exit("couldn't get queue id...");

    char str[64];
    printf("Type your message\n");
    while (fgets(str, sizeof str, stdin) != NULL) {
      int len = strlen(str);
      if( str[len-1] == '\n' )
        str[len-1] = 0;

      queuedMessage msg;
      msg.type = 1;
      strcpy(msg.payload, str);
      msgsnd(qid, &msg, sizeof(msg), IPC_NOWAIT);
      printf("'%s' sent\n", msg.payload);
    }
  return 0;
}