package cosi131;

import java.util.concurrent.locks.*;

public class RWLock {
// Synchronization Variables
	private final Lock myLock = new ReentrantLock();
	private final Condition readGo = myLock.newCondition();
	private final Condition writeGo = myLock.newCondition();

	private int activeReaders = 0;
	private int activeWriters = 0;
	private int waitingReaders = 0;
	private int waitingWriters = 0;

	// Here is where the policy is set
	private Boolean readShouldWait() {
		return (activeWriters > 1 || waitingWriters > 0);
	}

	private Boolean writeShouldWait() {
		return (activeWriters > 0 || activeReaders > 0);
	}

	// And here are the semaphores
	public void startRead() throws InterruptedException {
		myLock.lock();
		try {
			waitingReaders++;
			while (readShouldWait()) {
				readGo.await();
			}
			waitingReaders--;
			activeReaders++;
		} finally {
			myLock.unlock();
		}
	}

	public void doneRead() {
		myLock.lock();
		try {
			activeReaders--;
			if (activeReaders == 0 && waitingWriters > 0) {
				writeGo.signal();
			}
		} finally {
			myLock.unlock();
		}
	}

	public void startWrite() throws InterruptedException {
		myLock.lock();
		try {
			waitingWriters++;
			while (writeShouldWait()) {
				writeGo.await();
			}
			waitingWriters--;
			activeWriters++;
		} finally {
			myLock.unlock();
		}
	}

	public void doneWrite() {
		myLock.lock();
		try {
			activeWriters--;
			assert activeWriters == 0;
			if (waitingWriters > 0) {
				writeGo.signal();
			} else {
				readGo.signalAll();
			}
		} finally {
			myLock.unlock();
		}
	}
}
