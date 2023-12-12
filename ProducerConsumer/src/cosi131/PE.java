package cosi131;

public class PE implements Mutex {

	public boolean flag0, flag1;
	public int turn;

	public PE() {
		flag0 = false;
		flag1 = false;
		turn = 0;
		System.out.println("PETERSONS ALGO");
	}

	@Override
	public void enterCS(int t) {
		System.out.printf("Turn: %d, flag 0=%b 1=%b\n", turn, flag0, flag1);
		if (t == 0) {
			flag0 = true;
			turn = 1;
			while (turn == 1 && flag1) {
				System.out.printf("yielded 0 - turn: %d, flag 0=%b 1=%b\n", turn, flag0, flag1);
				Thread.yield();
			}
		} else if (t == 1) {
			flag1 = true;
			turn = 0;
			while (turn == 0 && flag0) {
				System.out.printf("yielded 1 - turn: %d, flag 0=%b 1=%b\n", turn, flag0, flag1);
				Thread.yield();
			}
		} else
			System.out.println("Invalid t in enterCS");
	}

	@Override
	public void exitCS(int t) {
		flag0 = !(t == 0);
		flag1 = !(t == 1);
//		
//		if (t == 0)
//			flag0 = false;
//		else if (t == 1) {
//			flag1 = false;
//		} else
//			System.out.println("Invalid t in enterCS");
	}

}
