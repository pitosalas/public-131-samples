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
		try {
			if (id == 0) {
				while (true) {
					System.out.printf("\"entercs\", \"%s\"\n", name);
					mutex.enterCS(id);
					Thread.sleep(generateSleepTime(300, 1000));
					mutex.exitCS(id);
					System.out.printf("\"exitcs\", \"%s\"\n", name);
					Thread.sleep(generateSleepTime(600, 2000));
					System.out.printf("\"exhitwhile\", \"%s\"\n", name);
				}
			} else if (id == 1) {
				System.out.printf("\"entercs\", \"%s\"\n", name);
				mutex.enterCS(id);
				Thread.sleep(generateSleepTime(300, 1000));
				mutex.exitCS(id);
				System.out.printf("\"exitcs\", \"%s\"\n", name);
				Thread.sleep(generateSleepTime(50, 100));		
				System.out.printf("\"exhitwhile\", \"%s\"\n", name);
			} else
				System.out.println("Invalid thread number");
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private int generateSleepTime(int min, int max) {
		Random rand = new Random();
		return rand.nextInt((max - min) + 1) + min;
	}
}