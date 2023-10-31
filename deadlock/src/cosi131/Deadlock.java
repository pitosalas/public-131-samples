package cosi131;

public class Deadlock {

	public static void main(String[] args) {
		SpatulaResource spatula = new SpatulaResource(10);
		WokResource wok = new WokResource(3);
		
		Thread chef1 = new Thread(new ChefRunnable(spatula, wok));
		Thread chef2 = new Thread(new ChefRunnable(spatula, wok));
		Thread chef3 = new Thread(new ChefRunnable(spatula, wok));
		Thread chef4 = new Thread(new ChefRunnable(spatula, wok));
		Thread chef5 = new Thread(new ChefRunnable(spatula, wok));
		
		chef1.start();
		chef2.start();
		chef3.start();
		chef4.start();
		chef5.start();
				
		
	}

}