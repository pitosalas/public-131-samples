package cosi131;

public class BoundedBuffer {
	
	private static final int SIZE = 10;//maximum # items in buffer
	public int count;  			//# items in buffer
	private int in;				//index of next free position
	private int out;			//index of next full position
	private String [] buffer;	//buffer array

	public BoundedBuffer(){
		// buffer is initially empty
		count = 0;
		in = 0;
		out = 0;
		buffer = new String [SIZE];
	}

	void insert (String item){
		while (count == SIZE) Thread.yield(); //do nothing – no free position

		// add item to buffer
		count ++;
		buffer[in] = item;
		in = (in + 1) % SIZE;
	}

	public String remove () {
		String item;
		while (count == 0) Thread.yield();
		
		//remove item from buffer
		--count;
		item = buffer[out];
		out = (out + 1) % SIZE;
		return item;
	}


	public static void main(String[] args) {
		BoundedBuffer buf = new BoundedBuffer();
		Consumer cons = new Consumer(buf);
		Producer prod = new Producer(buf);
		Thread consThread = new Thread(cons);
		Thread prodThread = new Thread(prod);
		consThread.start();
		prodThread.start();
	}

}
