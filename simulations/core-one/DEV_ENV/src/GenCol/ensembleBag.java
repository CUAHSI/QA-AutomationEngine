/*     
 *    
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */

/**
* This is the basic class that has the full implementation of ensemble
* capabilities
 * Note: Restrictions:
 *1) the classes whose instances are added to any ensemble collection
 * must be public for the ensemble methods to work
 *
 * 2) for threaded variants,e.g., threadEnsembleBag, deadlocks have occured when
 * methods that call notify have been called by the ensemble.
*/


package GenCol;


import java.util.*;
import java.lang.reflect.*;



public class ensembleBag extends Bag implements ensembleInterface{

protected ensembleInterface result; //set by specific ensemble


/**
 * Makes it easy to get the class from its name.
 * Prints  exception if the the class doesn't exist.
 *
 * @version 1.0 11/12/00
 * @author BPZ
 */
public static Class getTheClass(String classnm){
Class str = null;
try{
     str = Class.forName(classnm);
}
catch(Exception e1) {
System.out.println(e1);
    }
return str;
}

public static void printClassMethods(Class cl){
Method n[] = cl.getMethods();
for (int i = 0;i<n.length;i++){
System.out.println(n[i].toString());
Class cln[] = n[i].getParameterTypes();
System.out.println(cln.toString());
}
}

public static Class[] getClasses(Object[] args){
Class classes[]  = new Class[args.length];
for (int i = 0;i<args.length;i++)
    classes[i] = args[i].getClass();
return classes;
}



public void tellAll(String MethodNm,Class[] classes,Object[] args){
Iterator it = iterator();
while(it.hasNext()){
Object o = it.next();
holder h = new holder(o,MethodNm,classes,args);
h.run();
}
}

public void tellAll(String MethodNm){
Class [] classes = {};
Object [] args  = {};
tellAll(MethodNm,classes,args);
}

public void AskAll(ensembleInterface Result,String MethodNm,Class[] classes,Object[] args){
result = Result;
Iterator it = iterator();
while(it.hasNext()){
Object o = it.next();
holder h = new holder(result,o,MethodNm,classes,args);
h.run();
}
}

public  void wrapAll(ensembleInterface Result,Class cl){
Iterator it = iterator();
while(it.hasNext()){
Object o = it.next();
holder h = new holder(Result,o,cl);
}
}
/**
* The method called MethodNm  must return "this" (pointer to itself) if condition is true
* and null otherwise
*/

public void which(ensembleInterface result,String MethodNm,Class[] classes,Object[] args)
{AskAll(result,MethodNm,classes,args);
}

/**
* The method called MethodNm  must return "this" (pointer to itself) if condition is true
* and null otherwise.
*/
public Object whichOne(String MethodNm,Class[] classes,Object[] args){
ensembleBag result = new ensembleBag();
AskAll(result,MethodNm,classes,args);
Iterator it = result.iterator();
return !it.hasNext()?null:it.next();
}

public boolean none(String MethodNm,Class[] classes,Object[] args){
Object o = whichOne(MethodNm,classes,args);
return o == null;
}

public boolean all(String MethodNm,Class[] classes,Object[] args){
ensembleBag result = new ensembleBag();
which(result,MethodNm,classes,args);
return result.size() == size();
}


public void print(){
Class classes[] = {};
Object arguments[] = {};
tellAll("print",classes,arguments);
}


public  ensembleInterface copy(ensembleInterface c){
                             //inherit directly to ensembleBag
ensembleBag wrapped = new ensembleBag();
ensembleBag result = new ensembleBag();
c.wrapAll(wrapped, ensembleBag.getTheClass("GenCol.wrapObject"));
Class [] classes = {ensembleBag.getTheClass("GenCol.ensembleBag")};
Object [] args  = {result};
wrapped.tellAll("addSelf",classes,args);
return result;
}


public boolean retainAll(Collection c) { //becomes set intersection
if (c.isEmpty()) return false;
ensembleBag wrapped = new ensembleBag();
ensembleBag result = new ensembleBag();
//ensembleInterface ce = (ensembleInterface)c;
ensembleBag ce = (ensembleBag)c;  //needed for recognition in reflect
wrapAll(wrapped, ensembleBag.getTheClass("GenCol.wrapObject"));
Class [] classes = {ensembleBag.getTheClass("GenCol.ensembleBag"),
                    ensembleBag.getTheClass("GenCol.ensembleBag")};
Object [] args  = {this,ce};
wrapped.tellAll("removeSelf",classes,args);
return true;
}

public boolean containsAll(Collection c) { //inclusion
if (c.isEmpty()) return true;
ensembleBag wrapped = new ensembleBag();
ensembleBag result = new ensembleBag();  //to efficiently use the return test
ensembleInterface ce = (ensembleInterface)c;
ce.wrapAll(wrapped, ensembleBag.getTheClass("GenCol.wrapObject"));
Class [] classes = {ensembleBag.getTheClass("GenCol.ensembleBag")};
Object [] args  = {this};
wrapped.AskAll(result,"isContained",classes,args);
return !result.contains(Boolean.FALSE);

}



public boolean addAll(Collection c){  //union
ensembleInterface ce = (ensembleInterface)c;
ensembleBag wrapped = new ensembleBag();
ce.wrapAll(wrapped, ensembleBag.getTheClass("GenCol.wrapObject"));
Class [] classes = {ensembleBag.getTheClass("GenCol.ensembleBag")};
Object [] args  = {this};
wrapped.tellAll("addSelf",classes,args);
return true;
}

public boolean removeAll(Collection c){ //difference
ensembleInterface ce = (ensembleInterface)c;
ensembleBag wrapped = new ensembleBag();
ce.wrapAll(wrapped, ensembleBag.getTheClass("GenCol.wrapObject"));
Class [] classes = {ensembleBag.getTheClass("GenCol.ensembleBag")};
Object [] args  = {this};
wrapped.tellAll("removeSelf",classes,args);
return true;
}

public Object[] toArray() {
	Object[] result = new Object[size()];
	Iterator e = iterator();
	for (int i=0; e.hasNext(); i++)
	    result[i] = e.next();
	return result;
    }


public Object[] toArray(Object a[]) {
        int size = size();
        if (a.length < size)
            a = (Object[])java.lang.reflect.Array.newInstance(
                                  a.getClass().getComponentType(), size);

        Iterator it=iterator();
        for (int i=0; i<size; i++)
            a[i] = it.next();

        if (a.length > size)
            a[size] = null;

        return a;
    }



}


