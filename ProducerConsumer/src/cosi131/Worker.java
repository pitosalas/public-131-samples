package cosi131;

public class Worker implements Runnable {

	private String name;
	private int id;
	private Mutex mutex;

	public Worker(String s, int i, Mutex m) {
		this.name = s;
		this.id = i;
		this.mutex = m;
		System.out.printf("Created worker %s with id=%d\n", s, i);
	}

	public void run() {
		while (true) {
			mutex.enterCS(id);
			
			System.out.printf("\n>>> Thread %s enters critical section. (%d)\n", name, id);

			doWork(id);

			System.out.printf("<<< Thread %s departs" + " critical section. (%d)\n", name, id);

			mutex.exitCS(id);
		}
	}

	private void doWork(int id) {
		System.out.printf("Doing work for thread: %s\n", name);
		try {
			if (id == 0)
				Thread.sleep(10);
			else
				Thread.sleep(10);
			System.in.read();
		} catch (Exception e) {
			e.printStackTrace();
		}
		
	}
}