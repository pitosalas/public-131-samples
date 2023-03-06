package cosi131;

class Count {

// A synchronized function named displayCounting() 
// is created that is taking an integer parameter n and displaying counting
// from 1 to n. The code Thread.sleep(500); will sleep the thread for
// 500 milliseconds when this line is executed.	

	synchronized void displayCounting(int n) {
		for (int i = 1; i <= n; i++) {
			System.out.println(i);
			try {
				// sleep for 500 milliseconds
				Thread.sleep(500);
			} catch (Exception e) {
				System.out.println(e);
			}
		}
	}
}
