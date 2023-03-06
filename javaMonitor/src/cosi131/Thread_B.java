package cosi131;

class Thread_B extends Thread {
	
// This is the second thread named Thread_B, similar to the first thread. 
// The run() function is also calling the displayCounting() to print numbers.
	Count c;

	Thread_B(Count c) {
		this.c = c;
	}

	public void run() {
        c.displayCounting(5, "Thread B", 100);
	}
}
