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

public class JenkinsJobCoord extends ViewableAtomic {
    protected entity nextJob;

    public JenkinsJobCoord() {
	this("JenkinsJobCoord");
    }
    
    public JenkinsJobCoord(String name) {
	super(name);
	addInports();
	addOutports();
    }
    
    private void addInports(){
	addInport("github-response");
	addInport("trigger");
    }
    
    private void addOutports(){
	addOutport("github-request");
	addOutport("jenkins-api");
    }	
    
    public void initialize() {
	phase = "passive";
	sigma = INFINITY;
	super.initialize();
    }
    
    public void deltext(double e, message x) {
	Continue(e);
	for (int i=0; i<x.getLength(); i++) {
	    if (messageOnPort(x, "trigger", i)) {
		holdIn("cloning", 0);
	    } else if (messageOnPort(x, "github-response", i)) {
		holdIn("running", 0);
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
	if (phaseIs("cloning")) {
	    nextJob = new entity("repo-request");
	    m.add(makeContent("github-request", nextJob));
	} else if (phaseIs("running")) {
	    nextJob = new entity("job-initiation");
	    m.add(makeContent("jenkins-api", nextJob));
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
