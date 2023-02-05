package cosi131;

import java.util.Random;

class Producer implements Runnable {
	private Channel mbox;

	public Producer(Channel m) {
		mbox = m;
	}

	public void run() {
		Integer widgetNumber = 0;
		while (true) {
			
			// nap for a random time
			Random r = new Random();
			try {
				Thread.sleep(r.nextInt(100, 2000));

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
