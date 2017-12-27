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

public class Bag extends Relation implements BagInterface{

public int numberOf(Object key){
return getSet(key).size();
}

public boolean add(Object o){
put(o,new Integer(numberOf(o)+1));
return true;
}

public boolean remove(Object o){
if (remove(o,new Integer(numberOf(o))) != null)
return true;
else return false;
}

public void clear(){
Set elements  = keySet();
Iterator it = elements.iterator();
while (it.hasNext())
   removeAll(it.next());
}

public Set bag2Set(){
return keySet();
}

public boolean contains(Object key){
return  numberOf(key)>0;
}

public Iterator iterator(){
return new BagIterator(this);
}

public String toString(){
Set s = bag2Set();
Iterator it = s.iterator();
String st = "";
while (it.hasNext()) {
  Object o = it.next();
  st += numberOf(o)+":"+o.toString()+"\n";
}
return st;
}



public static Bag List2Bag (java.util.List li){
Bag b = new Bag();
Iterator it = li.iterator();
while (it.hasNext())b.add(it.next());
return b;
}

}

class BagIterator extends RelationIterator{

public BagIterator(Bag b){
super(b);
}


public Object next(){
return ((Pair)super.next()).getKey();
}
}


