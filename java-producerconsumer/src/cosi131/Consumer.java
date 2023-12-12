package cosi131;

import java.util.Random;

class Consumer implements Runnable {
	private Pipe pipe;
	private int counter;

	public Consumer(Pipe m) {
		pipe = m;
		counter = 0;
	}

	public void run() {
		String widgetName;
		while (!pipe.empty()) {
			try {
				Thread.sleep(0);

				// Pick up waiting message, if any
				widgetName = (String) pipe.receive();
				if (widgetName != null) {
					System.out.println("Consumed: " + widgetName);
					counter +=1;
				}
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				System.out.println("Exception in Consumer");
				e.printStackTrace();
			}
		}
//		System.out.printf("Consumed a total of %d widgets\n", counter);
	}
}