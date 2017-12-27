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
import java.util.Vector;
import java.util.List;

import GenCol.entity;


import model.modeling.IOBasicDevs;
import model.modeling.atomic;
import model.modeling.componentIterator;
import model.modeling.digraph;
import model.simulation.atomicSimulator;

import view.modeling.ViewableAtomic;
import view.modeling.ViewableDigraph;
import view.simView.*;

/**
 * FCoupled Model which contains a ViewableDigraph model for the SimView
 * @author  Ranjit Singh 
 * @modified by Sungung Kim 05/29/2008
 */
public class FCoupledModel extends FModel
{
    private ViewableDigraph model;
    private Vector childComponents;
    
    public FCoupledModel(ViewableDigraph model, FSimulator simulator) 
    {
        this(model,null,simulator);
    }
    
    public FCoupledModel(ViewableDigraph model, FModel parent, FSimulator simulator) 
    {
        super(model,parent,simulator);
        this.model = model;
        this.childComponents = createChildModels(model,this,simulator);
    }
    
    public ViewableDigraph getModel(){
    	return model;
    }    
    
    public List getChildren()
    {
        return new Vector(childComponents);
    }
    
    public double getTimeOfNextEvent() 
    {
        return((atomicSimulator)model.getCoordinator()).getTN();
    }
    
    public double getTimeOfLastEvent() 
    {
        return((atomicSimulator)model.getCoordinator()).getTL();
    }
    
    public List getOutputPortContents(String portName) 
    {
         if (outputPortNames.contains(portName))
            return extractEntities(model.getCoordinator()
                                   .getOutput().valuesOnPort(portName));
        else
            throw new FIllegalModelParameterException("Invalid Output Port: " + portName);
    }
    
    public List getInputPortContents(String portName) 
    {
        if (inputPortNames.contains(portName))
            return extractEntities(model.getCoordinator()
                                   .getInput().valuesOnPort(portName));
        else
            throw new FIllegalModelParameterException("Invalid Input Port: " + portName);
    }
    
    public void injectInput(String portName, entity input) 
    {
        if (inputPortNames.contains(portName))
        {
            short currentState = fSimulator.getCurrentState();
            if (currentState == FSimulator.STATE_INITIAL)
            {
                if (isRootModel())
                {
                    model.getCoordinator().simInject(0,portName,input);
                }
                else
                    throw new FModelException("Can only [Inject Input] from the Root " 
                                               + "Coupled Model.");
            }
            else
                throw new FIllegalSimulatorStateException("Can only [Inject Input] from state:"
                                                          + "{Initial}.");
        }
        else
            throw new FIllegalModelParameterException("Invalid Input Port: " + portName);
    }
    
    
    
    private static Vector createChildModels(digraph model, 
                                            FModel fModel, 
                                            FSimulator fSimulator)
    {
        Vector vector = new Vector();
        componentIterator it = model.getComponents().cIterator();
        while (it.hasNext())
        {
            IOBasicDevs next = it.nextComponent();
            if (next instanceof ViewableAtomic)
                vector.add(new FAtomicModel((ViewableAtomic)next,fModel,fSimulator));
            else if (next instanceof ViewableDigraph)
                vector.add(new FCoupledModel((ViewableDigraph)next,fModel,fSimulator));
            else
                throw new FModelException("Unknown Model Type: " + next.getName());
        }
        return vector;
    }
}