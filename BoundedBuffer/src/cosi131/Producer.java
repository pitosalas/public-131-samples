package cosi131;

public class Producer implements Runnable {
	BoundedBuffer buf;
	Producer(BoundedBuffer theBuffer) {
		buf = theBuffer;
	}

	public void run() {
		System.out.println("Producer ready.");
		for (int i = 0; i<10; i++) {
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			String bagel = "Bagel: " + i;
			System.out.println("+ Toasting: " + bagel);
			buf.insert(bagel);
		}
	}
	

}
