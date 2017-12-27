/*
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 

package model.modeling;


import java.util.*;

import GenCol.*;





/*
class componentIterator{
private Iterator it;
public componentIterator(ComponentsInterface c){it = c.iterator();}
public boolean hasNext(){return it.hasNext();}
public IOBasicDevs nextComponent() {return (IOBasicDevs)it.next();}   //  ???  Problem
}
*/

//public class Components extends threadEnsembleSet implements ComponentsInterface{
public class Components extends ensembleSet implements ComponentsInterface{
public componentIterator cIterator(){
return new componentIterator(this);
}
}