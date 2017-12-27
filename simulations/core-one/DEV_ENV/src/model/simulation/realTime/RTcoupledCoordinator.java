/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 


package model.simulation.realTime;


import java.util.*;

import GenCol.*;


import model.modeling.*;
import model.simulation.*;


public class RTcoupledCoordinator extends coupledCoordinator implements RTCoupledCoordinatorInterface{

protected int numIter;
//protected  Thread myThread;
protected RTCoordinatorInterface myRTRootParent;
protected RTcoupledCoordinator myRTParent;

public RTcoupledCoordinator(Coupled c){
super(c);
}

public long timeInSecs() {
    return (timeInMillis()/1000);
}
public long timeInMillis() {
    return System.currentTimeMillis();
}
 public void setRTRootParent(RTCoordinatorInterface r){
myRTRootParent = r;
}

public RTCoordinatorInterface getRTRootParent(){
return myRTRootParent;
}

public void setRTParent(RTcoupledCoordinator r){
myRTParent = r;
}

public RTCoupledCoordinatorInterface getRTParent(){
return myRTParent;
}

public void addSimulator(IOBasicDevs comp){
coupledRTSimulator s = new coupledRTSimulator(comp);
simulators.add(s);
s.setRTParent(this);      // set the parent
modelToSim.put(comp.getName(),s);
internalModelTosim.put(comp.getName(),s);
}

public void addCoordinator(Coupled comp){
RTcoupledCoordinator s = new RTcoupledCoordinator(comp);
s.setRTParent(this);       // set the parent
simulators.add(s);
modelToSim.put(comp.getName(),s);
internalModelTosim.put(comp.getName(),s);
}


public void  simulate(int numIter)
{
  this.numIter = numIter;
  tL = timeInSecs();
  tN = nextTN();
  tellAllSimulate(numIter);
//  myThread.start();

  }

public synchronized void putMessages(ContentInterface c){
input.add(c);
sendDownMessages();
input = new message();
}

public synchronized void putMyMessages(ContentInterface c){
output.add(c);
sendMessages();
output = new message();
}

public void sendMessages() {    //extend so they send message to its parent also
  MessageInterface o = getOutput();
  if( o!= null && !o.isEmpty()) {
    Relation r = convertMsg((message)getOutput());//assume computeInputOutput done first
    Iterator rit = r.iterator();
    while (rit.hasNext()){
       Pair p = (Pair)rit.next();
       content co = (content)p.getValue();
       Object ds = p.getKey();
       if(modelToSim.get(ds) instanceof CoupledRTSimulatorInterface){
           CoupledRTSimulatorInterface sim = (CoupledRTSimulatorInterface)modelToSim.get(ds);
           sim.putMessages(co);
       }
       else if(modelToSim.get(ds) instanceof RTCoupledCoordinatorInterface){
           RTCoupledCoordinatorInterface sim = (RTCoupledCoordinatorInterface)modelToSim.get(ds);
           sim.putMessages(co);
       }
       else{            // this is an internal output coupling
           RTCoupledCoordinatorInterface cci = getRTParent();
           RTCoordinatorInterface ci = getRTRootParent();
           if(cci != null) myRTParent.putMyMessages(co);
           else if(ci != null)  myRTRootParent.putMyMessages(co);
       }
    }
  }
}

public void sendDownMessages() {
  if(!input.isEmpty()){
    Relation r = convertInput(input);
    Iterator rit = r.iterator();
    while (rit.hasNext()){
       Pair p = (Pair)rit.next();
       Object ds = p.getKey();
       content co = (content)p.getValue();
       if(internalModelTosim.get(ds) instanceof CoupledRTSimulatorInterface){
           CoupledRTSimulatorInterface sim = (CoupledRTSimulatorInterface)internalModelTosim.get(ds);
           sim.putMessages(co);
       }
       else if(internalModelTosim.get(ds) instanceof RTCoupledCoordinatorInterface){
           RTCoupledCoordinatorInterface sim = (RTCoupledCoordinatorInterface)internalModelTosim.get(ds);
           sim.putMessages(co);
       }
    }
  }
}

public void tellAllSimulate(int numIter){
Class [] classes  = {ensembleBag.getTheClass("java.lang.Integer")};
Object [] args  = {new Integer(numIter)};
simulators.tellAll("simulate",classes,args);
}

public void stopSimulate(){
simulators.tellAll("stopSimulate");
//myThread.interrupt();
}
/*
public void run(){
long observeTime = 10000;
 try {
  Thread.currentThread().sleep((long)observeTime);
} catch (Exception e) {}
tellAllStop();
System.out.println("Coordinator Terminated Normally at time: " + timeInMillis());

}
*/
public void tellAllStop(){
simulators.tellAll("stopSimulate");
}

}
