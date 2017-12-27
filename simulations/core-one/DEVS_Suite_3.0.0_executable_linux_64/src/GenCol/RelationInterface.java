/*     
 *    
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */
/*
/*  no correspondence in Java collections
/*  iteration is through Pairs rather than Entries
*/

package GenCol;


import java.util.*;


//Zcontainers compatibility through extending to ZRelationInterface

interface RelationInterface{

public boolean isEmpty();
public int size();
public boolean contains(Object key, Object value);
public Object get(Object key);
public Set getSet(Object key);
public Object put(Object key, Object value);
public Object remove(Object key, Object value);
public void removeAll(Object key);
public Set keySet();
public Set valueSet();
public Iterator iterator();
public String toString();
public int hashCode();
public boolean equals(Object o);
}




