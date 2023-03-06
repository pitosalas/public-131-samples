package cosi131;

// Thread 1
class Thread_A extends Thread {
	
// Here, the first thread Thread_A has been created
// and extended from the Thread class. The run() function is executed when
// a thread is invoked, which calls the displayCounting() to print numbers.
	
    Count c;
    Thread_A(Count c) {
        this.c = c;
    }
    public void run() {
        c.displayCounting(5, "Thread A", 300);
    }
}
