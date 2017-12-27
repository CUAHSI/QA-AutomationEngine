/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */  
 

package view.timeView;

import javax.swing.JPanel;
import java.awt.BasicStroke;
import java.awt.event.ActionEvent;
import java.awt.image.BufferedImage;
import java.awt.print.*;
import java.util.*;
import java.lang.Number;



import javax.swing.AbstractAction;
import javax.swing.Action;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.Timer;

import javax.swing.*;

import controller.Stopwatch;

import view.acims.Graphics.*;
import view.acims.diagrams.*;

import java.awt.*;
import java.awt.image.BufferedImage;

/**
 * TimeGraph class actually creates the Time View based on the information
 * @modified Sungung Kim
 *
 */
public class TimeGraph extends JScrollPane implements Printable{
	//Diagram
	private Diagram graphsDisplay;
	private TimeGraphAttributeSet att;
	
	//Each graph in the Time View
	private ArrayList graphs = new ArrayList();
	
	private String XaxisLabel = "Time";       //Default x-axis label
	
	private int numLabels = 10;               //number of labels shown on the screen	
	
	private int graphXStart = 30;             //X-axis for each graph
	private int graphXEnd = 780;
	
	private int graphY = 80;                  //Y-axis for each graph
	private int graphStartY = 125;
	
	private int graphSeparation = 150;	      // seperation between each graph
	
	private double curTime = 0;               //Current time
	private double endingTime = 0;            //Ending Time
	
	private double labelIncrement = 10;       //default label increment 
	
	private double timeStart = 0;             // displayed time on the screen
	private double timeEnd = labelIncrement*numLabels;
	
	private double xIncrement = ((graphXEnd-graphXStart)/
								(numLabels*labelIncrement));
	
	private double timeIncrement = 1;         //logic time increment
	
	private String modelName="";
	
	/**
	 * Create Time Graph with attributes for each model
	 * @param lblInc
	 * @param XLabel
	 */
	
	public TimeGraph(int lblInc, String XLabel, String _modelName){
		
		modelName=_modelName;
		//TimeGraph Attributes class
		att = new TimeGraphAttributeSet();
		
		//If no value is assigned to the x-axis label, set as N/A, otherwise "Time [units]"
		if(XLabel.equalsIgnoreCase(""))
			XLabel = "N/A";
		
		XaxisLabel = XaxisLabel + " [" +XLabel +"]"; 
		
		graphsDisplay = new Diagram(" ",att);
		att.setComponentType(TimeGraphAttributeSet.frame);
		graphsDisplay.setBackgroundComponent(TimeGraphAttributeSet.frame,"graph");
		setLabelIncrement(lblInc);
		setViewportView(graphsDisplay);
	}
	
	/**
	 * Selt label increment
	 * @param inc
	 */	
	public void setLabelIncrement(double inc){
		labelIncrement = inc;
		xIncrement = ((graphXEnd-graphXStart)/
				(numLabels*labelIncrement));
		timeIncrement = (labelIncrement/5);
		timeStart = curTime;       //time displayed on the leftmost side
		timeEnd = (labelIncrement*numLabels)+ timeStart;  //Time displayed on the right most side
		att.setUnitLabels(generateLabels());  //generate label and set to the graph
	}
	
	/**
	 * This class adds a graph for each user selected data(input/output ports, state variables, and etc)
	 * @param typ
	 * @param lb
	 * @param dataType
	 * @param graphUnit
	 */
	public void addGraph(String typ, String lb, boolean dataType, String graphUnit){
		GraphData gd;
		graphs.add(gd = new GraphData(typ,lb, graphs.size(), graphUnit));
		gd.setNumber(dataType);
	}
	
	/**
	 * Draw the entire time graph based on the user selection
	 */
	private int drawGraphs(){
		
		int before=0, after=0;
		for(int i = 0; i < graphs.size();i++){
			before=((GraphData)graphs.get(i)).getNextSize();
			((GraphData)graphs.get(i)).updateLists();   //make the graph move to the next
			((GraphData)graphs.get(i)).drawGraphData();
			after=((GraphData)graphs.get(i)).getNextSize();
			//System.out.println("#"+timeStart+" / "+timeEnd+" / "+curTime+" / "+endingTime);
		}
		if(before>0 && after==0)
			return 1;
		else
			return 0;
	}
	
