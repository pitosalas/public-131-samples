package cosi131;
import java.util.Date;

class Consumer implements Runnable {
	private Channel mbox;
	public Consumer (Channel m) {mbox = m;}

	public void run() {
		Date message;
		while (true) {

			//nap for random time
			Thread.CurrentThread(;

			// Pick up awaiting message if any
			message = (Date) mbox.receive();
			if (message != NULL)
			   System.out.println (“Consumer consumed” + message);
		}	
	}
}
