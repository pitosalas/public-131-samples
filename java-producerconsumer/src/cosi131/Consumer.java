package cosi131;

import java.util.Random;

class Consumer implements Runnable {
	private Channel mbox;
	
	public Consumer (Channel m) { mbox = m; }
	
	public void run() {
		String widgetName;
		while (true) {
			
			// nap for a random time
			Random r = new Random();
			try {
				Thread.sleep(r.nextInt(200,2000));
				
			// Pick up waiting message, if any
				widgetName = (String) mbox.receive();
				if (widgetName != null) {
					System.out.println("Consumed: " + widgetName);
				}
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
}