/*     
 *    
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */
/*
/* wrapper class to create threaded ensemble classes
/*
*/

package GenCol;

import java.util.*;
import java.lang.reflect.*;
import java.io.*;


public class ensembleWrapper{

private ensembleWrapper.ensemble el;
private ensembleWrapper(){}       //no instantiation


public static ensemble make(Collection c){
	return new ensemble(c);
}

static class ensemble implements ensembleBasic,ensembleLogic{  //need static to be called from make
private Collection col;
private  countCoord c;

private ensemble (Collection col){     //only called from ensembleWrapper
	    this.col = col;
}

public void tellAll(String MethodNm,Class[] classes,Object[] args){
Iterator it = col.iterator();
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
Iterator it = col.iterator();
while(it.hasNext()){
Object o = it.next();
holder h = new holder(Result,o,MethodNm,classes,args);
h.run();
}
}

public  void wrapAll(ensembleInterface Result,Class cl){
Iterator it = col.iterator();
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
return result.size() == col.size();
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
	Object[] result = new Object[col.size()];
	Iterator e = col.iterator();
	for (int i=0; e.hasNext(); i++)
	    result[i] = e.next();
	return result;
    }


public Object[] toArray(Object a[]) {
        int size = col.size();
        if (a.length < size)
            a = (Object[])java.lang.reflect.Array.newInstance(
                                  a.getClass().getComponentType(), size);

        Iterator it= col.iterator();
        for (int i=0; i<size; i++)
            a[i] = it.next();

        if (a.length > size)
            a[size] = null;

        return a;
    }


}
}