	public boolean checkTimeGraphs()
	{
		for(int i=0; i<graphs.size(); i++)
		{
			if(((GraphData)graphs.get(i)).getNextSize()>0)
				return false;
		}
		return true;
	}
	
	/**
	 * add an event into the correspoinding graph
	 * @param nm
	 * @param typ
	 * @param tm
	 * @param dat
	 */	
	public void addEvent(String nm, String typ, double tm, String dat){
		for(int i = 0; i < graphs.size(); ++i){
			GraphData gd = (GraphData)graphs.get(i);
			if((gd.name).equals(nm)){   //Found the graph
				gd.addEvent(tm,dat);
				i = graphs.size();
			}
		}
	}
	
	//Ending time always should be bigger than actual ending time so that we can see all data
	public void endTime(double time){
		endingTime = time+1;
	}
	
	//Update time and by calling this method, the graph will be cleared and drawed again
	//basically at the moment every event occurs, time will be updated
	private int last_ret=0;
	
	public int updateTime(){
		int ret=0;
		
		if(curTime < endingTime)  //Ending time is the time to stop updating the TimeGraph
			curTime += timeIncrement;
		
		if(curTime > timeEnd){// && curTime <= endingTime){  //TimeEnd is the last label on the graph
			timeStart += timeIncrement;
			timeEnd += timeIncrement;
			att.setUnitLabels(generateLabels());
		}
		
		//Update time and draw graph again
		if (curTime <= endingTime || !checkTimeGraphs()){	
			graphsDisplay.clearDiagram();
			ret=drawGraphs();
			//if(ret==1)	System.out.println("         "+modelName+" V TIME: "+Stopwatch.lap()+" sec");
			graphsDisplay.drawDiagram(XaxisLabel);
		}
				
		return ret;
	}
	
	/**
	 * Generate labels and store into the list
	 * @return
	 */
	private Vector generateLabels(){
		Vector result = new Vector(numLabels+1);
		double shift = (labelIncrement-(timeStart%labelIncrement));
		result.add(new Integer((int)(shift*xIncrement)));
		result.add(new Integer((int)(labelIncrement*xIncrement)));
		for(int i = 0; i < numLabels; ++i){
			String t = Double.toString((i*labelIncrement)+timeStart+shift);
			if(t.length() > 10){
				t = t.substring(0,9);
			}
			result.add(t);
		}
		return result;
	}
	
	public int print(Graphics g, PageFormat pf, int pageIndex) {
		if (pageIndex != 0) return NO_SUCH_PAGE;
		Graphics2D g2 = (Graphics2D)g;
		double pageHeight = pf.getImageableHeight();
		double pageWidth = pf.getImageableWidth();
		double tableWidth = getSize().width;
		double scale = 1;
		if (tableWidth >= pageWidth) {
			scale = pageWidth/tableWidth;
		}
		double tableWidthOnPage=tableWidth*scale;
		g2.translate(pf.getImageableX(), pf.getImageableY());
		g2.setClip(0,(int)(pageHeight*pageIndex), (int) Math.ceil(tableWidthOnPage),
	              (int) Math.ceil(pageHeight));

		g2.scale(scale,scale);
		paint(g2);
		return PAGE_EXISTS;
	}
	
	public void printImage() {
		PrinterJob pj = PrinterJob.getPrinterJob();
		pj.setPrintable(this);
		if (pj.printDialog()) {
			try {
				pj.print();
			}
			catch (Exception pe) {
				System.out.println(pe);
			}
		}
	}
	
	/**
	 * Inner Class: Construct Time Graph and Draw Data
	 */	
	private class GraphData{
		private ArrayList previous = new ArrayList();
		private ArrayList current = new ArrayList();
		private ArrayList next = new ArrayList();
		private ArrayList levels = new ArrayList();
		private DataStructureOps ops = new DataStructureOps();
		private String previousState;
		public String graphUnit = "";
		private String type = "";
		private String name = "";
		private double top = 0;
		private double bottom = 0;
		private boolean isNumber = true;
		private boolean isFirst = true;
		private int graphNum = 0;
		private String lastmessage="", message;	//for debugging purposes only
		
		GraphData(String typ, String nm, int num, String gUnit){
			previousState = " ";
			type = typ;
			graphNum = num;
			graphUnit = gUnit;
			name = nm;
		}
		
