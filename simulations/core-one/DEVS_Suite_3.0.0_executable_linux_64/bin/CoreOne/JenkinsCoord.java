/*     
 *  Module Author         : Neal DeBuhr
 *  Module Date           : 27-December-2017  
 *  DEVS Suite Author     : Savitha and Anindita ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  DEVS Version          : DEVSJAVA 2.7 
 *  DEVS Date             : 15-April-2012
 *
 */
package CoreOne;

import java.util.Random;
import GenCol.*;
import model.modeling.*;
import model.simulation.*;
import view.modeling.ViewableAtomic;
import view.simView.*;

public class JenkinsCoord extends ViewableAtomic {
    // ViewableAtomic is used instead
    // of atomic due to its
    // graphics capability
    
    public JenkinsCoord() {
	this("JenkinsCoord");
    }
    
    public JenkinsCoord(String name) {
	super(name);
	addInport("setup-in");
	addOutport("setup-out");
	addInport("results-in");
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
	    entity repo_object = new entity("clone request");
	    m.add(makeContent("setup-out", repo_object));
	} else if (phaseIs("send results")) {
	    entity results_object = new entity("test results");
	    m.add(makeContent("results-out", results_object));
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
