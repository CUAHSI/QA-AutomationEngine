/*     
 *  Module Author         : Neal DeBuhr
 *  Module Date           : 27-December-2017  
 *  DEVS Suite Author     : Savitha and Anindita ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  DEVS Version          : DEVSJAVA 2.7 
 *  DEVS Date             : 15-April-2012
 *
 */
package CoreOne;

import GenCol.*;
import model.modeling.*;
import model.simulation.*;
import view.modeling.ViewableAtomic;
import view.simView.*;

public class EmptyUnit extends ViewableAtomic {
    protected entity transObject;
    protected String entityName;
    protected boolean port0;
    protected boolean port1;
    protected boolean port2;
    protected boolean port3;
    protected boolean port4;
    protected boolean port5;
    
    public EmptyUnit() {
	this("EmptyUnit", "Object");
    }
    
    public EmptyUnit(String name, String entity_name) {
	super(name);
	addInports();
	addOutports();
	entityName = entity_name;
    }

    private void addInports(){
	addInport("0-in");
	addInport("1-in");
	addInport("2-in");
	addInport("3-in");
	addInport("4-in");
	addInport("5-in");
    }

    private void addOutports(){
	addOutport("0-out");
	addOutport("1-out");
	addOutport("2-out");
	addOutport("3-out");
	addOutport("4-out");
	addOutport("5-out");
    }
    
    public void initialize() {
	phase = "passive";
	sigma = INFINITY;
	super.initialize();
    }
    
    public void deltext(double e, message x) {
	Continue(e);
	for (int i=0; i<x.getLength(); i++){
	    if (messageOnPort(x, "0-in", i))
		port0 = true;
	    if (messageOnPort(x, "1-in", i))
		port1 = true;
	    if (messageOnPort(x, "2-in", i))
		port2 = true;
	    if (messageOnPort(x, "3-in", i))
		port3 = true;
	    if (messageOnPort(x, "4-in", i))
		port4 = true;
	    if (messageOnPort(x, "5-in", i))
		port5 = true;
	    holdIn("Process", 0);
	}
    }
    
    public void deltint() {
	passivate();
    }
    
    public void deltcon(double e, message x) {
	System.out.println("confluent");
	deltint();
	deltext(0, x);
    }
    
    public message out() {
	message m = new message();
	if (phaseIs("Process")){
	    if (port0){
		transObject = new entity(entityName);
		m.add(makeContent("0-out", transObject));
		port0 = false;
	    }
	    if (port1){
		transObject = new entity(entityName);
		m.add(makeContent("1-out", transObject));
		port1 = false;
	    }
	    if (port2){
		transObject = new entity(entityName);
		m.add(makeContent("2-out", transObject));
		port2 = false;
	    }
	    if (port3){
		transObject = new entity(entityName);
		m.add(makeContent("3-out", transObject));
		port3 = false;
	    }
	    if (port4){
		transObject = new entity(entityName);
		m.add(makeContent("4-out", transObject));
		port4 = false;
	    }
	    if (port5){
		transObject = new entity(entityName);
		m.add(makeContent("5-out", transObject));
		port5 = false;
	    }
	}
	return m;
    }
    
    public void showState() {
	super.showState();
    }
    
    public String getTooltipText() {
	return super.getTooltipText();
    }
}
