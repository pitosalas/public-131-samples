package cosi131;

public class Consumer implements Runnable {
	BoundedBuffer buf;

	Consumer(BoundedBuffer theBuffer) {
		buf = theBuffer;
	}

	@Override
	public void run() {
		System.out.println("Consumer ready.");
		for (int i = 0; i < 10; i++) {
			String s = buf.remove();
			System.out.println("- Yummy: " + s);
		}
		
	}


}
