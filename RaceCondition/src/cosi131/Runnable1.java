package cosi131;

public class Runnable1 implements Runnable {
	Count1 counter;

	public Runnable1(Count1 c) {
		counter = c;
	}

	@Override
	public void run() {
		for (int i = 1; i <= 1000; i++) {
			counter.increment();
		}
	}
}
