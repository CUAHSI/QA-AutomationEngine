/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
package view;


/**
 * FSimulatorView: Display the controller, realtime factor, animation speed factor, and TN&TL of the simulation
 * @modified Sungung Kim
 */
import facade.simulation.*;

//Standard API Imports
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import java.util.Hashtable;
import javax.swing.text.*;

import controller.ControllerInterface;
import controller.Governor;

import view.simView.*;

public class FSimulatorView extends JPanel
{
    private static final double[] REAL_TIME_FACTORS = {0.0001, 0.001, 0.01, 0.1, 0.5, 1, 5, 10, 50, 100, 1000};    
    
    /**
     * This slide is for animation speed on the simulation
     */
    protected double[] speedFactors = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    
    protected double[] timeViewFactors={1,5,10,15,20,30,50,100,1000};
    
    //Real Time Factor
    protected RealTimeFactor rtFactor;
    protected JSlider realFactor;    
    protected JLabel rtFactorLabel;
    
    //Speed Factor
    protected SpeedFactor speedFactor;
    protected JLabel speedFactorLabel;
    protected JSlider speedFactorSlider;
    
    protected TimeViewFactor timeViewFactor;
    protected JLabel timeViewFactorLabel;
    protected JSlider timeViewSlider;
	
	protected JCheckBox governorbox;
    
    private ControllerInterface controller;
    private FSimulator simulator;
    private JLabel sliderLabel;
    private Document simulatorDetailDoc;
    private final Color[] colors = {Color.black,new Color(0,0,128),new Color(0,0,128),
                                    Color.red,new Color(132,41,144),Color.darkGray};
    private final short HEADER_ATTR     = 0;
    private final short TIME_ATTR       = 1;
    private final short INITIAL_ATTR    = 2;
    private final short SIMULATING_ATTR = 3;
    private final short PAUSE_ATTR      = 4;
    private final short END_ATTR        = 5;
    private MutableAttributeSet[] attrSets;
    
    //Run, Step, Step(n), Pause, Reset
    private JButton[] ctrlButtons = new JButton[5];
    
    public FSimulatorView(ControllerInterface controller)
    {
        super(new BorderLayout());
        setBorder(BorderFactory.createTitledBorder("Simulator Control"));
        this.controller = controller;        
        add(Box.createVerticalStrut(100));
    }
    
