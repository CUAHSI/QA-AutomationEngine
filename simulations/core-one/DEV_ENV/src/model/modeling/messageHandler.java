/*  
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 

package model.modeling;


import java.util.*;

import GenCol.*;



public class messageHandler implements IODevs{
protected ports inports,outports,removedInports, removedOutports;
protected message input,output;

public ports getInports(){
return inports;
}
public ports getOutports(){
return outports;
}

public messageHandler(){
inports = new ports();
outports = new ports();
removedInports = new ports();
removedOutports = new ports();

}

public ExternalRepresentation getExtRep(){return new ExternalRepresentation.ByteArray();}
public String getName(){return "messageHandler";}
public Object equalName(String name){return null; }
public void addInport(String portName){inports.add(new port(portName));}
public void addOutport(String portName){outports.add(new port(portName));}
//by saurabh
public void removeInport(String portName){
  Iterator ip = inports.iterator();
 while(ip.hasNext()){
    port p = (port)ip.next();
    if(portName.equals(p.getName())){
      //System.out.println("inside the mh class, removing inport....Now, no. of inports"+inports.size());
       //inports.remove(p);
      removedInports.add(p);
     }
  }
//  System.out.println("printing the removed inports");
//  printPorts(removedInports);
  inports.removeAll(removedInports);
}
public void removeOutport(String portName){
  Iterator op = outports.iterator();
  while(op.hasNext()){
    port p = (port)op.next();
    if(portName.equals(p.getName())){
      //System.out.println("inside the mh class, removing outport..Now, no. of Out..ports"+outports.size());
      //outports.remove(p);
      removedOutports.add(p);
    }
  }
//  System.out.println("printing the removed outports");
//  printPorts(removedOutports);
  outports.removeAll(removedOutports);
}

public ContentInterface makeContent(PortInterface p,EntityInterface value){
return new content((port)p,(entity)value);
}
public content makeContent(String p,entity value){  //for use in usual devs
return new content(p,value);
}
public boolean   messageOnPort(MessageInterface x,PortInterface p, ContentInterface c){
return  x.onPort(p,c);
}
public boolean   messageOnPort(message x,String p, int i){ //for use in usual devs
return x.onPort(p,i);
}


}