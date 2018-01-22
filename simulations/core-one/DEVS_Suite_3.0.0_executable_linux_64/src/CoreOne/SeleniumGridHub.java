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
    protected boolean job0;
    protected boolean job1;
    protected boolean job2;
    protected boolean job3;
    protected boolean job4;
    protected boolean node0;
    protected boolean node1;
    protected boolean node2;
    protected Queue jobsQueue;
    protected Queue resultsQueue;
    protected int numberNodes;
    protected int numberJobs;
    protected int jobsComplete;
    protected entity job;
    protected entity nextJob;
    protected String nextResult;
    protected entity completion;
    protected int fullCount;
    
    public SeleniumGridHub() {
	this("SeleniumGridHub", 3, 5);
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
	addInport("jenkins-0-in");
	addInport("jenkins-1-in");
	addInport("jenkins-2-in");
	addInport("jenkins-3-in");
	addInport("jenkins-4-in");
	addInport("node-0-in");
	addInport("node-1-in");
	addInport("node-2-in");
    }

    private void addOutports(){
	addOutport("jenkins-0-out");
	addOutport("jenkins-1-out");
	addOutport("jenkins-2-out");
	addOutport("jenkins-3-out");
	addOutport("jenkins-4-out");
	addOutport("node-0-out");
	addOutport("node-1-out");
	addOutport("node-2-out");
    }

    private void addTestInputs(){
	addTestInput("status1", new entity("free"));
	addTestInput("status1", new entity("free"), 20);
    }

    public void initialize() {
	phase = "passive";
	sigma = INFINITY;
	jobsQueue = new Queue();
	node0 = true;
	node1 = true;
	node2 = true;
	resultsQueue = new Queue();
	resultsQueue.add("jenkins-2-out");
	resultsQueue.add("jenkins-1-out");
	resultsQueue.add("jenkins-4-out");
	resultsQueue.add("jenkins-0-out");
	resultsQueue.add("jenkins-3-out");
	jobsComplete = 0;
	super.initialize();
    }

    public void deltext(double e, message x) {
	Continue(e);

	for (int i=0; i<x.getLength(); i++) {
	    if (messageOnPort(x, "jenkins-0-in", i)) {
		job = new entity("test-case");
		jobsQueue.add(job);
		holdIn("send-case", 0);
	    }
	    if (messageOnPort(x, "jenkins-1-in", i)) {
		job = new entity("test-case");
		jobsQueue.add(job);
		holdIn("send-case", 0);
	    }
	    if (messageOnPort(x, "jenkins-2-in", i)) {
		job = new entity("test-case");
		jobsQueue.add(job);
		holdIn("send-case", 0);
	    }
	    if (messageOnPort(x, "jenkins-3-in", i)) {
		job = new entity("test-case");
		jobsQueue.add(job);
		holdIn("send-case", 0);
	    }
	    if (messageOnPort(x, "jenkins-4-in", i)) {
		job = new entity("test-case");
		jobsQueue.add(job);
		holdIn("send-case", 0);
	    }
	    if (messageOnPort(x, "node-0-in", i)) {
		node0 = true;
		jobsComplete += 1;
		if (jobsQueue.size() == 0) {
		    holdIn("send-results", 0);
		} else {
		    holdIn("send-both", 0);
		}
	    }
	    if (messageOnPort(x, "node-1-in", i)) {
		node1 = true;
		jobsComplete += 1;
		if (jobsQueue.size() == 0) {
		    holdIn("send-results", 0);
		} else {
		    holdIn("send-both", 0);
		}
	    }
	    if (messageOnPort(x, "node-2-in", i)) {
		node2 = true;
		jobsComplete += 1;
		if (jobsQueue.size() == 0) {
		    holdIn("send-results", 0);
		} else {
		    holdIn("send-both", 0);
		}
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
	if (phaseIs("send-results") || phaseIs("send-both")) {
	    nextResult = (String)resultsQueue.remove();
	    nextJob = new entity("results");
	    m.add(makeContent(nextResult, nextJob));
	}
	if (phaseIs("send-case") || phaseIs("send-both")){
	    if (jobsQueue.size() > 0)
		if (node0) {
		    nextJob = (entity)jobsQueue.remove();
		    m.add(makeContent("node-0-out", nextJob));
		    node0 = false;
		}
	    if (jobsQueue.size() > 0)
		if (node1) {
		    nextJob = (entity)jobsQueue.remove();
		    m.add(makeContent("node-1-out", nextJob));
		    node1 = false;
		}
	    if (jobsQueue.size() > 0)
		if (node2) {
		    nextJob = (entity)jobsQueue.remove();
		    m.add(makeContent("node-2-out", nextJob));
		    node2 = false;
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
