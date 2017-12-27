
/**
 * An atomic devs component that is capable of creating and updating a
 * graphical view of itself.
 *
 * @author  Jeff Mather
 */ 
package view.modeling;




import java.awt.*;
import java.text.DecimalFormat;
import java.util.List;
import java.util.*;

import GenCol.*;


import model.modeling.*;
import model.simulation.*;
import util.*;
import view.simView.*;
import view.*;

public class ViewableAtomic extends atomic implements ViewableComponent
{
    /**
     * Holds member variables in common with other viewable-component classes.
     * If you are looking for a member variable and can't find it, it's
     * likely in here.
     */
    protected ViewableComponentBase base = new ViewableComponentBase();

    /**
     * the parent of this atomic model
     */
  //  protected ViewableDigraph myParent;

    /**
     * get a handle for the coupled model . Not clear why ??
     */
    protected coupledDevs myCoupled;
    /**
     * A graphical view on this atomic's state.
     */
    protected AtomicView view;

    /**
     * The background color to use with this atomic's view.
     */
    protected Color backgroundColor = new Color(155, 155, 155);

    /**
     * Constructor.
     *
     * @param   name        The name to give this devs atomic component.
     */
    public ViewableAtomic(String name) {super(name);}

    /**
     * A convienence constructor.
     */
    public ViewableAtomic() {super("ViewableAtomic");}

    /**
     * Returns this atomic's sigma value as a nicely formatted string.
     */
    public String getFormattedSigma()
    {
        // if this atomic's sigma is equal to infinity
        double sigma = getSigma();
        if (sigma >= Double.POSITIVE_INFINITY) {
            return "infinity";
        }

        // return this atomic's sigma formatted to three places
        return (new DecimalFormat("0.000")).format(sigma);
    }

    /**
     * See member variable accessed.
     */
    public ComponentView getView() {return view;}

    /**
     * See member variable accessed.
     */
    public AtomicView getAtomicView() {return view;}

    /**
     * Returns this atomic's phase value as a nicely formatted string.
     */
    public String getFormattedPhase()
    {
        // if this atomic has no current phase, return null
        String phase = getPhase();
        if (phase == null) return null;

        // if this atomic's phase can be converted to a double, return
        // the double formatted to three places, otherwise just return the
        // phase the way it is
        try {
            double numericValue = Double.parseDouble(phase);
            phase = (new DecimalFormat("0.000")).format(numericValue);
        } catch (NumberFormatException e) {}
        return phase;
    }

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
     * Creates this atomic's view on itself.
     *
     * @param   modelView       The sim-view model-view that will contain the
     *                          created view.
     */
    public void createView(SimView.ModelView modelView)
    {
        // create the view
        view = new AtomicView(this, modelView);

        // if this atomic is supposed to be hidden, don't show the view
        if (isHidden()) view.setVisible(false);
    }

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
     * See member variable accessed.
     */
    public void setBackgroundColor(Color color) {backgroundColor = color;}

    /**
     * See member variable accessed.
     */
    public Color getBackgroundColor() {return backgroundColor;}

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
        return (atomicSimulator)getSim();
    }

    /**
     * See member variable accessed.
     */
    public Point getPreferredLocation() {return base.preferredLocation;}

    /**
     * See member variable accessed.
     */
    public void setPreferredLocation(Point location) {base.preferredLocation = location;}

    /**
     * See parent method.
     */
    public void setSigma(double sigma)
    {
        super.setSigma(sigma);

        // inform the view
        if (view != null) {
            view.sigmaChanged();
        }
    }

    /**
     * Returns the text that should be displayed as this atomic's tooltip.
     * This can be overridden to display any info about this atomic that is
     * desired.  Note that the expected format is HTML (so, use "<br>"
     * instead of "\n" for line breaks).
     */
    public String getTooltipText()
    {
        return "class: <font size=\"-2\">" + getClass().getName() + "</font><br>" +
            "phase: " + getFormattedPhase() + "<br>" +
            "sigma: " + getFormattedSigma() + "<br>" +
            "tL: " + getFormattedTL() + "<br>" +
            "tN: " + getFormattedTN();
    }

    /**
     * Returns this atomic's time-of-last-event value as a nicely
     * formatted string.
     */
    protected String getFormattedTL()
    {
        // return this atomic's TL value formatted to three places
        return (new DecimalFormat("0.000")).format(
            ((atomicSimulator)mySim).getTL());
    }

    /**
     * Returns this atomic's time-of-next-event value as a nicely
     * formatted string.
     */
    protected String getFormattedTN()
    {
        // return this atomic's TN value formatted to three places
        return (new DecimalFormat("0.000")).format(
            ((atomicSimulator)mySim).getTN());
    }

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
    public boolean isHidden() {return base.hidden;}

    /**
     * See member variable accessed.
     */
     public void setHidden(boolean hidden) {base.hidden = hidden;}
     
     public void addModel(IODevs iod){
         
    	 /*
    	 ViewableDigraph P = (ViewableDigraph)getParent();
         P.add(iod);
         coordinator PCoord = P.getCoordinator();
         PCoord.setNewSimulator((IOBasicDevs)iod);
         */
    	 super.addModel(iod);
    	 /*
    	 ViewableDigraph P = (ViewableDigraph)getParent();
         DigraphView dv=P.getDigraphView();
         SimView.ModelView mv= dv.getModelView();
         ViewableComponent vc= (ViewableComponent)iod;
         mv.modelAdded(vc, P);
         */
    }
   
     public void removeModel(String modelName){
                  
    	 super.removeModel(modelName);
    	 
    	 /*
    	 ViewableDigraph P = (ViewableDigraph)getParent();
         DigraphView dv=P.getDigraphView();
         SimView.ModelView mv= dv.getModelView();
         ViewableComponent vc= (ViewableComponent)P.withName(modelName);
         mv.modelRemoved(vc, P);
    	  */
         
       }

  
     //edited and modified from saurabh's code