		/**
		 * This method update the Time View so that it will move to the right		 *
		 */
		public void updateLists(){
			while((next.size() > 0)&&(((ModelEvent)ops.peekEnd(next)).time <= curTime)){
				ops.addFront(ops.removeEnd(next),current);
			}
			while((current.size() > 0)&&((ModelEvent)ops.peekEnd(current)).time < timeStart){
				ops.addFront(ops.removeEnd(current),previous);
			}
			while((previous.size() > 0)&&((ModelEvent)ops.peekFront(previous)).time >= timeStart){
				ops.addEnd(ops.removeFront(previous),current);
			}
			while((current.size() > 0)&&((ModelEvent)ops.peekFront(current)).time > curTime){
				ops.addEnd(ops.removeFront(current),next);
			}
/*			message=timeStart+" ( "+timeIncrement+" ) "+timeEnd+" | "+
					curTime+", "+endingTime+" | "+
					((previous.size()>0)?((ModelEvent)ops.peekFront(previous)).time:"---")+", "+
					((current.size()>0)?((ModelEvent)ops.peekEnd(current)).time:"---")+", "+
					((current.size()>0)?((ModelEvent)ops.peekFront(current)).time:"---")+", "+
					((next.size()>0)?((ModelEvent)ops.peekEnd(next)).time:"---")+" | ";
			if(!lastmessage.equals(message))
				System.out.println(message);
			lastmessage=message;*/
		}
		
		public int getNextSize()
		{	
			//System.out.println(name+"="+previous.size()+"/"+current.size()+"/"+next.size());
			return next.size();

		}
		
		/**
		 * add event to the list with current level
		 * @param t
		 * @param dat
		 */
		public void addEvent(double t, String dat){
			double temp = 0;
			if(isNumber){				
				temp = Double.parseDouble(dat);			
				
				if(Double.isInfinite(temp)){  //if the data is infinite, then set the value as -0.1
					temp = -1;				
				}				
				
				//If this event is the first
				if((previous.size() == 0) && (current.size() == 0)
						&& (next.size() == 0)){
					bottom = 1;   
				}
				
				//if the value is bigger than top, set this value as the top
				//or this value is smaller than bottom, set this value as the bottom
				if(temp > top){
					top = temp;
				}
				else if(temp < bottom){
					bottom = temp;
				}
			}
			else{   // If data is string, set level
				temp = top;   //current top
				++top;    
				
				for(int i = 0; i < levels.size();++i){
					if(((String)(levels.get(i))).equals(dat)){ // keep the level since data is the same
						temp = i+1;
						--top;
					}
				}
				
				if(top > levels.size()){
					levels.add(dat);
					temp = top;
				}
			}
			
			//Add an event to the data structure 
			ops.addFront(new ModelEvent(t, dat,temp), next);
			updateLists();
		}
		
		public String getType(){
			return type;
		}
		
		public String getName(){
			return name;
		}
		public void setNumber(boolean isNumb){
			isNumber = isNumb;
		}
		
		private int getXTime(double t){
			return (int)(((t-timeStart)*xIncrement)+graphXStart);
		}
		
		private int getYLevel(double level){
			return (int)((level*graphY)/(top-bottom));
		}
		
