package cosi131;

import java.util.concurrent.locks.ReentrantLock;

public class Count1 {
	Integer counter;
	String turn;
	ReentrantLock lock = new ReentrantLock();
	
	Count1(int initial) {
		counter = initial;
	}
	
	 void increment() {
		lock.lock();
		counter = counter + 1;
		lock.unlock();
	}
	
	String turn() {
		return turn;
	}
	

	public String toString() {
		return counter.toString();
	}

}
