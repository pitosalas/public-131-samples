package cosi131demos;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;

public class Main {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Main m = new Main();
		m.demo2();

	}

	void demo2() {
		try {
			// create a new process
			System.out.println(">>> Creating Process");
			Process p = Runtime.getRuntime().exec("date");

			BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
			String s = null;
			while ((s = stdInput.readLine()) != null) {
				System.out.println(s);
			}
			// close the output stream
			System.out.println(">>> Closing the output stream");
			stdInput.close();
		} catch (Exception ex) {
			ex.printStackTrace();
		}

	}

}
