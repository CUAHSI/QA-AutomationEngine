/*     
 *    
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */
/*
/* PairInterface is similar to Entry contained within Map
*/

package GenCol;



import java.util.*;


interface PairInterface {

public String toString();
public boolean equals(Object o);
public Object getKey();
public Object getValue();
public int hashCode();
public int compare(Object m,Object n);     //less than
}



