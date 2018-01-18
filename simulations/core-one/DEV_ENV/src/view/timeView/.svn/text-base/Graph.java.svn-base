/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */  

package view.timeView;

public class Graph {
	public final static String INPUT = TimeView.INPUT;
	public final static String OUTPUT = TimeView.OUTPUT;
	public final static String STATEVARIABLE = TimeView.STATEVARIABLE;
	public final static String STATE= TimeView.STATE;
	public final static boolean NUMBER = TimeView.NUMBER;
	public final static boolean STRING = TimeView.STRING;
	
	private String name = "";
	private String type = "";
	private String Unit = "";
	private boolean dataType = NUMBER;
	
	public Graph(String nm, String typ, boolean datTyp){
		name = nm;
		type = typ;
		dataType = datTyp;
	}
	
	public Graph(String nm, String typ, boolean datTyp, String unitVal){
		name = nm;
		type = typ;
		Unit = unitVal;
		dataType = datTyp;
	}
	
	public String getName(){
		return name;
	}
	
	public String getType(){
		return type;
	}
	
	public boolean getDataType(){
		return dataType;
	}
	
	public String getUnit(){
		if(Unit.equalsIgnoreCase(""))
			return "N/A";
		else
			return Unit;
	}
}