		/**
		 * Draw the graphs & add the event
		 */
		private void drawGraphData(){
			int height = 40;
			double previousLevel = 0;
			int previousX = getXTime(timeStart);   //get previous x (time)
			
			String previousData = "  ";
			String iStr = "";
			
			att.setRelationType(TimeGraphAttributeSet.xAxis);
			att.setComponentType(TimeGraphAttributeSet.dataPoint);  //this is data point
			
			Point origin = new Point(graphXStart,(graphNum+1)*graphSeparation);
			Point end = new Point(graphXEnd,(graphNum+1)*graphSeparation);
			
			String orgName = Integer.toString(graphNum)+"O";
			String endName = Integer.toString(graphNum)+"E";
			
			graphsDisplay.addDComponent(orgName,origin);
			graphsDisplay.addDComponent(endName,end);
			
			//Add label for each graph with unit
			graphsDisplay.addRelationship(name + "  [" + graphUnit +"]",orgName,endName);
			
			//if there was data previously, then get previous data
			if(previous.size() > 0){
				previousLevel = ((ModelEvent)(previous.get(0))).level;
				previousData = ((ModelEvent)(previous.get(0))).data;
			}
			
			//Draw the data on the corresponding graph
			for(int i = 0; i < current.size(); ++i){
				ModelEvent me = (ModelEvent)current.get(i);
				iStr = Integer.toString(i);
				while((i < (current.size()-1)) &&
					  (me.time == ((ModelEvent)current.get(i+1)).time)){
					current.remove(i+1);
				}
				
				//If data type is input or output, then draw arrow
				if(type.equals(TimeView.INPUT) ||
				   type.equals(TimeView.OUTPUT)){
					int a = getXTime(me.getTime());   //current time
					int b = (graphNum+1)*graphSeparation;  //graph number
					
					//Set attributes
					att.setRelationType(TimeGraphAttributeSet.eventArrow);
					att.setComponentType(TimeGraphAttributeSet.dataPoint);
					att.setDataLabelVisible(false);
					
					//Draw graph
					graphsDisplay.addDComponent("a"+name+iStr,new Point(a,b));
					b -= height;
					graphsDisplay.addDComponent("b"+name+iStr,new Point(a,b));
					graphsDisplay.addRelationship(me.getData(),"a"+name+iStr,"b"+name+iStr);
				}
				// if data type is state or statevariable, then line graph
				else if(type.equals(TimeView.STATE)||
						type.equals(TimeView.STATEVARIABLE)){
					//(x1, y1)
					int x1 = previousX;
					int y1 = ((graphNum+1)*graphSeparation)-getYLevel(previousLevel);
					
					//(x2, y2)
					me = (ModelEvent)current.get(current.size()-i-1);
					int x2 = getXTime(me.time);
					int y2 = ((graphNum+1)*graphSeparation)-getYLevel(me.getLevel());
					previousX = x2;
					previousLevel = me.getLevel();
					
					//Set attributes
					att.setRelationType(TimeGraphAttributeSet.vGraphLine);
					att.setComponentType(TimeGraphAttributeSet.dataPoint);
					att.setDataLabelVisible(false);
					
					//Draw graph
					graphsDisplay.addDComponent("a"+name+iStr,new Point(x1,y1));  //previous point
					graphsDisplay.addDComponent("b"+name+iStr,new Point(x2,y1));  //horizontal point to the next point
					graphsDisplay.addDComponent("c"+name+iStr,new Point(x2,y2));  //vertical poin to the next point
					graphsDisplay.addRelationship(previousData,"a"+name+iStr,"b"+name+iStr);
					
					//If the current state is the same as the previous, don't display
					String stateName = me.getData();  //get current state
									
					if(previousState.equalsIgnoreCase(stateName)){ //equal to the previous
						previousData = "  ";  // nothing will be displayed 
					}
					else{
						previousData = stateName;  //Display new state
						previousState = stateName;  //memory the current state so that we can check later
					}									
					att.setRelationType(TimeGraphAttributeSet.hGraphLine);
					graphsDisplay.addRelationship(" ","b"+name+iStr,"c"+name+iStr);
				}
			}
		}
		
		/**
		 * Inner class for events
		 */
		
		class DataStructureOps{
			public void addEnd(Object o, ArrayList v){
				v.add(o);
			}
			public Object peekFront(ArrayList v){
				if(!empty(v)){
					return v.get(0);
				}
				return null;
			}
			public Object removeFront(ArrayList v){
				if(!empty(v)){
					return v.remove(0);
				}
				return null;
			}
		
			public boolean empty(ArrayList v){
				return (v.size() <= 0);
			}
		
			public void addFront(Object o, ArrayList v){
				v.add(0,o);
			}
		
			public Object peekEnd(ArrayList v){
				if(!empty(v)){
					return v.get(v.size()-1);
				}
				return null;
			}
			public Object removeEnd(ArrayList v){
				if(!empty(v)){
					return v.remove(v.size()-1);
				}
				return null;
			}
		}
	}
	
	/**
	 * 	Inner class for the event data structure 
	 *  which is storing the time, data, and level
	 */
	private class ModelEvent{
		private double time;
		private String data = "";
		private double level;
		
		ModelEvent(double t, String dat, double lvl){
			time = t;
			data = dat;
			level = lvl;
		}
		
		public double getTime(){
			return time;
		}
		public String getData(){
			return data;
		}
		public double getLevel(){
			return level;
		}
		public int display(){
			if(time < timeStart){
				return -1;
			}
			if(time > timeStart){
				return 1;
			}
			return 0;
		}
		
	}
	
}
