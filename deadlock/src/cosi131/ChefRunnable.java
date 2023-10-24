package cosi131;

public class ChefRunnable implements Runnable {
	
	private SpatulaResource spat;
	private WokResource wok;

	ChefRunnable(SpatulaResource spat, WokResource wok) {
		this.spat = spat;
		this.wok = wok;
	}

	@Override
	public void run() {
		for (int i=0; i<100; i++) {
			try {
				spat.acquire();
				wok.acquire();
				Thread.sleep(35);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			wok.release();
			spat.release();
			System.out.printf("Serving platter: %d\n", i);
		}
	}

}
