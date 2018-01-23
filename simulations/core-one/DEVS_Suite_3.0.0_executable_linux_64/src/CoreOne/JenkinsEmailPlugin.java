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

public class JenkinsEmailPlugin extends ViewableAtomic {
    protected String emailAddress;
    
    public JenkinsEmailPlugin() {
	this("JenkinsEmailPlugin", "ndebuhr@cuahsi.org");
    }
    
    public JenkinsEmailPlugin(String name, String email_address) {
	super(name);
	emailAddress = email_address;
	addInports();
    }
    
    private void addInports(){
	addInport("in");
    }	
    
    public void initialize() {
	phase = "passive";
	sigma = INFINITY;
	super.initialize();
    }
    
    public void deltext(double e, message x) {
	Continue(e);
	holdIn("email-sent", INFINITY);
	System.out.println("Test Results Email Sent");
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
	return m;
    }
    
    public void showState() {
	super.showState();
    }
    
    public String getTooltipText() {
	return super.getTooltipText() + "\n" + "email: " + emailAddress;
    }
}
