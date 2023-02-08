package cosi131;

import java.util.Random;

class Producer implements Runnable {
	private Channel mbox;

	public Producer(Channel m) {
		mbox = m;
	}

	public void run() {
		Integer widgetNumber = 0;
		for (int i=0; i<100; i++) {
			
			// nap for a random time
			Random r = new Random();
			try {
				Thread.sleep(r.nextInt(100, 200));

				// produce new item for buffer
				String widget = "Widget " + widgetNumber++;
				System.out.println("Produced: " + widget);

				// enter into buffer
				mbox.send(widget);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
}
