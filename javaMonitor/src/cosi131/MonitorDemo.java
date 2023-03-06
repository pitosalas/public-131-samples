package cosi131;

public class MonitorDemo {
	public static void main(String args[]) {

// These lines cover the main function. Objects of Thread_A and Thread_B
// are created, and both threads are started. Both threads will call the
// synchronized function displayCounting() in parallel, but here is where the
// monitor comes into play. When the first thread executes the function, the 
// monitor will block the second thread till the completion of the first thread.
// It will then be allowed to execute.

		Count obj = new Count();
		Thread_A t1 = new Thread_A(obj);
		Thread_B t2 = new Thread_B(obj);
		t1.start();
		t2.start();
	}
}