package cosi131;

public class Consumer implements Runnable {
	BoundedBuffer buf;

	Consumer(BoundedBuffer theBuffer) {
		buf = theBuffer;
	}

	@Override
	public void run() {
		System.out.println("Consumer ready.");
		for (int i = 0; i < 20; i++) {
			try {
				String s = buf.remove();
				System.out.println("... Consumed: " + s);
				Thread.sleep(10);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
	}


}
