/**
 * A digraph devs component that is capable of creating and updating a
 * graphical view of itself.
 *
 * @author  Jeff Mather
 */

package view.modeling;



import java.awt.*;
import java.util.*;
import java.util.List;

import GenCol.*;


import model.modeling.*;
import model.simulation.*;

import view.simView.*;


public class ViewableDigraph extends digraph implements ViewableComponent
{
    /**
     * Whether this digraph should be depicted as a black-box.  That is,
     * whether or not the subcomponents it contains should be displayed.
     */
    protected boolean blackBox;

    /**
     * Holds member variables in common with other viewable-component classes.
     * If you are looking for a member variable and can't find it, it's
     * likely in here.
     */
    protected ViewableComponentBase base = new ViewableComponentBase();

    /**
     * Whether this digraph's layout has been changed within a sim-view
     * since the last time that layout was saved (in this digraph's source
     * code file).
     */
    protected boolean layoutChanged = false;

    /**
     * How large this digraph would like its view to be.
     */
    protected Dimension preferredSize = new Dimension(549, 253);

    /**
     * the parent of this atomic model
     */
   // protected ViewableDigraph myParent;

    /**
     * A graphical view of this digraph.
     */
    protected DigraphView view;

    /**
     * Constructor.
     *
     * @param   name        The name to give this devs digraph component.
     */
    public ViewableDigraph(String name)
    {
        super(name);
    }

    /**
     * Creates this digraph's view on itself.
     *
     * @param   modelView       The sim-view model-view that will contain the
     *                          created view.
     */
    public void createView(SimView.ModelView modelView)
    {
        // create the view
        view = new DigraphView(this, modelView);

        // if this digraph is supposed to be hidden, don't show the view
        if (isHidden()) view.setVisible(false);
    }

    /**
     * See member variable accessed.
     */
    public Dimension getPreferredSize() {return preferredSize;}

    /**
     * See member variable accessed.
     */
    public void setPreferredSize(Dimension size)
    {
        preferredSize = size;
        layoutChanged = true;
    }

    /**
     * See member variable accessed.
     */
    public Point getPreferredLocation() {return base.preferredLocation;}

    /**
     * See member variable accessed.
     */
    public void setPreferredLocation(Point location)
    {
        base.preferredLocation = location;
    }

    /**
     * See member variable accessed.
     */
    public ComponentView getView() {return view;}

    /**
     * See member variable accessed.
     */
    public DigraphView getDigraphView() {return view;}

    /**
     * See ViewableComponent method implemented.
     */
    public List getInportNames()
    {
        return ViewableComponentUtil.getPortNames(mh.getInports());
    }

    /**
     * See ViewableComponent method implemented.
     */
    public List getOutportNames()
    {
        return ViewableComponentUtil.getPortNames(mh.getOutports());
    }

    /**
     * See full-signature method.
     */
    public void addTestInput(String portName, entity value) {
    	addTestInput(portName, value, 0);
    }

    /**
     * Creates a test input structure from the given information,
     * and adds that input structure to the list of test inputs for
     * the given port.
     *
     * @param   portName    The name of the port on which to inject the value.
     * @param   value       The value to inject.
     * @param   e           The amount of simulation time to wait before
     *                      injecting the value.
     */
    public void addTestInput(String portName, entity value, double e)
    {
    	super.addTestInput(portName, value, e);
        ViewableComponentUtil.addTestInput(portName, value, e,
            base.testInputs, base.testInputsByPortName);
    }

    /**
     * See base member variable accessed.
     */
    public List getTestInputs()
    {
        return base.testInputs;
    }

    /**
     * See ViewableComponent method implemented.
     */
    public List getTestInputs(String portName)
    {
        return (List)base.testInputsByPortName.get(portName);
    }

    /**
     * See ViewableComponent method implemented.
     */
    public atomicSimulator getSimulator()
    {
        return getCoordinator();
    }
   
    /*
    //by saurabh
    public void setMyParent(ViewableDigraph dg){
    //myParent = new ViewableDigraph("none");
     myParent =dg;
    }
*/
    public ViewableDigraph getMyParent(){return (ViewableDigraph) super.getParent();}

    public void add(ViewableAtomic iod){
        //setMyParent(this);
        super.add((IODevs)iod);
      }

      public void add(ViewableDigraph iod){
        //setMyParent(this);
        super.add((IODevs)iod);
      }
      
    /**
     * This method may be overridden to provide programmatic layout
     * of this digraph's components.
     *
     * @return  Whether the workings of this method obviate the need for
     *          the automatically generated layoutForSimView() method
     *          to be called.
     */
    public boolean layoutForSimViewOverride() {return false;}

    /**
     * See member variable accessed.
     */
    public boolean getLayoutChanged() {return layoutChanged;}

    /**
     * See member variable accessed.
     */
    public void setLayoutChanged(boolean changed) {layoutChanged = changed;}

    /**
     * See member variable accessed.
     */
    public String getLayoutName()
    {
        return base.layoutName != null ? base.layoutName :
            ViewableComponentUtil.buildLayoutName(name);
    }

    /**
     * See member variable accessed.
     */
    public void setLayoutName(String name) {base.layoutName = name;}

    /**
     * See member variable accessed.
     */
    public boolean isBlackBox() {return blackBox;}

    /**
     * See member variable accessed.
     */
    public void setBlackBox(boolean blackBox_) {blackBox = blackBox_;}

    /**
     * See member variable accessed.
     */
    public boolean isHidden() {return base.hidden;}

    /**
     * See member variable accessed.
     */
     public void setHidden(boolean hidden) {base.hidden = hidden;}

    /**
     * See ViewableComponent method implemented.
     */
    public int getNumInports()
    {
        return mh.getInports().size();
    }

    /**
     * See ViewableComponent method implemented.
     */
    public int getNumOutports()
    {
        return mh.getOutports().size();
    }
    
    /**
     * Returns the text that should be displayed as this digraph's tooltip.
     * This can be overridden to display any info about this digraph that is
     * desired.  Note that the expected format is HTML (so, use "<br>"
     * instead of "\n" for line breaks).
     */
    public String getTooltipText()
    {
        return "class: <font size=\"-2\">" + getClass().getName() + "</font>";
    }
    
    /**
     * Automatically generated by the SimView program.
     * Do not edit this manually, as such changes will get overwritten.
     */
    public void layoutForSimView()
    {
        preferredSize = new Dimension(591, 332);
        ViewableComponent vcomp = (ViewableComponent)withName("");
        if(vcomp != null)
             ((ViewableComponent)withName("")).setPreferredLocation(new Point(185, 135));
    }
}
