package cosi131;

import java.util.ArrayList;

public class Pipe {
	private ArrayList<Object> queue;
	private boolean open;

	public Pipe() {
		queue = new ArrayList<Object>();
		open = true;
	}
	
	public void close() {
		open = false;
	}
	
	public boolean isOpen() {
		return open;
	}
	

	public void send(Object item) {
		queue.add(item);
	}

	public Object receive() {
		if (queue.size() == 0)
			return null;
		else
			return queue.remove(0);
	}

	public boolean empty() {
		return queue.isEmpty();
	}
}
