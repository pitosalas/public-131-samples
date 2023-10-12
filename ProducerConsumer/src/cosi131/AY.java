package cosi131;

public class AY implements Mutex {
	private boolean flag0, flag1;

	public AY() {
		flag0 = flag1 = false;
		System.out.println("AFTER YOU ALGO");
	}

	public void enterCS(int tread_id) {
		deadcheck("+entercs");

		if (tread_id == 0) {
			flag0 = true;
			while (flag1);
//				System.out.println("Yielding...Flag1");
//				Thread.yield();
		} else if (tread_id == 1) {
			flag1 = true;
			while (flag0);
//				System.out.println("Yielding...Flag0");
//				Thread.yield();
		} else
			System.out.printf("********* t is neither 0 or 1\f");
			
		System.out.printf("Worker %d successfully entered: flag0: %s flag1: %s\n", tread_id, flag0, flag1);
		deadcheck("-entercs");

	}

	public void exitCS(int tread_id) {
		deadcheck("+exitcs");
//		flag0 = !(t == 0);
//		flag1 = !(t == 1);
		if (tread_id == 0)
			flag0 = false;
		else if (tread_id == 1)
			flag1 = false;
		else System.out.println("*************** Exit cs threadid issue");
		System.out.printf("Worker %d successfully left: flag0: %s flag1: %s\n", tread_id, flag0, flag1);
		deadcheck("-exitcs");

	}

	public void deadcheck(String w) {
		System.out.printf("Deadcheck %s, flag0: %s flag1: %s\n", w, flag0, flag1);
		if (flag0 && flag1)
			System.out.printf("DEADLOCK: %s\n", w);
	}

}
