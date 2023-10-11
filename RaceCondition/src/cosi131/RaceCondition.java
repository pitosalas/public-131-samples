package cosi131;

public class RaceCondition {

	public static void main(String[] args) {
//		raceCondition1();
		raceCondition2();
	}
	
	private static void raceCondition1() {
		Count1 count = new Count1(0);

		Thread t1 = new Thread(new Runnable1(count));
		Thread t2 = new Thread(new Runnable1(count));

		t1.start();
		t2.start();

		try {
			t1.join();
			t2.join();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		System.out.println(count);
	}

	private static void raceCondition2() {
		
		
		Count2 count = new Count2("A", 0);

		Thread t1 = new Thread(new Runnable2("A", count));
		Thread t2 = new Thread(new Runnable2("B", count));

		t1.start();
		t2.start();

		try {
			t1.join();
			t2.join();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		System.out.println(count);
	}
}