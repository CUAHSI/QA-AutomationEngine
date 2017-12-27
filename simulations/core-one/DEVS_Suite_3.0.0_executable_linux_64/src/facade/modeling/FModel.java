/*     
 *    
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */
package facade.modeling;

//Model Connections
import facade.simulation.FSimulator;

//Intra-Facade Connections

//Collection Connections

//Standard API Imports
import java.util.Iterator;
import java.util.Vector;
import java.util.List;
import java.util.Set;

import GenCol.ensembleBag;
import GenCol.entity;


import model.modeling.TestInput;
import model.modeling.devs;
import model.modeling.port;

import view.modeling.ViewableComponent;
import view.simView.*;

/**
 * Interface of the Facade model
 * @author  Ranjit Singh 
 * @modified Sungung Kim
 */
public abstract class FModel
{
	public static final short ATOMIC    = 0;
    public static final short COUPLED   = 1;
    
    private devs model;
    private FModel parent;
    protected FSimulator fSimulator;
    protected List inputPortNames;
    protected List outputPortNames;
    
    public static final double INFINITY = Double.MAX_VALUE;
    
    public FModel(devs model, FModel parent, FSimulator fSimulator)
    {
        this.model      = model;
        this.parent     = parent;
        this.fSimulator = fSimulator;
        
        this.inputPortNames  = extractPortNames(model.getMessageHandler().getInports());
        this.outputPortNames = extractPortNames(model.getMessageHandler().getOutports());
    }
    
    public abstract void injectInput(String portName, entity input);
    public abstract List getOutputPortContents(String portName);
    public abstract List getInputPortContents(String portName);
    public abstract double getTimeOfLastEvent();
    public abstract double getTimeOfNextEvent();
    public devs getModel(){return model;}
    
    public String getName()
    {
        return model.getName();
    }
   
    public List getInputPortNames()
    {
        return new Vector(inputPortNames);
    }
    
    public List getOutputPortNames()
    {
        return new Vector(outputPortNames);
    }
    
    public boolean isRootModel()
    {
        return getParent() == null;
    }
    
    public FModel getParent()
    {
        return parent;
    }
    
    public String toString()
    {
        return getName();
    }
    
    //returns list of entities // if nothing, empty list
    public List getInputPortTestValues(String portName)
    {
        if (inputPortNames.contains(portName))
        {
            List list = new Vector();
            List inputsForPort = model.getTestInputsForPort(portName);
            if (inputsForPort != null)
            {
                Iterator it = inputsForPort.iterator();
                while (it.hasNext())
                    list.add(((TestInput)it.next()).getValue());
            }
            return list;
        }
        else
            throw new FIllegalModelParameterException("Invalid Input Port: " + portName);
    }
  
    protected static List extractPortNames (Set ports)
    {
        List names = new Vector();
        Iterator it = ports.iterator();
        while (it.hasNext()) 
            names.add(((port)it.next()).getName());

        return names;
    }  
    
    protected static List extractEntities(ensembleBag eBag)
    {
        List list = new Vector(eBag.size());
        Iterator it = eBag.iterator();
        while (it.hasNext())
            list.add(it.next());
            
        return list;
    }
}
