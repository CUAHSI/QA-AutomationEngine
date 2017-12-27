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


public class threadEnsembleWrapper{
private threadEnsembleWrapper(){}       //no instantiation


public static ensemble make(Collection c){
	return new ensemble(c);
}

static class ensemble implements ensembleBasic,ensembleLogic{  //need static to be called from make
private Collection col;
private  countCoord c;

private ensemble (Collection col){     //only called from threadEnsembleWrapper
	    this.col = col;
}

public void tellAll(String MethodNm,Class[] classes,Object[] args){
countCoord c = new countCoord(col.size());
c.start();
coordTimer t = new coordTimer(c);
t.start();
c.setTimer(t);
Iterator it = col.iterator();
while(it.hasNext()){
Object o = it.next();
holder h = new holder(o,MethodNm,classes,args,c);
h.start();
}
while(c.isAlive());
}

public void tellAll(String MethodNm){
Class [] classes = {};
Object [] args  = {};
tellAll(MethodNm,classes,args);
}

public void AskAll(ensembleInterface result,String MethodNm,Class[] classes,Object[] args){

countCoord c = new countCoord(col.size());
c.start();
coordTimer t = new coordTimer(c);
t.start();
c.setTimer(t);
Iterator it = col.iterator();
while(it.hasNext()){
Object o = it.next();
holder h = new holder(result,o,MethodNm,classes,args,c);
h.start();
}
while(c.isAlive());
}


public void which(ensembleInterface result,String MethodNm,Class[] classes,Object[] args){
 //MethodNm method must return this if condition is true and null otherwise
AskAll(result,MethodNm,classes,args);
}

public Object whichOne(String MethodNm,Class[] classes,Object[] args){
ensembleBag result = new ensembleBag();
countCoord c = new countCoord(1,col.size());
c.start();
coordTimer t = new coordTimer(c);
t.start();
c.setTimer(t);
Iterator it = col.iterator();
while(it.hasNext()){
Object o = it.next();
holder h = new holder(result,o,MethodNm,classes,args,c,true);
h.start();
}
while(c.isAlive());
Iterator itr = result.iterator();
return itr.hasNext()?itr.next():null;
}

public  void wrapAll(ensembleInterface Result,Class cl){
Iterator it = col.iterator();
while(it.hasNext()){
Object o = it.next();
holder h = new holder(Result,o,cl);
}
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

public void print(){
Class classes[] = {};
Object arguments[] = {};
tellAll("print",classes,arguments);
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

}
}