    public void loadSimulator(FSimulator simulator)
    {
        removeAll();
        this.simulator = simulator;
        
        UniversalListener listener = new UniversalListener();
        
        ctrlButtons[0] = new JButton("Run");
        ctrlButtons[0].setActionCommand("RUN");
        ctrlButtons[0].addActionListener(listener);
        
        ctrlButtons[1]= new JButton("Step"); 
        ctrlButtons[1].setActionCommand("STEP");
        ctrlButtons[1].addActionListener(listener);
        
        ctrlButtons[2] = new JButton("Step(n)");
        ctrlButtons[2].setActionCommand("STEPN");
        ctrlButtons[2].addActionListener(listener);
        
        ctrlButtons[3] = new JButton("Request Pause");
        ctrlButtons[3].setActionCommand("PAUSE");
        ctrlButtons[3].addActionListener(listener);
        
        ctrlButtons[4] = new JButton("Reset");
        ctrlButtons[4].setActionCommand("RESET");
        ctrlButtons[4].addActionListener(listener);
        
        //Panel for the controller
        JPanel south = new JPanel();
        south.setLayout(new BoxLayout(south, BoxLayout.Y_AXIS));
        
        /**
         * Realtime factor controller
         */       
        rtFactor = new RealTimeFactor();
        rtFactorLabel = new JLabel();
        rtFactorLabel.setAlignmentX(0.5f);
        
        // this will get the initial speed factor value shown by the label
        rtFactor.set(rtFactor.get());
        
        // add the animation speed slider
        JSlider slider = realFactor = new JSlider();
        slider.setAlignmentX(0.5f);
        slider.setMinimum(0);
        slider.setMaximum(REAL_TIME_FACTORS.length - 1);
        slider.setSnapToTicks(true);
        
        // set the speed factor slider to the notch that corresponds
        // with the factor's value
        for (int i = 0; i < REAL_TIME_FACTORS.length; i++) {
            if (REAL_TIME_FACTORS[i] == rtFactor.get()) {
                slider.setValue(i);
                controller.userGesture(controller.SIM_SET_RT_GESTURE,
                        REAL_TIME_FACTORS[i]);
                break;
            }
        }

        // when the animation speed slider is adjusted
        slider.addChangeListener(new ChangeListener() {
            public void stateChanged(ChangeEvent e) {
                // store the speed value
                JSlider slider1 = realFactor;
                rtFactor.set(REAL_TIME_FACTORS[slider1.getValue()]);
                controller.userGesture(controller.SIM_SET_RT_GESTURE,
                        REAL_TIME_FACTORS[slider1.getValue()]);
            }
        });
        
        /**
         * Add to the panel
         */
        south.add(rtFactorLabel);
        south.add(slider);
        
        /**
         * Speed Factor controller
         */
        speedFactor = new SpeedFactor();
        
        speedFactorLabel = new JLabel();
        speedFactorLabel.setAlignmentX(0.5f);
        

        // this will get the initial speed factor value shown by the label
        speedFactor.set(speedFactor.get());

        // add the animation speed slider
        JSlider slider1 = speedFactorSlider = new JSlider();
        slider1.setAlignmentX(0.5f);
        slider1.setMinimum(0);
        slider1.setMaximum(speedFactors.length - 1);
        slider1.setSnapToTicks(true);
        
        // set the speed factor slider to the notch that corresponds
        // with the factor's value
        for (int i = 0; i < speedFactors.length; i++) {
            if (speedFactors[i] == speedFactor.get()) {
                slider1.setValue(i);
                break;
            }
        }

        // when the animation speed slider is adjusted
        slider1.addChangeListener(new ChangeListener() {
            public void stateChanged(ChangeEvent e) {
                // store the speed value
                JSlider slider2 = speedFactorSlider;
                speedFactor.set(speedFactors[slider2.getValue()]);                
            }
        });
        
        south.add(speedFactorLabel);
        
        if(!View.isSimView)
        	slider1.setEnabled(false);
        
        south.add(slider1);    

		
         /**
         * timeview factor controller
         */       
        timeViewFactor = new TimeViewFactor();
        timeViewFactorLabel = new JLabel();
        timeViewFactorLabel.setAlignmentX(0.5f);
        
        // this will get the initial speed factor value shown by the label
        timeViewFactor.set(timeViewFactor.get());
        
        // add the animation speed slider
        JSlider slider2 = timeViewSlider = new JSlider();
        slider2.setAlignmentX(0.5f);
        slider2.setMinimum(0);
        slider2.setMaximum(timeViewFactors.length - 1);
        slider2.setSnapToTicks(true);
        
        // set the speed factor slider to the notch that corresponds
        // with the factor's value
        for (int i = 0; i < timeViewFactors.length; i++) {
            if (timeViewFactors[i] == timeViewFactor.get()) {
                slider2.setValue(i);
                controller.userGesture(controller.SIM_SET_TV_GESTURE,
                        timeViewFactors[i]);
                break;
            }
        }

        // when the animation speed slider is adjusted
        slider2.addChangeListener(new ChangeListener() {
            public void stateChanged(ChangeEvent e) {
                // store the speed value
                JSlider slider3 = timeViewSlider;
                timeViewFactor.set(timeViewFactors[slider3.getValue()]);
                controller.userGesture(controller.SIM_SET_TV_GESTURE,
                        timeViewFactors[slider3.getValue()]);
            }
        });
        
        /**
         * Add to the panel
         */
        south.add(timeViewFactorLabel);
        south.add(slider2);

		//end of timeviewfactor
		
        JPanel simInfo = new JPanel(new BorderLayout());
        JTextPane simDetailArea = new JTextPane();
        simDetailArea.setBackground(new Color(204,204,204));
        simDetailArea.setEditable(false);
        simulatorDetailDoc  = simDetailArea.getDocument();
        simInfo.add(simDetailArea);
        south.add(simInfo);
        simInfo.setPreferredSize(new Dimension(0,60));
        
        JPanel panel = new JPanel(new GridLayout(0,2));
        
        for (int i = 0; i < ctrlButtons.length; i++)
            panel.add(ctrlButtons[i]);
			
		governorbox=new JCheckBox("Enable Governor");
		governorbox.addActionListener(listener);	
		Governor.setSelected(false);
		
		panel.add(governorbox);
        add(panel);
        add(south,BorderLayout.SOUTH);
        
        setupAttributeSets();
        synchronizeView();
        revalidate();
        repaint();
    }
    
