package cosi131;

public class Runnable2 implements Runnable {
	Count2 counter;
	String name;

	public Runnable2(String n, Count2 c) {
		counter = c;
		name = n;
	}

	@Override
	public void run() {
		for (int i = 1; i <= 1000; i++) {
			counter.increment(name);
		}
	}
}
