package cosi131;

public class Count2 {
	Integer counter;
	String turn;
	
	Count2(String t, int initial) {
		counter = initial;
		turn = t;
	}
	
	 void increment(String name) {
		while (name != turn) 
			Thread.yield();
		System.out.printf("T: %s = %d\n", turn, counter);
		counter = counter + 1;
		turn = turn.equals("A") ? "B" : "A";
	}
	
	String turn() {
		return turn;
	}
	

	public String toString() {
		return counter.toString();
	}

}
