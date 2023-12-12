import java.util.ArrayList;
import java.util.concurrent.Semaphore;

public class ParkingLot {
	
	public static Semaphore semephore = new Semaphore(50);
	public static ArrayList<Thread> threadList = new ArrayList<Thread>();
	
	public static void main(String[] args) {
		
		for (int i = 0; i < 100; i++) {
			Car currentCar = new Car("car" + (i+1), semephore);
			Thread currentThread = new Thread(currentCar);
			currentThread.setName("car" + (i+1));
			threadList.add(currentThread);
		}
		
		
		for (Thread thread: threadList) {
			thread.start();
		}
		
	}
	
	

}
