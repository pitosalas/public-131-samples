package cosi131;

public class RaceCondition {

	public static void main(String[] args) {
		Counter count = new Counter("A", 0);

		Thread t1 = new Thread(new CounterRunnable("A", count));
		Thread t2 = new Thread(new CounterRunnable("B", count));

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