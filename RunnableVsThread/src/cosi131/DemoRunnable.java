package cosi131;
public class DemoRunnable {

	public static void main(String[] args) {
		System.out.println("Main Function");

		System.out.println("Creating runnables");
		
		Runnable runnable_a = new MyRunnable("How are you?", 100);
		Runnable runnable_b = new MyRunnable("hello", 200);
				
		System.out.println("Creating threads");
		Thread ta = new Thread(runnable_a);
		Thread tb = new Thread(runnable_b);
		
		System.out.println("Launching Threads");
		
		ta.start();
		tb.start();

	}

}
