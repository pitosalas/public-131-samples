package cosi131;

public class Factory
{
	public Factory() {
		//create message buffer
		Channel mailBox = new Channel();

		//create producer, consumer threads
		Thread pThread = new Thread (new Producer(mailbox));
		Thread cThread = new Thread (new Consumer(mailbox));
		pThread.start();
		cThread.start();
	}

	public static void main (String args[]){
		Factory f = new Factory();
	}
}
