package cosi131;

public class CounterRunnable implements Runnable {
	Counter counter;
	String name;

	public CounterRunnable(String n, Counter c) {
		counter = c;
		name = n;
	}

	@Override
	public void run() {
		for (int i = 0; i < 1000; i++) {
			counter.increment(name);
		}
	}
}
