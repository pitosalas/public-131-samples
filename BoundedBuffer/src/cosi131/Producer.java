package cosi131;

public class Producer implements Runnable {
	BoundedBuffer buf;
	Producer(BoundedBuffer theBuffer) {
		buf = theBuffer;
	}

	public void run() {
		System.out.println("Producer ready.");
		for (int i = 0; i<20; i++) {
			try {
				Thread.sleep(0);
				String bagel = "Bagel: " + i;
				System.out.println("... produced: " + bagel);
				buf.insert(bagel);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	

}
