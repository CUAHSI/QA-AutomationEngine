/*
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 



package model.simulation;


import java.util.*;

import GenCol.*;


import model.modeling.*;


public interface CoordinatorInterface extends AtomicSimulatorInterface{
public void setSimulators();
public void addSimulator(IOBasicDevs comp);
public void addCoordinator(Coupled comp);
public coupledDevs getCoupled();
public void addExtPair(Pair cs,Pair cd) ;
public void informCoupling();
public void showCoupling();
public Relation convertInput(MessageInterface x);
public void putMyMessages(ContentInterface c);
public void sendDownMessages();
//public void decrement();


}