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

public class JenkinsCoord extends ViewableAtomic {
    protected entity repoObject;
    protected entity resultsObject;

    public JenkinsCoord() {
	this("JenkinsCoord");
    }
    
    public JenkinsCoord(String name) {
	super(name);
	addInports();
	addOutports();
    }
    
    private void addInports(){
	addInport("setup-in");
	addInport("results-in");
    }
    
    private void addOutports(){
	addOutport("setup-out");
	addOutport("results-out");
    }	
    
    public void initialize() {
	phase = "passive";
	sigma = INFINITY;
	super.initialize();
    }
    
    public void deltext(double e, message x) {
	Continue(e);
	for (int i=0; i<x.getLength(); i++) {
	    if (messageOnPort(x, "setup-in", i)) {
		holdIn("get repo", 0);
		System.out.println("Jenkins Job Initiated");
	    } else if (messageOnPort(x, "results-in", i)) {
		holdIn("send results", 0);
	    }
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
	if (phaseIs("get repo")) {
	    repoObject = new entity("clone request");
	    m.add(makeContent("setup-out", repoObject));
	} else if (phaseIs("send results")) {
	    resultsObject = new entity("test results");
	    m.add(makeContent("results-out", resultsObject));
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
