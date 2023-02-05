package cosi131;

public class WidgetFactory {
	public WidgetFactory() {
		// create message buffer
		Channel mailBox = new Channel();

		// create producer, consumer threads
		Thread producerThread = new Thread(new Producer(mailBox));
		Thread consumerThread = new Thread(new Consumer(mailBox));

		producerThread.start();
		consumerThread.start();
	}

	public static void main(String args[]) {
		WidgetFactory f = new WidgetFactory();
	}
}
