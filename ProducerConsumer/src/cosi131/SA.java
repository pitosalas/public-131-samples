package cosi131;

// Implementation of Strict Alternation
public class SA implements Mutex {

	private int turn;

	public SA() {
		this.turn = 0;
	}

	 public void enterCS(int t) {
		while (this.turn != t)
			Thread.yield(); // yields CPU to equal priority thread
	}

	public void exitCS (int t) {
		this.turn = 1 - t;
	}

}