    private void setupAttributeSets()
    {
        attrSets = new MutableAttributeSet[6];
        for (int i = 0; i < 6; i++)
        {
            attrSets[i] = new SimpleAttributeSet();
            StyleConstants.setFontFamily(attrSets[i],"Monospaced");
            StyleConstants.setForeground(attrSets[i], colors[i]);
            StyleConstants.setFontSize(attrSets[i],12);
            StyleConstants.setBold(attrSets[i],true);
        }
    }
    
    private void writeSimulatorInfo(String line, AttributeSet attr)
    {
        try {simulatorDetailDoc.insertString(
             simulatorDetailDoc.getLength(),line,attr);}
        catch (Exception e){}
    }
    
    public void synchronizeView()
    {
        //Corresponds to legal behaviors of the sim
        //run, step, step(n), pause, reset
        final boolean[] INITIAL_PAUSE = {true,true,true,false,true};
        final boolean[] SIMULATING    = {false,false,false,true,false};
        final boolean[] END           = {false,false,false,false,true};
        boolean[] legalBehavior = INITIAL_PAUSE;
        short state = simulator.getCurrentState();
        
        try {simulatorDetailDoc.remove(0,simulatorDetailDoc.getLength());}
        catch (Exception e){}
         
        String stateLabel = "Undefined";
        MutableAttributeSet stateAttr = attrSets[HEADER_ATTR];
        
        switch (state)
        {
            case FSimulator.STATE_INITIAL:
                stateLabel = "Ready";
                stateAttr    = attrSets[INITIAL_ATTR];
                legalBehavior = INITIAL_PAUSE;
                break;
            case FSimulator.STATE_SIMULATING:
                stateLabel = "Simulating";
                stateAttr    = attrSets[SIMULATING_ATTR];
                legalBehavior = SIMULATING;
                break;
            case FSimulator.STATE_PAUSE:
                stateLabel = "Pause";
                stateAttr    = attrSets[PAUSE_ATTR];
                legalBehavior = INITIAL_PAUSE;
                break;
            case FSimulator.STATE_END:
                stateLabel = "End";
                stateAttr    = attrSets[END_ATTR];
                legalBehavior = END;
                break;
        }
            
         for (int i = 0; i < legalBehavior.length; i++){
                ctrlButtons[i].setEnabled(legalBehavior[i]);
                View.ButtonControls[i].setEnabled(legalBehavior[i]);
                View.controlMenus[i].setEnabled(legalBehavior[i]);
         }
         
        writeSimulatorInfo("Simulator State: ",attrSets[HEADER_ATTR]);
        writeSimulatorInfo(stateLabel,stateAttr);
        writeSimulatorInfo("\nTime of Last Event: ",attrSets[HEADER_ATTR]);
        writeSimulatorInfo(""+Round(simulator.getTimeOfLastEvent(), 4),attrSets[TIME_ATTR]);        
        writeSimulatorInfo("\nTime of Next Event: ",attrSets[HEADER_ATTR]);
        writeSimulatorInfo(""+Round(simulator.getTimeOfNextEvent(), 4),attrSets[TIME_ATTR]);
      //  System.out.println("SimView%%%%%%%%%%%%%%%"+ simulator.getTimeOfNextEvent());
    }
    
