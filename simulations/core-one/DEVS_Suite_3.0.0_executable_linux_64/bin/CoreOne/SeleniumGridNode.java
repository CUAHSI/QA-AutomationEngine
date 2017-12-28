/*     
 *  Module Author         : Neal DeBuhr
 *  Module Date           : 27-December-2017  
 *  DEVS Suite Author     : Savitha and Anindita ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  DEVS Version          : DEVSJAVA 2.7 
 *  DEVS Date             : 15-April-2012
 *
 *  This component system acts as a test case executor, for example a Selenium Grid node.  The test cases are modeled as
 *  "jobs" to be processed.  The processing time for the received job is set as a random integer (0,300) multiplied by
 *  the executors "fitness" (default value of 1).
 */
package CoreOne;

import java.util.Random;
import GenCol.*;
import model.modeling.*;
import model.simulation.*;
import view.modeling.ViewableAtomic;
import view.simView.*;

public class SeleniumGridNode extends ViewableAtomic {// ViewableAtomic is used instead
	// of atomic due to its
	// graphics capability
	protected entity job;
	protected double processing_fitness;

	public SeleniumGridNode() {
	    this("SeleniumGridNode", 1);
	}

	public SeleniumGridNode(String name, double Processing_fitness) {
		super(name);
		addInport("in");
		addOutport("out");
		processing_fitness = Processing_fitness;
		addTestInput("in", new entity("job1"));
		addTestInput("in", new entity("job2"), 20);
	}

	public void initialize() {
		phase = "passive";
		sigma = INFINITY;
		job = new entity("job");
		super.initialize();
	}

	public void deltext(double e, message x) {
		Continue(e);

		if (phaseIs("passive"))
			for (int i = 0; i < x.getLength(); i++)
				if (messageOnPort(x, "in", i)) {
					job = x.getValOnPort("in", i);
					Random randomGenerator = new Random();
					int processing_time = randomGenerator.nextInt(300);
					processing_time *= processing_fitness;
					holdIn("busy", processing_time);
				}
	}

	public void deltint() {
		passivate();
		job = new entity("none");
	}

	public void deltcon(double e, message x) {
	    // Job finishes processing before receiving next job, should
	    // these events be scheduled for the same time
		System.out.println("confluent");
		deltint();
		deltext(0, x);
	}

	public message out() {
		message m = new message();
		if (phaseIs("busy")) {
			m.add(makeContent("out", job));
		}
		return m;
	}

	public void showState() {
		super.showState();
		// System.out.println("job: " + job.getName());
	}

	public String getTooltipText() {
		return super.getTooltipText() + "\n" + "job: " + job.getName();
	}
}
