/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
package view;

/**
 * Facade Connections
 * Tracker: tracks data from the facade layer
 */
import facade.modeling.*;
import view.timeView.Event;








//Standard API Imports
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;

import GenCol.*;
import model.modeling.content;
import model.modeling.message;
import view.timeView.*;

import java.util.HashMap;
import java.util.List;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.ArrayList;

public class Tracker
{
    private boolean trackPhase;
    private boolean trackSigma;
    private boolean trackTL;
    private boolean trackTN;
    
    private boolean isTimeViewSelected;
    private boolean istrackinglogselected;   //to make one tracking log panel
    
   
    private boolean isBreakout = false;
    
    
    private int modelNum;
    private Event e;
    private double time;
    private double TN;
    
    private boolean atLeastOneInputTracked;
    private boolean atLeastOneOutputTracked;
    private boolean[] trackInputPorts;
    private boolean[] trackOutputPorts;
    private List timeViewData;
    private List[] dataStorage;
    private String[] dataHeaderList;
    private boolean isAtomic;
    private int uniqueID;
   
    private TrackingControl trackingControl;   
    private FModel model;    
    private String xUnit = "sec";
    private String timeIncr = "10";
    
    
     private  JList inputJList;  
     private JList copyJList; 
     private JButton copyJButton; 
     private Object[] trackInputPorts1;
     
     private ArrayList graphs = new ArrayList();
     private String[] inputPortUnits;
     private String[] outputPortUnits;
     
    public Tracker (FModel model, int num)
    {
        this.model = model;
        modelNum = num;      //model number for this tracker
        TN = 0;
        
        trackPhase = false;
        trackSigma = false;
        trackTL    = false;
        trackTN    = false;
        atLeastOneInputTracked = false;
        atLeastOneOutputTracked = false;
        trackInputPorts  = new boolean[model.getInputPortNames().size()];
        trackOutputPorts = new boolean[model.getOutputPortNames().size()];   
        inputPortUnits = new String[model.getInputPortNames().size()];
        for(int i =0; i<inputPortUnits.length;i++)
        {
        	inputPortUnits[i]="";
        }
        outputPortUnits = new String[model.getOutputPortNames().size()];
        for(int i =0; i<outputPortUnits.length;i++)
        {
        	outputPortUnits[i]="";
        }
        isTimeViewSelected = false;
        istrackinglogselected = false;
        
        //added
       
        
        for (int i = 0; i < trackInputPorts.length; i++)
            trackInputPorts[i] = false;
        for (int i = 0; i < trackOutputPorts.length; i++)
            trackOutputPorts[i] = false;
        
        uniqueID = 0;
        isAtomic = model instanceof FAtomicModel;
                
        trackingControl = new TrackingControl();       
        
        ArrayList dataStore  = new ArrayList(10);
        ArrayList dataHeader = new ArrayList(10); 
        dataStore.add(new LinkedList()); //Phase
        dataHeader.add("Phase");
        dataStore.add(new LinkedList()); //Sigma
        dataHeader.add("Sigma");
        
        dataStore.add(new LinkedList()); //TL
        dataHeader.add("TL");
        dataStore.add(new LinkedList()); //TN
        dataHeader.add("TN");
        
        List inputPortNames = model.getInputPortNames();
        for (int i = 0; i < inputPortNames.size(); i++)
        {
            dataStore.add(new LinkedList()); //Next InputPort
            dataHeader.add((String)inputPortNames.get(i));
        }
        
        List outputPortNames = model.getOutputPortNames();
        for (int i = 0; i < outputPortNames.size(); i++)
        {
            dataStore.add(new LinkedList()); //Next OutputPort
            dataHeader.add((String)outputPortNames.get(i));
        }
        
        dataStorage = (List[])dataStore.toArray(new LinkedList[0]);
        dataHeaderList = (String[])dataHeader.toArray(new String[0]);
    }
    
    
    
    public String toString()
    {
        return model.getName();
    }
    
    public FModel getAttachedModel()
    {
        return model;
    }
    
    public List[] getDataStorage()
    {
        return dataStorage;
    }
    
    public String[] getDataHeaders()
    {
        return dataHeaderList;
    }
    
