/*     
 *    
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */
/*
/*
/*   Pair is more  primitive than Entry which is private to Hashtable
*/

package GenCol;



import java.util.*;

public class Pair extends entity implements PairInterface{
public Object key,value;

public Pair(){
}

public Pair(Object Key, Object Value){
key = Key;
value = Value;
}
public String toString(){
return "key = " + key.toString() + " ,value = "+ value.toString();
}
public boolean equals(Object o){
	if (o == this)
	    return true;
Class cl = getClass();
if (!cl.isInstance (o))return false;
Pair p = (Pair)o;
return  key.equals(p.key) && value.equals(p.value);
}

public Object getKey(){
return key;
}

public Object getValue(){
return value;
}

public int hashCode(){
return key.hashCode() + value.hashCode();
}

public int compare(Object m,Object n){     //less than
Class cl = getClass();
if (!cl.isInstance (m) || !cl.isInstance(n))return 0;
Pair pm = (Pair)m;
Pair pn = (Pair)n;
if (m.equals(n))return 0;
if (pm.key.hashCode() < pn.key.hashCode()) return -1;
if (pm.key.hashCode() == pn.key.hashCode()
          && pm.value.hashCode() <= pn.value.hashCode())
                          return -1;
return 1;
}
}
class PairComparator implements Comparator{


public PairComparator(){
}

public boolean equals(Object o){
Class cl = getClass();
if (cl.isInstance (o))return true;
return false;
}

public int compare(Object m,Object n){     //less than
Class cl = testGeneral.getTheClass("GenCol.Pair");
if (!cl.isInstance (m) || !cl.isInstance(n))return 0;
Pair pm = (Pair)m;
Pair pn = (Pair)n;
if (m.equals(n))return 0;
if (pm.key.hashCode() < pn.key.hashCode()) return -1;
if (pm.key.hashCode() == pn.key.hashCode()
          && pm.value.hashCode() <= pn.value.hashCode())
                          return -1;
return 1;
}
}
