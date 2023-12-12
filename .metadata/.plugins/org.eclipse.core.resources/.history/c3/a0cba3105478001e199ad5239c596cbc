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
		for (int i=0; i<1000; i++) {
			try {
				wok.acquire();
				spat.acquire();
				Thread.sleep(0);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			spat.release();
			wok.release();

			System.out.printf("Bad Chef Serving platter: %d\n", i);
		}
	}

}
