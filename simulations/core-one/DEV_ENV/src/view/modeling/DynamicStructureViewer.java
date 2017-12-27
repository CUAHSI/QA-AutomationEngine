/* /* 
 *   *Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
	 *  Version    : DEVSJAVA 3.0 Beta
	 *  Date       : 02-22-03
	 */

package view.modeling;

import model.modeling.*;

/**
 * the interface needed for displaying variable structure DEVS
 *
 * @author  Xiaolin Hu
 * @modified Muqsith
 */

public interface DynamicStructureViewer {
	   
	void couplingAdded(IODevs src, String p1, IODevs dest, String p2);
	void couplingRemoved(IODevs src, String p1, IODevs dest, String p2);
	void modelAdded(ViewableComponent iod, ViewableDigraph parent);
	void modelRemoved(ViewableComponent iod, ViewableDigraph parent);
}
