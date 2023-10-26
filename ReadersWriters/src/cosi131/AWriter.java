package cosi131;

public class AWriter implements Runnable {
	
	private RWLock theRWLock;
	private int ident;

	AWriter(int ident, RWLock theRWLock) {
		this.theRWLock = theRWLock;
		this.ident = ident;
	}
	
	@Override
	public void run() {
		for (int i=0; i<25; i++) {
			try {
				System.out.printf("...W%d wants to write %d\n", ident, i);
				theRWLock.startWrite();
				System.out.printf("...W%d writing %d!\n", ident, i);
				Thread.sleep(700);
				theRWLock.doneWrite();
				System.out.printf("...W%d Done Writing %d\n", ident, i);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
}
