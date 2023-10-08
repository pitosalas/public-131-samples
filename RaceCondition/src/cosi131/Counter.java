package cosi131;

public class Counter {
	Integer counter;
	String turn;
	
	Counter(String t, int initial) {
		counter = initial;
		turn = t;
	}
	
	 void increment(String name) {
		System.out.printf("T: %s = %d\n", turn, counter);
//		while (name != turn) 
//			Thread.yield();
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
