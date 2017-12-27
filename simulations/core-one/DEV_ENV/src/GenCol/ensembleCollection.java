/*     
 *    
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */
package GenCol;

import java.util.*;

interface ensembleCollection extends ensembleBasic, Collection{
public void print();
public  void wrapAll(ensembleInterface Result,Class cl);
public ensembleInterface copy(ensembleInterface ce);
}

