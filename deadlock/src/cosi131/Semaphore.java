package cosi131;

public class Semaphore {
	private volatile int permits;

	Semaphore(int count) {
		this.permits = count;
	}

	public Semaphore() {
		this(1);
	}

	synchronized void acquire() throws InterruptedException {
		while (this.permits <= 0) {
			wait();
		}
		this.permits--;

	}

	synchronized void release() {
		this.permits++;
		notify();
	}
}
