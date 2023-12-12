package cosi131;

public class BadChefRunnable implements Runnable {
	
	private SpatulaResource spat;
	private WokResource wok;

	BadChefRunnable(SpatulaResource spat, WokResource wok) {
		this.spat = spat;
		this.wok = wok;
	}

	@Override
	public void run() {
		for (int i=0; i<100; i++) {
			try {
				wok.acquire();
				Thread.sleep(5);
				spat.acquire();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			wok.release();
			spat.release();

			System.out.printf("Bad Chef Serving platter: %d\n", i);
		}
	}

}
