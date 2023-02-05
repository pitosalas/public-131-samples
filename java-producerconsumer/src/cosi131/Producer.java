package cosi131;

import java.util.Date;

class Producer implements Runnable {
	private Channel mbox;
	
	public Producer (Channel m) {mbox = m;}

	public void run() {
		Date message;
		while (true) {
			//nap for random time
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		 	//produce new item for buffer 
			message = new Date ();	
		   	System.out.println ("Producer produces" + message);
		   	
			//enter into buffer
			mbox.send (message);
		}
	}
}
