package cosi131;

public interface Mutex 
{
	public abstract void enterCS (int turn);

	public abstract void exitCS (int turn);
}
