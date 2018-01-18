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

import GenCol.*;
import model.modeling.*;
import model.simulation.*;
import view.modeling.ViewableAtomic;
import view.simView.*;

public class SeleniumGridHub extends ViewableAtomic {
    protected Queue jobsQueue;
    protected int numberNodes;
    protected int numberJobs;
    protected int nodeReady;
    protected int jobsComplete;
    protected entity nextJob;
    protected entity completion;
    
    public SeleniumGridHub() {
	this("SeleniumGridHub", 3, 10);
    }
    
    public SeleniumGridHub(String name, int number_nodes, int number_jobs) {
	super(name);
	numberNodes = number_nodes;
	numberJobs = number_jobs;
	addInports();
	addOutports();
	addTestInputs();
    }
    
    private void addInports(){
	addInport("code");
	addInport("status0");
	addInport("status1");
	addInport("status2");
    }

    private void addOutports(){
	addOutport("out0");
	addOutport("out1");
	addOutport("out2");
	addOutport("suite-status");
    }

    private void addTestInputs(){
	addTestInput("status1", new entity("free"));
	addTestInput("status1", new entity("free"), 20);
    }

    public void initialize() {
	phase = "passive";
	sigma = INFINITY;
	jobsQueue = new Queue();
	nodeReady = 1;
	jobsComplete = 0;
	for (int i=0; i<numberJobs; i++){
	    entity job = new entity("job"+Integer.toString(i));
	    jobsQueue.add(job);
	}
	super.initialize();
    }

    public void deltext(double e, message x) {
	Continue(e);

	for (int i=0; i<x.getLength(); i++) {
	    for (int j=0; j<numberNodes; j++)
		if (messageOnPort(x, "status"+Integer.toString(j), i)) {
		    nodeReady = j;
		    jobsComplete += 1;
		    if (jobsComplete == numberJobs) {
			holdIn("done", 0);
		    } else {
			holdIn("transmitting", 0);
		    }
		}
	    if (messageOnPort(x, "code", i))
		holdIn("initials", 0);
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
	if (phaseIs("initials")){
	    for (int i=0; i<numberNodes; i++){
		if (jobsQueue.size() > 0) {
		    nextJob = (entity)jobsQueue.remove();
		    m.add(makeContent("out"+Integer.toString(i), nextJob));
		}
	    }
	} else if (phaseIs("transmitting")){
	    if (jobsQueue.size() > 0) {
		nextJob = (entity)jobsQueue.remove();
		m.add(makeContent("out"+Integer.toString(nodeReady), nextJob));
	    }
	} else if (phaseIs("done")){
	    completion = new entity("Done");
	    m.add(makeContent("suite-status", completion));
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
