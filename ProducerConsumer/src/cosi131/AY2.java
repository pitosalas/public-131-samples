package cosi131;

public class AY2 implements Mutex {
	private int flag0, flag1;

	public AY2() {
		flag0 = flag1 = 0;
	}

	public void enterCS(int thread_id) {
		System.out.printf("enterCS: Thread_id %d starting, Flag1 = %s, Flag2 = %s\n", thread_id, flag0, flag1);
		if (thread_id == 0) {
			flag0 = 1;
			while (flag1 == 1)
				;
		} else if (thread_id == 1) {
			flag1 = 1;
			while (flag0 == 1)
				;
		} else
			System.out.println("invalid thread_id");
		System.out.printf("enterCS: Thread_id %d done, Flag1 = %s, Flag2 = %s\n", thread_id, flag0, flag1);
	}

	public void exitCS(int thread_id) {
		System.out.printf("exitCS: Thread_id %d starting, Flag1 = %s, Flag2 = %s\n", thread_id, flag0, flag1);
		if (thread_id == 0) {
			flag0 = 0;
		} else if (thread_id == 1) {
			flag1 = 0;
		} else
			System.out.println("invalid thread_id");
		System.out.printf("exitCS: Thread_id %d done, Flag1 = %s, Flag2 = %s\n", thread_id, flag0, flag1);

	}
}
