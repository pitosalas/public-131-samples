package cosi131;

public class Count1 {
	Integer counter;
	String turn;
	
	Count1(int initial) {
		counter = initial;
	}
	
	 void increment() {
		System.out.printf("Count is: %d\n", counter);
		counter = counter + 1;
	}
	
	String turn() {
		return turn;
	}
	

	public String toString() {
		return counter.toString();
	}

}
