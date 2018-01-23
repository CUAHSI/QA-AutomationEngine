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

public class GithubThread extends ViewableAtomic {
    protected String repositoryName;
    protected entity repoObject;
    
    public GithubThread() {
	this("GithubThread", "CUAHSI QA Automation Engine");
    }
    
    public GithubThread(String name, String repository_name) {
	super(name);
	repositoryName = repository_name;
	addInports();
	addOutports();
    }

    private void addInports(){
	addInport("in");
    }

    private void addOutports(){
	addOutport("out");
    }
    
    public void initialize() {
	phase = "passive";
	sigma = INFINITY;
	super.initialize();
    }
    
    public void deltext(double e, message x) {
	Continue(e);
	
	holdIn("clone request", 0);
	System.out.println("Git Clone Request Received");
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
	if (phaseIs("clone request")) {
	    repoObject = new entity("repository");
	    m.add(makeContent("out", repoObject));
	}
	return m;
    }
    
    public void showState() {
	super.showState();
    }
    
    public String getTooltipText() {
	return super.getTooltipText() + "\n" + "repo: " + repositoryName;
    }
}
