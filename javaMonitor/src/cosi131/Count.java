package cosi131;

class Count {

// A synchronized function named displayCounting() 
// is created that is taking an integer parameter n and displaying counting
// from 1 to n. The code Thread.sleep(500); will sleep the thread for
// 500 milliseconds when this line is executed.	

	synchronized void displayCounting(int n, String name, int sleep) {
		for (int i = 1; i <= n; i++) {
			System.out.printf("%s count=%d\n", name, i);
			try {
				Thread.sleep(sleep);
			} catch (Exception e) {
				System.out.println(e);
			}
		}
	}
}
