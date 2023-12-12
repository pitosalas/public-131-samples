import java.util.Random;
import java.util.concurrent.Semaphore;

public class Car implements Runnable{
	String name;
	Semaphore semaphore;
	
	public Car(String name, Semaphore semaphore) {
		this.name = name;
		this.semaphore = semaphore;
	}
	
	public void run() {
		try {
			semaphore.acquire();
			System.out.println(Thread.currentThread().getName() + " entered the parking lot");
			Random rand = new Random();
			int sleepTime = rand.nextInt(4000) + 1000;
			Thread.sleep(sleepTime);
			System.out.println(Thread.currentThread().getName() + " left the parking lot");
			System.out.flush();
			semaphore.release();
			System.out.printf("the total number of cars in the parking lot is %d\n", semaphore.availablePermits());
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
}
