/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
/*
 * FSimulatorSCView.java
 * FSimulator State-Chart Viewer
 */

package view;

import facade.simulation.FSimulator;

import java.awt.Color;
import javax.swing.*;

public class FSimulatorSCView extends JInternalFrame
{
    private FSimulator simulator;
    private ImageIcon initialIcon;
    private ImageIcon simulatingIcon;
    private ImageIcon pauseIcon;
    private ImageIcon endIcon;
    private JLabel image;
    
    /** Creates a new instance of FSimulatorSCView */
    public FSimulatorSCView()
    {
        super("Abstracted Simulation State Chart",true,true,true,true);
        initialIcon    = new ImageIcon(ViewUtils.loadFullImage(ViewUtils.INITIAL_SC));
        simulatingIcon = new ImageIcon(ViewUtils.loadFullImage(ViewUtils.SIMULATING_SC));
        pauseIcon      = new ImageIcon(ViewUtils.loadFullImage(ViewUtils.PAUSE_SC));
        endIcon        = new ImageIcon(ViewUtils.loadFullImage(ViewUtils.END_SC));
        image = new JLabel(initialIcon);
        setSize(450, 350);
        setDefaultCloseOperation(HIDE_ON_CLOSE);
        
        JPanel panel = new JPanel();
        panel.setBackground(Color.white);
        panel.add(image);
        getContentPane().add(panel);
    }
    
    public void loadSimulator(FSimulator simulator)
    {
        this.simulator = simulator;
        synchronizeView();
    }
    
    public void synchronizeView()
    {
        switch (simulator.getCurrentState())
        {
            case FSimulator.STATE_INITIAL:
                image.setIcon(initialIcon);
                break;
            case FSimulator.STATE_SIMULATING:
                image.setIcon(simulatingIcon);
                break;
            case FSimulator.STATE_PAUSE:
                image.setIcon(pauseIcon);
                break;
            case FSimulator.STATE_END:
                image.setIcon(endIcon);
                break;
        }   
    }
}
