package cosi131;

import java.util.Random;

class Producer implements Runnable {
	private Pipe pipe;

	public Producer(Pipe m) {
		pipe = m;
	}

	public void run() {
		Integer widgetNumber = 0;
		for (int i=0; i<500; i++) {
			
			try {
				Thread.sleep(0);

				// produce new item for buffer
				String widget = "Widget " + widgetNumber++;
				System.out.println("Produced: " + widget);

				// enter into buffer
				pipe.send(widget);
			} catch (InterruptedException e) {
				System.out.println("Exception in Producer");
				e.printStackTrace();
			}
		}
		while (!pipe.empty())
			//System.out.println("Busy waiting...");
			Thread.yield();
		pipe.close();
	}
}
