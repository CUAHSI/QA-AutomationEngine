/**
 * ViewInterface.java
 * Provides View Interface
 * Created on September 18, 2002, 4:21 PM
 */
/**
 *
 * @author  rsingh
 */

package view;

//Facade Connections
import javax.swing.JPanel;

import view.simView.SimView;
import facade.simulation.FSimulator;


public interface ViewInterface 
{
    public void synchronizeView();
    public void loadSimulator(FSimulator simulator);
    public void addTrackingColumn(double currentTime);
    public void clearConsole();
    public String getHTMLTrackingLog();
    public String getConsoleLog();
    public String[] getEncodedCSVExport();
    public String getCSVExport();
    public void simlationControl(String control);
    public SimView getSim();
    public JPanel getConsole();
    public void removeExternalWindows();
}