    public void saveCurrentTrackingState(double currentTime)
    {    	
    	//time = currentTime;
    	int offset = 4;
        if (isAtomic)
        {
            FAtomicModel atomic = (FAtomicModel)model;
            dataStorage[0].add((trackPhase) ? atomic.getPhase() : null);
            dataStorage[1].add((trackSigma) ? ""+atomic.getSigma() : null);            
            
        }
        else
        {
            dataStorage[0].add(null);
            dataStorage[1].add(null);
        }
        dataStorage[2].add((trackTL) ? ""+model.getTimeOfLastEvent() : null);
        dataStorage[3].add((trackTN) ? ""+model.getTimeOfLastEvent() : null);
        
        List inputPorts = model.getInputPortNames();
        for (int i = 0; i < inputPorts.size(); i++)
        {
            if (trackInputPorts[i])
            {
                String tmp = "";
                Iterator it = model.getInputPortContents((String)inputPorts.get(i)).iterator();
                while (it.hasNext())
                    tmp+="{"+it.next()+"} ";
                dataStorage[offset++].add((tmp.length() == 0) ? null : tmp);
            }
            else
                dataStorage[offset++].add(null);
        }
        
        List outputPorts = model.getOutputPortNames();
        for (int i = 0; i < outputPorts.size(); i++)
        {
            if (trackOutputPorts[i])
            {
                String tmp = "";
                Iterator it = model.getOutputPortContents((String)outputPorts.get(i)).iterator();
                while (it.hasNext())
                    tmp+="{"+it.next()+"} ";
                dataStorage[offset++].add((tmp.length() == 0) ? null : tmp);
            }
            else
                dataStorage[offset++].add(null);
        }
    }
    
    public String getCurrentTrackingHTMLString()
    {
        String html = "";
        if (isAtomic)
        {
            FAtomicModel atomic = (FAtomicModel)model;
            if (trackPhase)
                html+="<B>Phase:</B> "+atomic.getPhase()+"<BR>";                
            
            if (trackSigma)
                html+="<B>Sigma:</B> "+atomic.getSigma()+"<BR>";                           
        }     
        
        if (trackTL)
            html+="<B>TL:</B> "+model.getTimeOfLastEvent()+"<BR>";          
        
        if (trackTN)
            html+="<B>TN:</B> "+model.getTimeOfNextEvent()+"<BR>";
        if (atLeastOneInputTracked)
        {
            html+="<B>Input Ports:</B><BR> ";
            List inputPorts = model.getInputPortNames();
            for (int i =0; i < inputPorts.size(); i++)
            {
                if (trackInputPorts[i])
                {
                    html+=inputPorts.get(i)+": ";
                    Iterator it = model.getInputPortContents((String)inputPorts.get(i)).iterator();
                    while (it.hasNext())
                        html+="{"+it.next()+"} ";
                    html+="<BR>";
                }
            }
        }
        if (atLeastOneOutputTracked)
        {
            html+="<B>Output Ports:</B> <BR>";
            List outputPorts = model.getOutputPortNames();
            for (int i =0; i < outputPorts.size(); i++)
            {
                if (trackOutputPorts[i])
                {
                    html+=outputPorts.get(i)+": ";
                    Iterator it = model.getOutputPortContents((String)outputPorts.get(i)).iterator();
                    while (it.hasNext())
                        html+="{"+it.next()+"} ";
                    html+="<BR>";
                }
            }
        }
        
        
        return html; 
    }
    
    public List getCurrentTimeViewData(double currentTime){
    	timeViewData = new ArrayList(1);
    	time = currentTime;
    	if (isAtomic)
        {
            FAtomicModel atomic = (FAtomicModel)model;
            if (trackPhase){
                e = new Event("Phase","STATE",time, atomic.getPhase()); 
                timeViewData.add(e);                
            }
            if (trackSigma){
                e = new Event("Sigma","SIGMA",time, String.valueOf(atomic.getSigma())); 
                timeViewData.add(e);               
            }                
        }      
        
        if (trackTL){            
            e = new Event("tL","STATEVARIABLE",time, String.valueOf(model.getTimeOfLastEvent())); 
            timeViewData.add(e);          
        }
        
        if (trackTN){
        	        	
        	e = new Event("tN","STATEVARIABLE",time, String.valueOf(model.getTimeOfNextEvent())); 
        	timeViewData.add(e);   
        }
            
        if (atLeastOneInputTracked)
        {
            List inputPorts = model.getInputPortNames();
            for (int i =0; i < inputPorts.size(); i++)
            {
                if (trackInputPorts[i])
                {
                	Iterator it = model.getInputPortContents((String)inputPorts.get(i)).iterator();
                	if(it.hasNext())
                	{
                		e = new Event(inputPorts.get(i).toString(),"INPUT", time, it.next()); 
                		timeViewData.add(e);
                	}                   
                }
            }
        }
        
        if (atLeastOneOutputTracked)
        {
            
            List outputPorts = model.getOutputPortNames();
            for (int i =0; i < outputPorts.size(); i++)
            {
                if (trackOutputPorts[i])
                {
                	Iterator it = model.getOutputPortContents((String)outputPorts.get(i)).iterator();
                   	
                	if(it.hasNext())
                	{
                		
                		//change to object
                		e = new Event(outputPorts.get(i).toString(),"OUTPUT", time, it.next()); 
                		timeViewData.add(e);
                	}                      
                }
            }
        } 
        
        return timeViewData;
    }
    
