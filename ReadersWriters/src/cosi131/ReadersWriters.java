package cosi131;

public class ReadersWriters {

	public static void main(String[] args) {
		RWLock rwLock = new RWLock();
		Thread r1 = new Thread(new AReader(1, rwLock));
		Thread r2 = new Thread(new AReader(2, rwLock));
		Thread r3 = new Thread(new AReader(3, rwLock));
		Thread w3 = new Thread(new AWriter(1, rwLock));
		Thread w2 = new Thread(new AWriter(2, rwLock));
		
		Thread w1 = new Thread(new AWriter(0, rwLock));
		
		r1.start();
		r2.start();
		r3.start();
		w2.start();
		w3.start();

		w1.start();
		

	}

}
