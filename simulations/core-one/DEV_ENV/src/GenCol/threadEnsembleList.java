/*     
 *    
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */
package GenCol;

import java.util.*;

public class threadEnsembleList extends LinkedList implements ensembleInterface{
private threadEnsembleWrapper.ensemble el;

public threadEnsembleList(){
el = threadEnsembleWrapper.make(this);
}

public threadEnsembleList(Collection c){
addAll(c);
el =threadEnsembleWrapper.make(this);
}

public void tellAll(String MethodNm,Class[] classes,Object[] args){
el.tellAll(MethodNm,classes,args);
}

public void tellAll(String MethodNm){
Class [] classes = {};
Object [] args  = {};
el.tellAll(MethodNm,classes,args);
}


public void AskAll(ensembleInterface result,String MethodNm,Class[] classes,Object[] args){
el.AskAll(result,MethodNm,classes,args);
}

public void which(ensembleInterface result,String MethodNm,Class[] classes,Object[] args){
 //MethodNm method must return this if condition is true and null otherwise
el.AskAll(result,MethodNm,classes,args);
}

public Object whichOne(String MethodNm,Class[] classes,Object[] args){
return el.whichOne(MethodNm,classes,args);
}
public  ensembleInterface copy(ensembleInterface c){
return el.copy(c);                             
}
public  void wrapAll(ensembleInterface Result,Class cl){
el.wrapAll(Result,cl);
}

public boolean none(String MethodNm,Class[] classes,Object[] args){
return el.none(MethodNm,classes,args);
}
public boolean all(String MethodNm,Class[] classes,Object[] args){
return el.all(MethodNm,classes,args);
}

public void print(){
el.print();
}

public static void main(String[] args){
threadEnsembleList L = new threadEnsembleList();
testEnsembleList t = new testEnsembleList(L);
t.applyTests("threadEnsembleList");
}
}


class testEnsembleList extends testGeneral{
protected threadEnsembleList b;

public testEnsembleList(threadEnsembleList B){
super("GenCol.testEnsembleList");
b = B;
}

entity e = new entity("e");
entity f = new entity("f");
entity g = new entity("g");


public boolean testAddAll(){
description = "testing add all size";
precondition = new Boolean(b.isEmpty());
b.add(e);
b.add(e);
b.add(f);
ensembleBag c = new ensembleBag();
c.addAll(b);
return c.size() ==  3;
}                   

public boolean testWhichSize(){
description = "testing size of which";
precondition = new Boolean(!b.contains(g));
b.add(e);
b.add(f);
b.add(g);
ensembleBag c = new ensembleBag();
Class [] classes = {ensembleBag.getTheClass("java.lang.String")};
Object [] args  = {"g"};
b.which(c,"equalName",classes,args);
return c.size() == 1;
}

public boolean testWhichOne(){
b.add(e);
b.add(e);
b.add(f);
b.add(g);
description = "testing whichone is correct";
precondition = Boolean.TRUE;
Class [] classes = {ensembleBag.getTheClass("java.lang.String")};
Object [] args  = {"e"};
Object r = b.whichOne("equalName",classes,args);
return ((entity)r).eq("e");
}

public boolean testWhichNone(){
description = "testing whichNone is correct";
precondition = Boolean.TRUE;
Class [] classes = {ensembleBag.getTheClass("java.lang.String")};
Object [] args  = {"ej"};
Object r = b.whichOne("equalName",classes,args);
return r == null;
}

}