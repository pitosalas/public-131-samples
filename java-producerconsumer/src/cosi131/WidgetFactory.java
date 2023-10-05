package cosi131;

public class WidgetFactory {
	public WidgetFactory() {
		// create message buffer
		Pipe pipe = new Pipe();

		// create producer, consumer threads
		Thread producerThread1 = new Thread(new Producer(pipe));
		Thread consumerThread = new Thread(new Consumer(pipe));
		Thread producerThread2 = new Thread(new Producer(pipe));

		producerThread1.start();
		producerThread2.start();
		consumerThread.start();
		
		try {
			consumerThread.join();
			producerThread1.join();
			producerThread2.join();

		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println("Exiting top level process!");
		System.exit(0);
	}

	public static void main(String args[]) {
		WidgetFactory f = new WidgetFactory();
	}
}
