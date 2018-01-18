/*
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 

package model.simulation;

import java.util.*;

import GenCol.*;


import model.modeling.*;

//public
interface CouplingProtocolInterface {
public void putMessages(ContentInterface c);
public void sendMessages();
public void setModToSim(Function mts);
public void addPair(Pair cs,Pair cd);   //coupling pair
public void removePair(Pair cs, Pair cd); //remove coupling pair
public void showCoupling();
}

