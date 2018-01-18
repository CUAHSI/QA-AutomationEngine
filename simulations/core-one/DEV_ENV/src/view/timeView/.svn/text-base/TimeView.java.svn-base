/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */  
/**
 * This class will create the TimeView and integrated into the Tracking Environment
 * The data displayed on the time based chart are from the Facade layer
 * @modified Sungung Kim
 * @date: 5/30/2008
 *
 */

package view.timeView;

import java.util.*;

import java.awt.*;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

import javax.swing.*;
import javax.swing.Timer;

import controller.Governor;

public class TimeView {
	
	//What kind of data
	public final static String INPUT = "INPUT";
	public final static String OUTPUT = "OUTPUT";
	public final static String STATE = "STATE";
	public final static String STATEVARIABLE = "STATEVARIABLE";
	public final static String SIGMA = "SIGMA";
	
	//Data type
	public final static boolean STRING = false;
	public final static boolean NUMBER = true;	
	
	private TimeGraph tg;
	private int timeUnit = 50;      //Delay time before updating the internal time
	private int graphHeight =150;   //Each Graph Height
	public Timer clock;             //Time logic for the Time View 
	private int labelInc = 10;      //Label increment
	
	/**
	 * This method generates a Time View for the selected model
	 * @param graphList
	 * @param modelName
	 */
	
	public TimeView(ArrayList graphList, String modelName, String XLabel, String TimeIncre){
		//super("Time Graph View : " + modelName);
		//Get the new label Increment and then create time graph using that info
		labelInc = Integer.parseInt(TimeIncre);		
		tg = new TimeGraph(labelInc, XLabel, modelName);
		
		//Generates selected graphs
		for(int i = 0; i < graphList.size(); ++i){
			Graph g = (Graph)graphList.get(i);
			tg.addGraph(g.getType(),g.getName(), g.getDataType(), g.getUnit());
		}			
				
		//getContentPane().setLayout(new BorderLayout());
		//getContentPane().add(tg,BorderLayout.CENTER);		
		
		//Automatically define the height of the frame depending on the number of graph
		int FrameHeight = graphList.size() * graphHeight + 90;
		
		tg.updateTime();
		internalClock();
		
		Governor.registerTimeView(this);
	}
	
	/**
	 * This method adds an event to the TimeView
	 * @param e
	 */
	public void addEvent(Event e){
		try{
			System.out.println(e.toString());
			tg.addEvent(e.getName(),e.getType(),e.getTime(),e.getData());
		}
		catch (Exception ex){
			System.out.println(ex);
		}
	}	
	
	/**
	 * This methods send the ending time to the Time View
	 */
	public void endTime(double time)
	{
		tg.endTime(time);
	}	
	
	/**
	 * This method will start to run the Time View
	 * The clock for the Time View wait for timeUnit until event occurs
	 * Refer to the JAVA API timer
	 */
	
	public void internalClock()
	{
		internalClock(timeUnit);
	}
	
	public void internalClock(int t){		
		Action incTime = new AbstractAction(){
			public void actionPerformed(ActionEvent e) {
				tg.updateTime();
			}
		};
		clock = new Timer(t, incTime);  //Wait for timeUnit and runs		
	}
	
	public void clockStop()
	{
		clock.stop();
	}
	
	public JScrollPane retTG(){
		return tg;
	}

	public boolean checkTimeGraphs()
	{
		return tg.checkTimeGraphs();
	}
	
	public void setTV(double x)
	{
		if(clock!=null)
		{
			clock.stop();
			internalClock((int)(1000/x));
		}
	}
}
