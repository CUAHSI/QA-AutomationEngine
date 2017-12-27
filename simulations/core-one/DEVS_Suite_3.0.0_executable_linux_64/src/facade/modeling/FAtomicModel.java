/*     
 *    
 *  Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */
package facade.modeling;

//Model Connections
import facade.simulation.FIllegalSimulatorStateException;
import facade.simulation.FSimulator;

//Intra-Facade Connections

//Collection Connections

//Standard API Imports
import java.util.List;

import GenCol.entity;


import model.modeling.ContentInterface;
import model.modeling.atomic;
import model.simulation.atomicSimulator;

import view.modeling.ViewableAtomic;
import view.simView.*;


/**
 * FAtomice Model which contains a ViewableAtomice model for SimView
 * @author  Ranjit Singh
 * @modified by Sungung Kim 05/29/2008
 */
public class FAtomicModel extends FModel
{
    private ViewableAtomic model;
    
    /** Constructs this AtomicModel wrapper for a specific
     * atomic model.
     */    
    public FAtomicModel(ViewableAtomic model, FSimulator simulator) 
    {
        this(model,null,simulator);
    }
    
    public FAtomicModel(ViewableAtomic model, FModel parent, FSimulator simulator) 
    {
        super(model,parent,simulator);
        this.model = model;
    }
    
    public ViewableAtomic getModel(){
    	return model;
    }  
    
    public double getSigma()
    {
        return model.getSigma();
    }
    
    public void setSigma(double sigma)
    {
        model.setSigma(sigma);
    }
    
    public String getPhase()
    {
        return model.getPhase();
    }
    
    public double getTimeOfNextEvent() 
    {
        return ((atomicSimulator)model.getSim()).getTN();
    }
    
    public double getTimeOfLastEvent() 
    {
        return ((atomicSimulator)model.getSim()).getTL();
    }
    
    //returns list of entities
    public List getInputPortContents(String portName) 
    {
        if (inputPortNames.contains(portName))
            return extractEntities(((atomicSimulator)model.getSim())
                                     .getInput().valuesOnPort(portName));
        else
            throw new FIllegalModelParameterException("Invalid Input Port: " + portName);
    }
    
    //returns list of entities
    public List getOutputPortContents(String portName) 
    {     
        if (outputPortNames.contains(portName))
            return extractEntities(((atomicSimulator)model.getSim())
                                     .getOutput().valuesOnPort(portName));
        else
            throw new FIllegalModelParameterException("Invalid Output Port: " + portName);
    }

    public void injectInput(String portName, entity input) 
    {
        if (inputPortNames.contains(portName))
        {
            short currentState = fSimulator.getCurrentState();
           
            if (currentState == FSimulator.STATE_INITIAL || 
            	currentState == FSimulator.STATE_PAUSE   ||
            	currentState == FSimulator.STATE_END)
            {
                ((atomicSimulator)model.getSim()).simInject(0,portName,input);
            }
            else
                throw new FIllegalSimulatorStateException("Can only [Inject Input] from state:"
                                                          + "{Initial}.");
        }
        else
            throw new FIllegalModelParameterException("Invalid Input Port: " + portName);
    }
    
}
