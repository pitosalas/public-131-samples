package cosi131;

public class PE implements Mutex {

	public boolean flag0, flag1;
	public int turn;

	public PE() {
		flag0 = false;
		flag1 = false;
		turn = 0;
	}

	@Override
	public void enterCS(int t) {
		// call with t = 0 if thread A, t = 1 if thread B
		if (t == 0) {
			flag0 = true;
			turn = 1;
			while (turn == 1 && flag1) {
			   System.out.printf("yielded 0 %b %b\n", flag0, flag1);
			   Thread.yield();
			}
		} else if (t == 1) {
			flag1 = true;
			turn = 0;
			while (turn == 0 && flag0) {
			   System.out.printf("yielded 1 %b %b\n", flag0, flag1);
			   Thread.yield();
			}
		} else
			System.out.println("Invalid t in enterCS");
	}

	@Override
	public void exitCS(int t) {
		if (t == 0)
			flag0 = false;
		else
			flag1 = false;
	}

}