    /**
     * Return double value with two decimal points
     */
    
    protected double Round(double Rval, int Rpl) {
    	if(Rval > Double.MAX_VALUE){//Infinity
    		return Rval;
    	}
    	else{
    	  double p = (double)Math.pow(10,Rpl);
    	  Rval = Rval * p;
    	  double tmp = Math.round(Rval);
    	  return (double)tmp/p;
    	}
    }
    
    /**
     * A wrapper for a speed factor value, changes to which must be
     * accompanied by other actions.
     */
    protected class SpeedFactor
    {
        /**
         * The value being wrapped.
         */
        private double speedFactor = 9;//fastest animation speed

        public double get() {return speedFactor;}

        /**
         * Updates the wrapped variable, and performs resulting side effects.
         */
        public void set(double speedFactor_)
        {
            speedFactor = speedFactor_;

            // update the speed label
            if (speedFactorLabel != null) {
                speedFactorLabel.setText("Animation Speed: " + speedFactor);
            }
            SimView.speed = speedFactor;
            
        }
    }
    
    /**
     * A wrapper for a real time factor value, changes to which must be
     * accompanied by other actions.
     */
    protected class RealTimeFactor
    {
        /**
         * The value being wrapped.
         */
        private double rtFactor = 0.0001;//fastest realtime factor

        public double get() {return rtFactor;}

        /**
         * Updates the wrapped variable, and performs resulting side effects.
         */
        public void set(double rtFactor_)
        {
        	rtFactor = rtFactor_;

            // update the speed label
            if (rtFactorLabel != null) {
                rtFactorLabel.setText("Real Time Factor: " + rtFactor);
            }
      
        }
    }
    
	protected class TimeViewFactor
	{
		private double factor=20;
		public double get(){return factor;}
		
		public void set(double x)
		{
			factor=x;
			if(timeViewFactorLabel!=null)
				timeViewFactorLabel.setText("Time View Update Speed: "+factor);
		}
	}
   
     
    private class UniversalListener implements ActionListener
    {
        
        public void actionPerformed(ActionEvent e) 
        {
            String actionCommand = e.getActionCommand();
            
            if (actionCommand.equalsIgnoreCase("RUN"))
                controller.userGesture(controller.SIM_RUN_GESTURE,null);
            
            else if (actionCommand.equalsIgnoreCase("STEP"))
                controller.userGesture(controller.SIM_STEP_GESTURE,null);
            
            else if (actionCommand.equalsIgnoreCase("STEPN"))
            {
                String val = JOptionPane.showInputDialog(View.PARENT_FRAME,"Number of steps to iterate: ");
                if (val != null)
                    try
                    {
                        Integer i = new Integer(val);
                        controller.userGesture(controller.SIM_STEPN_GESTURE,i);
                    }
                    catch (Exception exp){System.err.println(exp);}
                    
            }
            
            else if (actionCommand.equalsIgnoreCase("PAUSE"))
                controller.userGesture(controller.SIM_PAUSE_GESTURE,null);
            
            else if (actionCommand.equalsIgnoreCase("RESET"))
            {            	
                String msg = "Reset this Model?\n";
                msg += "All Tracking Data Will Be Lost";
                int option = JOptionPane.showConfirmDialog(View.PARENT_FRAME,msg,
                             "Reset Model?",JOptionPane.YES_NO_OPTION);
                if (option == JOptionPane.YES_OPTION)
                    controller.userGesture(controller.SIM_RESET_GESTURE,null);
                
            }
			else if(e.getSource()==governorbox)
			{
				Governor.setSelected(governorbox.isSelected());	
			}
        }        
    }
}