package cosi131;

public class Consumer implements Runnable {
	BoundedBuffer buf;

	Consumer(BoundedBuffer theBuffer) {
		buf = theBuffer;
	}

	@Override
	public void run() {
		System.out.println("Consumer ready.");
		for (int i = 0; i < BoundedBuffer.HOW_MANY; i++) {
				try {
					String s = buf.remove();
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
		}
		
	}


}
