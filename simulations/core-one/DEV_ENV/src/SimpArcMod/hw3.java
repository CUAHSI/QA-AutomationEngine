/**
 * 
 */
/**
 * @author foonts
 *
 */
package SimpArcMod;


import java.lang.*;

import GenCol.*;


import model.modeling.*;
import model.simulation.*;

import view.modeling.ViewableAtomic;
import view.simView.*;


public class hw3 extends ViewableAtomic{


  protected double stepTime;
  protected int count;

  public hw3() {this("hw3", 30);}

public hw3(String name,double steptime){
   super(name);
   addInport("in");
   addOutport("out");
   stepTime = steptime ;
   
   addTestInput("in",new entity("0"));
   addTestInput("in",new entity("1"));
}

public void initialize(){
     holdIn("active", stepTime);
     phase = "passive";
     sigma = INFINITY;
     count = 0;
     super.initialize();
 }

public void  deltext(double e,message x)
{
	Continue(e);
	sigma = sigma - e;
	if(!messageOnPort(x,"in",0) && phaseIs("passive")){
		phase = "active";
		sigma = stepTime;
		count += 1;
	}
	else if(messageOnPort(x,"in",0) && phaseIs("passive")) {
		phase = "respond";
		sigma = stepTime;
	}
}


public void  deltint( )
{
	phase = "passive";
	sigma = INFINITY;
}

public message out( )
{

//System.out.println(name+" out count "+count);
   message  m = new message();
   if(phaseIs("respond")) {
	   content con = makeContent("out", new entity("" + count));
	   m.add(con);
   }
   return m;
}

}
