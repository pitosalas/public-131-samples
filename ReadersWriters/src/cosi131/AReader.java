package cosi131;

public class AReader implements Runnable {
	
	private RWLock theRWLock;
	private int ident;

	AReader(int ident, RWLock theRWLock) {
		this.theRWLock = theRWLock;
		this.ident = ident;
	}
	
	

	@Override
	public void run() {
		for (int i=0; i<25; i++) {
			try {
				System.out.printf("..............................R%d wants to read %d\n", ident, i);
				theRWLock.startRead();
				System.out.printf("..............................R%d reading %d\n", ident, i);
				Thread.sleep(100);
				theRWLock.doneRead();
				System.out.printf("..............................R%d Done Reading %d\n", ident, i);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
}
