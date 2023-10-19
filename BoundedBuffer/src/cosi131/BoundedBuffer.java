package cosi131;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

public class BoundedBuffer {
	public static final int HOW_MANY = 2000;// maximum # items in buffer

	private static final int SIZE = 10;// maximum # items in buffer
	public int count; // # items in buffer
	private int in; // index of next free position
	private int out; // index of next full position
	public String[] buffer; // buffer array
	private ReentrantLock myLock;
	private Condition cvNoLongerEmpty;
	private Condition cvNoLongerFull;

	public BoundedBuffer() {
		// buffer is initially empty
		count = 0;
		in = 0;
		out = 0;
		buffer = new String[SIZE];
		myLock = new ReentrantLock();
		cvNoLongerEmpty = myLock.newCondition();
		cvNoLongerFull = myLock.newCondition();
	}

	void insert(String item) throws InterruptedException {
		myLock.lock();
		checkValid();
		try {
			while (count == SIZE) cvNoLongerFull.await();

			// add item to buffer
			count++;
			buffer[in] = item;
			in = (in + 1) % SIZE;
			cvNoLongerEmpty.signalAll();
		} finally {
			myLock.unlock();
		}

	}

	public String remove() throws InterruptedException {
		String item = "";
		myLock.lock();
		checkValid();
		try {

			while (count == 0) cvNoLongerEmpty.await();
			--count;
			item = buffer[out];
			out = (out + 1) % SIZE;
			cvNoLongerFull.signalAll();
			return item;
		} finally {
			myLock.unlock();
		}

	}
	public void checkValid() {
		if (count == 0 && out == in) return;
		if (count == SIZE && out == in) return;
		if (count == (in - out + SIZE) % SIZE) return;
		System.out.printf("!!! In(%d)  Out(%d) Count(%d)\n", in, out, count);
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
			e.printStackTrace();
		}
		System.out.printf("At end buffer contains: %d entries\n", buf.count);
		System.out.println("Exiting top level process!");
		System.exit(0);
	}

}
