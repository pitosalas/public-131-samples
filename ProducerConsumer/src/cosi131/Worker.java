package cosi131;

import java.util.Random;

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
		if (id == 0) {
			while (true) {
				log("\nwork");
				generateSleepTime(300, 1000);
				mutex.enterCS(id);
				log("++cs");
				generateSleepTime(300, 1000);
				mutex.exitCS(id);
				log("--cs");
				generateSleepTime(600, 2000);
				log("done");
			}
		} else if (id == 1) {
			log("\nwork");
			mutex.enterCS(id);
			log("++cs");
			generateSleepTime(300, 1000);
			mutex.exitCS(id);
			log("--cs");
			generateSleepTime(50, 100);
			log("done");
		} else
			System.out.println("Invalid thread number");
	}

	private void generateSleepTime(int min, int max) {
		Random rand = new Random();
		int sleep_ms = rand.nextInt((max - min) + 1) + min;
		System.out.printf("Sleep(%d): %d\n", id, sleep_ms);
		try {
			Thread.sleep(sleep_ms);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private void log(String s) {
		System.out.printf("%s \"%s\"\n", s, name);

	}
}