package cosi131;

public class Deadlock {

	public static void main(String[] args) {
		SpatulaResource spatula = new SpatulaResource(1);
		WokResource wok = new WokResource(1);
		
		Thread chef1 = new Thread(new ChefRunnable(spatula, wok));
		Thread chef2 = new Thread(new BadChefRunnable(spatula, wok));
		
		chef1.start();
		chef2.start();
				
	}

}
