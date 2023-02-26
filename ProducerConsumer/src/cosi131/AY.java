package cosi131;

public class AY implements Mutex {
	private boolean flag0, flag1;

	public AY() {
		flag0 = flag1 = false;
	}

	public void enterCS(int t) {
		if (t == 0) {
			flag0 = true;
			while (flag1)
				Thread.yield();
		} else {
			flag1 = true;
			while (flag0)
				Thread.yield();
		}
	}

	public void exitCS(int t) {
		if (t == 0)
			flag0 = false;
		else
			flag1 = false;
	}

	public void deadcheck() {
		if (flag0 && flag1)
			System.out.println("DEADLOCK!");
	}

}