/*
     public void setMyParent(ViewableDigraph dg){
       myParent = new ViewableDigraph("none");
       myParent =dg;
     }
*/
     public ViewableDigraph getMyParent(){return (ViewableDigraph)super.getParent();}


     public void removeInportHook(String modelName, String port){

       ViewableDigraph P = (ViewableDigraph)getParent();
       IODevs a = (IODevs)P.withName(modelName);
       System.out.print("----------------------");
       System.out.print("Inport removedVA: "+port);

       if(P.getView()!=null)
       if (a instanceof ViewableAtomic){
         ((ViewableAtomic)a).updateComponentView();
       }

     }

     public void removeOutportHook(String modelName, String port){

       ViewableDigraph P = (ViewableDigraph)getParent();
       IODevs a = (IODevs)P.withName(modelName);
       System.out.print("----------------------");
       System.out.print("Outport Removed VA: "+port);

       if(P.getView()!=null)
       if (a instanceof ViewableAtomic){
         ((ViewableAtomic)a).updateComponentView();
       }

     }

     public void addInportHook(String modelName, String port){

       ViewableDigraph P = (ViewableDigraph)getParent();
       IODevs a = (IODevs)P.withName(modelName);
       System.out.print("----------------------");
       System.out.print("Inport addedVA: "+port);

       if(P.getView()!=null)
       if (a instanceof ViewableAtomic){
         ((ViewableAtomic)a).updateComponentView();
       }
  
     }

     public void addOutportHook(String modelName, String port){

       ViewableDigraph P = (ViewableDigraph)getParent();
       IODevs a = (IODevs)P.withName(modelName);
       System.out.print("----------------------");
       System.out.print("Outport addedVA: "+port);

       if(P.getView()!=null)
       if (a instanceof ViewableAtomic){
         ((ViewableAtomic)a).updateComponentView();
       }
  
     }

     public void updateComponentView(){

       boolean goForView = false;
       ViewableDigraph parent = (ViewableDigraph)getParent();
       //System.out.print("Inside ViewableAtomic update component");
       // save the current Model Couplings
       coordinator cd = parent.getCoordinator();
       couprel savedCr = cd.getModelCoupling(this.getName());
       //if(this instanceof ViewableComponent)
       try{
         //SimView mysim = myModelView.getSim();
         goForView = true;
       }
       catch(NullPointerException ex){
         goForView = false;
         return;
       }
       
       if(goForView){
         try{
           //clear the couplings from the modelView window
           //remove the component View from the window
   
          //view.getSim().usePrevModelLayout = true;
    
          view.modelView.savingModelViewCouplingsRemove(this,savedCr);

           //create a new componentView
           //put back the saved couplings
           System.out.print("Updating the componenet: "+this.getName());
          
           view.modelView.savedModelViewCouplingsAdd(this,savedCr);
           view.modelView.repaint();
          
//            view.modelView.getSim().usePrevModelLayout = false;

         }
         catch(Exception ex){
           ex.printStackTrace();
           return;
         }
        view.modelView.repaint();
       }
     }
     
   
}


