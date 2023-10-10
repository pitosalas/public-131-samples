package cosi131;

public class Worker implements Runnable {

	private String name;
	private int tread_id;
	private Mutex mutex;

	public Worker(int i, Mutex m) {
		this.tread_id = i;
		this.mutex = m;
		System.out.printf("Created worker id=%d\n", i);
	}

	public void run() {
		int limit = tread_id == 0 ? 20 : 40;
		int sleepy = tread_id == 0 ? 200 : 50;
		for (int cs_loop = 0; cs_loop < limit; cs_loop++) {
			try {
				Thread.sleep(sleepy);

				mutex.enterCS(tread_id);

				System.out.printf("++ Worker %d ENTERING critical section during loop: %d\n", tread_id, cs_loop);

				Thread.sleep(sleepy);

				mutex.exitCS(tread_id);

				Thread.sleep(sleepy);
				System.out.printf("++ Worker %d LEAVING critical section during loop: %d\n", tread_id, cs_loop);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

}