    public boolean isTrackingSelected(){
    	return istrackinglogselected;
    }
    
    public boolean isTimeViewSelected(){
    	return isTimeViewSelected;
    }   
    
    
    
    
    public boolean getTrackPhase()
    {
    	return trackPhase;
    }
    
    public void setTrackPhase(boolean set)
    {
    	trackPhase=set;
    }
    
    public boolean getTrackSigma()
    {
    	return trackSigma;
    }
    
    public void setTrackSigma(boolean set)
    {
    	trackSigma=set;
    }
    
    public void setTrackTL(boolean set)
    {
    	trackTL=set;
    }
    
    public boolean getTrackTL()
    {
    	return trackTL;
    }
    
    public boolean getTrackTN(){
    	return trackTN;
    }
    
    public void setTrackTN(boolean set){
        trackTN=set;
       }
    
    public void setTimeViewSelected(boolean set){
     isTimeViewSelected=set;
    }
    
    public boolean getTimeViewSelected(){
    	return isTimeViewSelected;
    }
    
    public void setTrackingLogSelected(boolean set){
    	istrackinglogselected=set;
       }
       
       public boolean getTrackingLogSelected(){
       	return istrackinglogselected;
       }
       
    
    public TrackingControl getTrackingControl()
    {
    	return trackingControl;
    }
    
    public int getModelNum()
    {
    	return modelNum;
    }
    
     public boolean[] gettrackInputPorts()
     {
    	 return trackInputPorts;
     }
     
     public void settrackInputPorts(boolean[] trackInputPorts)
     {
    	this. trackInputPorts= trackInputPorts;
     }
     
     public boolean[] gettrackOutputPorts()
     {
    	 return trackOutputPorts;
     }
     
     public void settrackOutputPorts(boolean[] trackOutputPorts)
     {
    	this. trackOutputPorts= trackOutputPorts;
     }
    
     public void setGraphs(ArrayList graphs)
     {
    	 this.graphs=graphs;
     }
     
     public ArrayList getGraphs()
     {
    	 return graphs;
     }
     public String getxUnit()
     {
    	 return xUnit;
     }
     public void setxUnit(String unit)
     {
    	 xUnit=unit;
     }
     public String gettimeIncrement()
     {
    	 return timeIncr;
     }
     public void settimeIncrement(String tInc)
     {
    	 timeIncr=tInc;
     }
     public void setisBreakout(boolean set)
     {
    	 isBreakout=set;
     }
     public boolean getisBreakout()
     {
    	 return isBreakout;
     }
     
     public String[] getInputPortUnits()
     {
    	 return inputPortUnits;
     }
     public void setInputPortUnits(String[] units)
     {
    	 inputPortUnits=units;
     }
     
     public String[] getOutputPortUnits()
     {
    	 return outputPortUnits;
     }
     public void setOutputPortUnits(String[] units)
     {
    	 outputPortUnits=units;
     }
     public void setatLeastOneInputTracked(boolean set)
     {
    	 atLeastOneInputTracked= set;
     }
     public boolean getatLeastOneInputTracked(boolean set)
     {
    	 return atLeastOneInputTracked;
     }
     public void setatLeastOneOutputTracked(boolean set)
     {
    	 atLeastOneOutputTracked= set;
     }
     public boolean getatLeastOneOutputTracked(boolean set)
     {
    	 return atLeastOneOutputTracked;
     }
     
}