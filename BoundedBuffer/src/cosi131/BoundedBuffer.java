package cosi131;

public class BoundedBuffer {

	private static final int SIZE = 10;// maximum # items in buffer
	public int count; // # items in buffer
	private int in; // index of next free position
	private int out; // index of next full position
	private String[] buffer; // buffer array

	public BoundedBuffer() {
		// buffer is initially empty
		count = 0;
		in = 0;
		out = 0;
		buffer = new String[SIZE];
	}

	void insert(String item) {
		while (count == SIZE) {
			try {
//				Thread.sleep(0);
//				System.out.println("... buf full ... busy wait");
//				Thread.yield();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		System.out.printf("... Adding to buffer. Current count: %d\n", count);

		// add item to buffer
		count++;
		buffer[in] = item;
		in = (in + 1) % SIZE;
	}

	public String remove() {
		String item;
		while (count == 0) {
			try {
//				System.out.println("... buf empty ... busy wait");
//				Thread.sleep(0);
//				Thread.yield();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}

		// remove item from buffer
		--count;
		item = buffer[out];
		out = (out + 1) % SIZE;
		return item;
	}

	public static void main(String[] args) {
		BoundedBuffer buf = new BoundedBuffer();
		Consumer cons = new Consumer(buf);
		Producer prod = new Producer(buf);
		Thread consThread = new Thread(cons);
		Thread prodThread = new Thread(prod);
		consThread.start();
		prodThread.start();

		try {
			consThread.join();
			prodThread.join();

		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println("Exiting top level process!");
		System.exit(0);
	}

}
