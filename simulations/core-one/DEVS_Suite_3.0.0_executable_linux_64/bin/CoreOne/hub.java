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

public class hub extends ViewableAtomic {// ViewableAtomic is used instead
    // of atomic due to its
    // graphics capability
    protected Queue jobs_queue;
    protected int number_nodes;
    protected int number_jobs;
    protected int node_ready;
    protected entity next_job;
    
    public hub() {
	this("hub", 3, 10);
    }
    
    public hub(String name, int Number_nodes, int Number_jobs) {
	super(name);
	for (int i=0; i<number_nodes; i++){
	    addOutport("out"+Integer.toString(i));
	    addInport("status"+Integer.toString(i));
	}
	number_nodes = Number_nodes;
	number_jobs = Number_jobs;
	addTestInput("status1", new entity("free"));
	addTestInput("status1", new entity("free"), 20);
    }

    public void initialize() {
	phase = "initials";
	sigma = 0;
	jobs_queue = new Queue();
	node_ready = 1;
	for (int i=0; i<number_jobs; i++){
	    entity job = new entity("job"+Integer.toString(i));
	    jobs_queue.add(job);
	}
	super.initialize();
    }

    public void deltext(double e, message x) {
	Continue(e);

	for (int i=0; i<x.getLength(); i++)
	    for (int j=0; j<number_nodes; j++)
		if (messageOnPort(x, "status"+Integer.toString(j), i)) {
		    node_ready = j;
		    holdIn("transmitting", 0);
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
	    for (int i=0; i<number_nodes; i++){
		if (jobs_queue.size() > 0) {
		    next_job = (entity)jobs_queue.remove();
		    m.add(makeContent("out"+Integer.toString(i), next_job));
		}
	    }
	}
	if (phaseIs("transmitting")){
	    if (jobs_queue.size() > 0) {
		next_job = (entity)jobs_queue.remove();
		m.add(makeContent("out"+Integer.toString(node_ready), next_job));
	    }
	}
	return m;
    }
    
    public void showState() {
	super.showState();
	// System.out.println("job: " + job.getName());
    }
    
    public String getTooltipText() {
	return super.getTooltipText();
    }
}
