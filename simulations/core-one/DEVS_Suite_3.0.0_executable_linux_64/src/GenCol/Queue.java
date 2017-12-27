/*     
 *    
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */

package GenCol;



import java.util.*;

public class Queue extends LinkedList{  //add is to end

//DEVSJAVA2.7.0 implementation is revised for compatability with JDK5.0 
public Object remove(){
if (size()>0){
return remove(0);
}
return null;
}

public Object first(){
return get(0);
}


static public Queue set2Queue(Set s){
Queue q = new Queue();
Iterator it = s.iterator();
while (it.hasNext())q.add(it.next());
return q;
}

public Bag Queue2Bag(){
Bag b = new  Bag();
Iterator it = iterator();
while (it.hasNext())b.add(it.next());
return b;
}

}


