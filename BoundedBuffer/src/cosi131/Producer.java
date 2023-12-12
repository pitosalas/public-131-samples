package cosi131;

public class Producer implements Runnable {
	BoundedBuffer buf;
	Producer(BoundedBuffer theBuffer) {
		buf = theBuffer;
	}

	public void run() {
		System.out.println("Producer ready.");
		for (int i = 0; i< BoundedBuffer.HOW_MANY; i++) {
				String bagel = "Bagel: " + i;
				try {
					buf.insert(bagel);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
		}
	}
	

}
