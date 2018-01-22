/*     
 *  Module Author         : Neal DeBuhr
 *  Module Date           : 27-December-2017  
 *  DEVS Suite Author     : Savitha and Anindita ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  DEVS Version          : DEVSJAVA 2.7 
 *  DEVS Date             : 15-April-2012
 *
 *  This component model handles the distribution of test cases to test executor nodes
 */
package CoreOne;

import java.util.Random;
import GenCol.*;
import model.modeling.*;
import model.simulation.*;
import view.modeling.ViewableAtomic;
import view.simView.*;

public class JenkinsJobTestcase extends ViewableAtomic {
    protected int ready;
    protected int jobsComplete;
    protected entity nextJob;
    protected entity completion;
    protected Random randomGenerator;
    protected int testResult;
    
    public JenkinsJobTestcase() {
	this("JenkinsJobTestcase");
    }
    
    public JenkinsJobTestcase(String name) {
	super(name);
	addInports();
	addOutports();
	addTestInputs();
    }
    
    private void addInports(){
	addInport("trigger");
	addInport("github-response");
	addInport("results");
    }

    private void addOutports(){
	addOutport("github-request");
	addOutport("to-grid");
	addOutport("status");
    }

    private void addTestInputs(){
	addTestInput("trigger", new entity("start"));
	addTestInput("trigger", new entity("start"), 20);
	addTestInput("github-response", new entity("repo"));
	addTestInput("github-response", new entity("repo"), 20);
	addTestInput("results", new entity("results"));
	addTestInput("results", new entity("results"), 20);
    }

    public void initialize() {
	phase = "passive";
	sigma = INFINITY;
	ready = 1;
	jobsComplete = 0;
	super.initialize();
    }

    public void deltext(double e, message x) {
	Continue(e);

	for (int i=0; i<x.getLength(); i++) {
	    if (messageOnPort(x, "results", i)) {
		ready = 1;
		jobsComplete += 1;
		randomGenerator = new Random();
		testResult = randomGenerator.nextInt(1);
		if (testResult == 1) {
		    holdIn("SUCCESS", INFINITY);
		} else {
		    holdIn("FAILED", INFINITY);
		}
	    }
	    if (messageOnPort(x, "github-response", i))
		holdIn("Running", 0);
	    if (messageOnPort(x, "trigger", i))
		holdIn("Cloning", 0);
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
	if (phaseIs("Cloning")){
	    nextJob = new entity("repo-request");
	    m.add(makeContent("github-request", nextJob));
	}
	if (phaseIs("Running")){
	    nextJob = new entity("test-case");
	    m.add(makeContent("to-grid", nextJob));
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
