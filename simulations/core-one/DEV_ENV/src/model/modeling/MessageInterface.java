/*  
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 

package model.modeling;


import java.util.*;

import GenCol.*;






public interface MessageInterface  extends Collection{
public boolean onPort(PortInterface port, ContentInterface c);
public Object getValOnPort(PortInterface port,ContentInterface c);
public void print();
/* examples of using ensembleBag approach */
//public ensembleBag getPortNames();
public ensembleBag valuesOnPort(String portName);

// Jeff
ContentIteratorInterface mIterator();
// Jeff
}

