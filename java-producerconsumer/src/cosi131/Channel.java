package cosi131;

import java.util.ArrayList;

public class Channel {
	private ArrayList<Object> queue;

	public Channel() {queue = new ArrayList<Object>();}

	public void send (Object item) {
		queue.add(item);
	}

	public Object receive () {
		if (queue.size() == 0)
		   return null;
		else
		   return queue.remove(0);
	}
}
