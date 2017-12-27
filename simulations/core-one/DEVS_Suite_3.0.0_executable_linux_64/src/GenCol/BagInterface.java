/*     
 *    
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */

/*
/*  no correspondence in Java collections
*/

package GenCol;


import java.util.*;

interface BagInterface { //extends Collection{
public int numberOf(Object key);
public void removeAll(Object key);
public Set bag2Set();
//public static Bag List2Bag (java.util.List li);

}
