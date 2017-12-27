/*     
 *    
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */
package GenCol;

import java.util.*;

interface ensembleBasic {
public void tellAll(String MethodNm,Class[] classes,Object[] args);
public void tellAll(String MethodNm);
public void AskAll(ensembleInterface result,String MethodNm,Class[] classes,Object[] args);
public void which(ensembleInterface result,String MethodNm,Class[] classes,Object[] args);
public Object whichOne(String MethodNm,Class[] classes,Object[] args);
}

