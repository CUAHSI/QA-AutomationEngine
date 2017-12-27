/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */  

package view.timeView;

public class Event {
	
	public final static String INPUT = TimeView.INPUT;
	public final static String OUTPUT = TimeView.OUTPUT;
	public final static String STATE = TimeView.STATE;
	public final static String STATEVARIABLE = TimeView.STATEVARIABLE;
	
	private String name = "";
	private String type = "";
	private double time = 0.0;
	private String data = "";
	
	public Event(String nm, String typ, double tm, String dat){
		name = nm;
		type = typ;
		time = tm;
		data = dat;
	}
	
	public String getName(){
		return name;
	}
	
	public String getType(){
		return type;
	}
	
	public double getTime(){
		return time;
	}
	
	public String getData(){
		return data;
	}
	
	/**
	 * added by Donna for testing
	 */
	public String toString(){
		return "<== at " + time + ": " + name + ", " + type + ", " + data + "==>"; 
	}
}
