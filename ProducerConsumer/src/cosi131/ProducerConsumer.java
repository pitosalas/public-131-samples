package cosi131;

class ProducerConsumer
{
	// used to create two threads & test an algorithm

	public static void main (String args[])  {

		// Mutex alg = new SA ();
		// Mutex alg = new AY();
		Mutex alg = new PE();
		
		Thread one = new Thread (new Worker ("Thread A", 0, alg));
		Thread two = new Thread (new Worker ("Thread B", 1, alg));

		one.start();
		two.start();
	}

}
