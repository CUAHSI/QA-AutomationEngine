/* Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 

package model.modeling;


import java.util.*;

import GenCol.*;






public interface ContentInterface {
public PortInterface getPort();
public String getPortName();
public Object getValue();
public boolean onPort(PortInterface port);
}



