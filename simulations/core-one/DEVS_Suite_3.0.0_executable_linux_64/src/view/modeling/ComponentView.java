/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */  

package view.modeling;

import java.awt.*;

public interface ComponentView
{
    Point getPreferredLocation();
    Dimension getPreferredSize();
    Point getPortLocation(String portName);
    void injectAll();
    ViewableComponent getViewableComponent();
}