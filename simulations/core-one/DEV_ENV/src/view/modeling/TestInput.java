/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 

package view.modeling;

import GenCol.*;

/**
 * A value-port pair whose value may be injected into the associated port
 * of a viewable component during the viewing of a simulation.
 */
public class TestInput
{
    /**
     * The name of the port into which to inject the value.
     */
    public String portName;

    /**
     * The value to inject.
     */
    public entity value;

    /**
     * The amount of simulation time to wait before injecting the value.
     */
    public double e;

    /**
     * Constructor.
     */
    public TestInput(String portName_, entity value_, double e_)
    {
        portName = portName_;
        value = value_;
        e = e_;
    }

    /**
     * See parent method.
     */
    public String toString()
    {
        return "port: " + portName + ", value: " + value + ", e: " + e;
    }
}

