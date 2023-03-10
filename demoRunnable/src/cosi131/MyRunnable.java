package cosi131;

public class MyRunnable implements Runnable {

	private String myName;
	private long sleeptime;

	MyRunnable(String name, int sleeptime) {
		myName = name;
		this.sleeptime = sleeptime;
	}

	@Override
	public void run() {
		for (int i = 0; i < 10; i++) {
			System.out.println(myName);
			try {
				Thread.sleep(sleeptime);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

}
