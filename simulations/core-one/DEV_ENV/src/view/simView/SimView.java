
/**
 * An application that displays the execution of a simulation employing
 * a coupled devs model.
 * 
 * This Class is integrated into the Tracking Environment
 * so, several methods or functionalities from the origin removed
 *
 * @author      Jeff Mather
 * @modified Sungung Kim
 */

package view.simView;

import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.io.*;
import java.net.URL;
import javax.swing.*;
import javax.swing.text.*;
import javax.swing.event.*;

import GenCol.*;


import model.modeling.*;
import model.simulation.*;
import model.simulation.realTime.*;

import controller.ControllerInterface;

import java.text.DecimalFormat;
import java.util.*;
import java.util.List;

import facade.modeling.*;
import facade.simulation.*;
import facade.simulation.hooks.*;

import controller.simulation.SimViewCoordinator;
import util.*;
import view.*;
import view.modeling.AtomicView;
import view.modeling.ComponentView;
import view.modeling.ContentView;
import view.modeling.DigraphView;
import view.modeling.DragViewListener;
import view.modeling.ViewableAtomic;
import view.modeling.ViewableComponent;
import view.modeling.ViewableDigraph;
import view.modeling.DynamicStructureViewer;

public class SimView
{	
	/**
     * Whether to always show couplings between components, or just when
     * the mouse is over one of them.
     */
    static public boolean alwaysShowCouplings = false;
    
    /**
     * The panel which displays the components of the current model, along
     * with the scrollpane containing that panel.
     */
    static public ModelView modelView;
    
    //This variable control the speed of message movement.
    static public double speed = 5;

    /**
     * The width of the border (in pixels) between the top-level model being
     * viewed and the model-view.
     */
    protected final int modelBorderWidth = 5;

    /**
     * The name given to the default digraph that this sim-view uses to
     * wrap single atomic models that are to be viewed.
     */
    protected String wrapperDigraphName = "wrapper digraph";  

    /**
     * The model on which the simulation is being executed.
     */
    protected ViewableDigraph model;
    private String sourcePath;
        
    private JScrollPane modelViewScrollPane;
   
    //The size of the back ground(white part) in the SimView
    private Dimension wrapperSize;	
	
	
	/**
     * The coordinator executing the simulation on the current model.
     */
   // public static SimViewCoordinator coordinator;  

    /**
     * These string store the model name and package name
     */
    
    private JPanel main;
    
    private JScrollPane scrollPane;
    
    private Dimension dim;
    

    /**
     * Constructs a SimView
     */
    
    public SimView()
    {   
        constructUI();       
    }

    /**
     * Constructs the UI of the main window of this application.
     */
    protected void constructUI()
    {
       
        main = new JPanel();
        main.setLayout(new BoxLayout(main, BoxLayout.Y_AXIS));          
        
        // add the model-view panel in a scroll panel
        modelView = new ModelView();
        scrollPane = modelViewScrollPane = new JScrollPane(modelView);        
        
        modelViewScrollPane.setAutoscrolls(true);
        main.add(scrollPane);            
        // adjust tooltip delay settings to make tooltips show up immediately and
        // not go away
        
        
        
        ToolTipManager manager = ToolTipManager.sharedInstance();
        manager.setInitialDelay(0);
        manager.setReshowDelay(0);
    }
    
    //Return the main panel for the SimView 
    public JPanel getSimView(){
    	return main;
    }   
    
   
    /**
     * The panel which displays the components of the current model.
     */
    public class ModelView extends JLayeredPane
        implements SimulatorHookListener, FCoupledSimulator.FRTCentralCoordX.Listener,
        FAtomicSimulator.FAtomicSimulatorX.Listener, FCoupledCoordinator.FCoupledCoordX.Listener,
        DynamicStructureViewer
    {
        /**
         * The thread responsible for moving the currently displayed
         * content views around this model-view.
         */
        protected MoveContentViewThread moveContentViewThread;

        /**
         * A map of the movement objects of the content views currently
         * being moved around this model-view.
         */
        protected Map contentViewMovementMap = new HashMap();

        /**
         * Whether this view should display the couplings between the
         * components in the model.
         */
        protected boolean showCouplings =false;

        /**
         * The list of couplings between all the components (and their
         * subcomponents) in the model.
         */
        protected List couplings = new ArrayList();

        /**
         * The panel, which should cover this entire view, on which are drawn
         * the lines meant to represent the couplings between the components
         * in the model.
         */
        protected CouplingsPanel couplingsPanel;

       
        /**
         * The views on the components of the model this view
         * is displaying.
         */
        protected List componentViews = new ArrayList();

        /**
         * The content views currently displayed in this view.
         */
        protected List contentViews = new ArrayList();

        /**
         * A map of the paths contents are taking as they travel from
         * their source to their destination.  The key used is based
         * of the content's latest step in its path, meaning it is
         * composed of the content as well as the step's component name.
         */
        protected Map contentPathMap = new HashMap();

        /**
         * Whether or not this model-view should execute just one
         * iteration of the simulation at a time, and wait until the user
         * tells it to execute the next iteration, or if it should just
         * keep on executing iterations without stopping each time.
         */
        protected boolean stepMode = true;

        /**
         * Constructs a model-view.
         */
        public ModelView()
        {
            setOpaque(true);
            setBackground(Color.white);
            setLayout(null);
            

            // add the couplings panel
            JPanel panel = couplingsPanel = new CouplingsPanel();

            add(panel, new Integer(2));
            
            // make it so that the couplings panel's size will always
            // match this view's size
            addComponentListener(new ComponentAdapter() {
                public void componentResized(ComponentEvent e) {
                    couplingsPanel.setSize(getSize());
                }
            });

            // create and start the move-content-view thread
            Thread thread = moveContentViewThread = new MoveContentViewThread();
            thread.start();
        }

        /**
         * Adds the given devs-component view to this model view.
         *
         * @param   view        The view to add.
         */
        public void addView(ComponentView view, JComponent parent)
        {
            componentViews.add(view);

            // add the view's GUI component to the given parent component
            // as a layer-0 component
            JComponent comp = (JComponent)view;
            parent.add(comp, new Integer(0));

            // set the view's location and size to their preferred values
            comp.setLocation(view.getPreferredLocation());
            comp.setSize(view.getPreferredSize());
        }
        
        public void removeView(ComponentView view, JComponent parent){
        	
        	componentViews.remove(view);
        	
        	JComponent comp = (JComponent) view;
        	((DigraphView)parent).remove(comp,new Integer(0));
        	
        }

        /**
         * Informs this model view that the user has injected an input
         * into one of the components being viewed.
         */
        public void inputInjected()
        {
            // eliminate all previous content views, as they are now old
            removeContentViews();
        }

  
        /**
         * Removes all atomic views from this model-view.
         */
        public void removeAllViews()
        {
            componentViews.clear();
            modelView.removeAll();
            modelView.add(couplingsPanel);
        }
        
        /**
         * Informs this model-view that a single iteration of the simulation
         * is about to be executed.
         */
        public void stepToBeTaken()
        {
            // get any old content views removed
            removeContentViews();
            stepMode = true;        
        }

        /**
         * Informs this model-view that a run of simulation iterations
         * (versus individual iteration steps) is about to occur.
         */
        public void runToOccur()
        {
            // get any old content views removed
            removeContentViews();
            stepMode = false;
        }
        
        public void clockChanged(double newTime){}
        public void iterationsCompleted(){}
        public void postComputeInputOutputHook(){}
        public void simulatorStateChangeHook(){}
        
        /**
         * See ViewableAtomicSimulator.Listener interface method.
         */
        public void contentOutputted(content content,
            devs source, String sourcePortName)
        {
        	// this method requires the source component to be viewable
            if (!(source instanceof ViewableComponent)) return;
            
            // when step mode isn't on, this model-view shouldn't
            // display the transmittal of contents
            if (!stepMode) return;
            
            // create a content-path-step to hold this first (source) step
            // in the content's path to its destination
            ContentPathStep step = new ContentPathStep();
            step.view = ((ViewableComponent)source).getView();
            step.portName = sourcePortName;
            
            // create this content's path object and add to it the source step
            // just created
            List path = new ArrayList();
            path.add(step);

            // store the path in the content-to-path map using a newly created
            // key
            ContentPathKey key = new ContentPathKey(content, source.getName());
            contentPathMap.put(key, path);
        }

        
        public void savingModelViewCouplingsRemove(ViewableComponent iod,
            couprel savedCr) {
        	couprel mc = savedCr;
        	Iterator it = mc.iterator();
        	
        	ViewableDigraph parent=null ;
        	
        	if (iod instanceof ViewableAtomic){
    			parent = ((ViewableAtomic)iod).getMyParent();
    		}
    		else if (iod instanceof ViewableDigraph)
    		{
    			parent = ((ViewableDigraph)iod).getMyParent(); 
    		}
    		
        	 
        	while (it.hasNext()) {
        		Pair pr = (Pair) it.next();
        		Pair cs = (Pair) pr.getKey();
        		Pair cd = (Pair) pr.getValue();
        		String src = (String) cs.getKey();
        		String dst = (String) cd.getKey();

        		
        		IODevs source, dest;
        		if (src.equals(parent.getName())) {
        			source = parent;
        		}
        		else {
        			source = parent.withName(src);
        		}

        		if (dst.equals(parent.getName())) {
        			dest = parent;
        		}
        		else {
        			dest = parent.withName(dst);
        		}
        		//	s.s("Saving the coupling: "+src+"----"+(String)cs.getValue()+"----"+dst+"----"+(String)cd.getValue());

        		this.couplingRemoved(source, (String) cs.getValue(), dest,(String) cd.getValue());

        	}
        	
        	this.modelRemoved(iod, parent);

        	//redraw the compponent
        	DigraphView parentView = parent.getDigraphView();
        	if (iod instanceof ViewableAtomic) {
        		// tell the viewable atomic to create a view for itself
        		ViewableAtomic atomic = (ViewableAtomic) iod;
        		atomic.createView(modelView);
        		// 	add the atomic view to the model's view
        		AtomicView view1 = atomic.getAtomicView();
        		//	s.s(view1.getViewableComponent().getLayoutName());
        		addView(view1, parentView);
        	}

        	
        	// if this component is a viewable digraph

        	if (iod instanceof ViewableDigraph) {
        		// call this method recursively to get this digraph's
        		// components' views created

        		ViewableDigraph digraph = (ViewableDigraph) iod;
        		//         if(digraph.isBlackBox())
        		createViews(digraph, parentView);
        		//       digraph.mySimView.detmCouplings((ViewableDigraph)iod);
        		//       simview.detmCouplings((ViewableDigraph)iod);
        	}

        	repaint();
        }

        
        public void savedModelViewCouplingsAdd(ViewableComponent iod,
           
        	couprel savedCr) {
        	couprel mc = savedCr;
        	Iterator it = mc.iterator();
        	
        	
        	ViewableDigraph parent =  null;
        	
        	if (iod instanceof ViewableAtomic){
    			parent = ((ViewableAtomic)iod).getMyParent();
    		}
    		else if (iod instanceof ViewableDigraph)
    		{
    			parent = ((ViewableDigraph)iod).getMyParent(); 
    		}  
        	  
        	while (it.hasNext()) {
        		Pair pr = (Pair) it.next();
        		Pair cs = (Pair) pr.getKey();
        		Pair cd = (Pair) pr.getValue();
        		String src = (String) cs.getKey();
        		String dst = (String) cd.getKey();

        		IODevs source, dest;
        		if (src.equals(parent.getName())) {
        			source = parent;
        		}
        		else {
        			source = parent.withName(src);
        		}

        		if (dst.equals(parent.getName())) {
        			dest = parent;
        		}
        		else {
        			dest = parent.withName(dst);
        		}
        		//     s.s("Drawing the coupling: "+src+"----"+(String)cs.getValue()+"----"+dst+"----"+(String)cd.getValue());

        		this.couplingAdded(source, (String) cs.getValue(), dest,
        				(String) cd.getValue());

        	}
        }

        /**
         * See ViewableAtomicSimulator.Listener interface method.
         */
        public void couplingAddedToContentPath(content oldContent,
            devs destComponent, String destPortName,
            content newContent, String sourceComponentName)
        {
            // this method requires the destination component to be viewable
            if (!(destComponent instanceof ViewableComponent)) return;

            // when step mode isn't on, this model-view shouldn't
            // display the transmittal of contents
            if (!stepMode) return;

            // create a content-path-step to hold this step
            // in the content's path to its destination
            ContentPathStep step = new ContentPathStep();
            step.view = ((ViewableComponent)destComponent).getView();
            step.portName = destPortName;

            // use the old-content as part of a key to find the content's
            // path up to this point in the content-path-map
            ContentPathKey key = new ContentPathKey(
                oldContent, sourceComponentName);
            List path = (List)contentPathMap.get(key);
            
            // if no path was found above, then abort this method
            if (path == null) return;

            // use the content's path to find its movement object (if it
            // has one)
            ContentViewMovement movement =
                (ContentViewMovement)contentViewMovementMap.remove(path);

            // make a copy of the path, so that if this same content
            // branches off along multiple couplings at this point,
            // each of those branches can have its own complete path
            path = new ArrayList(path);

            // add the new step to the path
            path.add(step);

            // put the path back in the content-path-map using the new content
            // as part of a new key
            key = new ContentPathKey(newContent, destComponent.getName());
            contentPathMap.put(key, path);

            // if the content has a movement object associated with it already
            if (movement != null) {
                // update the movement object with the copied path, and remap
                // the movement object into the movement-object-map
                movement.path = path;
                contentViewMovementMap.put(path, movement);
            }

            // otherwise
            else {
                // add a content-view to this model-view for the given content;
                // don't make the view visible right away, because the movement
                // thread has to assign it the location of its first step
                ContentView view = new ContentView(newContent);
                view.setVisible(false);
                add(view, new Integer(3));
                contentViews.add(view);
                view.setSize(view.getPreferredSize());

                // make the content-view draggable, so that overlapped such
                // views may be manually separated by the user
                DragViewListener listener = new DragViewListener(view, this);
                view.addMouseListener(listener);
                view.addMouseMotionListener(listener);

                // have the content view moved along the couplings path;
                // the rest of the steps will be added to the path
                // before its reaches its first stop in the model-view
                movement = new ContentViewMovement();
                movement.view = view;
                movement.path = path;
                moveContentViewThread.addContentViewMovement(movement);

                // put the movement object in the movement-objects map, so
                // that we can find it when further steps need to be added
                // to its path
                contentViewMovementMap.put(path, movement);
            }
        }

       

        /**
         * Sizes this model-view to be just larger than the size of its
         * top-level model.
         */
        public Dimension getPreferredSize()
        {
            // if the model or its view have not yet been created
            if (model == null || model.getView() == null) {
                return super.getPreferredSize();
            }          
            
            // return the size of the model's view,
            // plus some space for an empty border
            Dimension size = ((JComponent)model.getView()).getSize();
            
            return new Dimension(size.width + modelBorderWidth * 10,
                size.height + modelBorderWidth * 10);
        }

        /**
         * Together, these force this model-view's size to be its
         * preferred size.
         */
        public Dimension getMinimumSize() {return getPreferredSize();}
        public Dimension getMaximumSize() {return getPreferredSize();}
        

        /**
         * Removes from this model-view each of the content-views
         * it is displaying.
         */
        protected void removeContentViews()
        {
            // for each content view this view contains
            for (int i = 0; i < contentViews.size(); i++) {
                ContentView view = (ContentView)contentViews.get(i);

                // remove this content view
                remove(view);
            }

            contentViews.clear();

            repaint();
        }

        /**
         * Informs this model-view that the mouse has entered a port-box
         * on one of the model's components.
         */
        public void mouseEnteredPort()
        {
            showCouplings = true;
            repaint();
        }

        /**
         * Informs this model-view that the mouse has exited a port-box
         * on one of the model's components.
         */
        public void mouseExitedPort()
        {
            showCouplings = false;
            repaint();
        }

        // Model Add/Remove 
        public void modelAdded(ViewableComponent iod, ViewableDigraph parent) {

            DigraphView parentView = parent.getDigraphView();
            if (parent.isBlackBox() || parent.isHidden()) {
              iod.setHidden(true);
            }
            if (iod instanceof ViewableAtomic) {
              // tell the viewable atomic to create a view for itself
              ViewableAtomic atomic = (ViewableAtomic) iod;
              atomic.createView(modelView);
              // add the atomic view to the model's view
              AtomicView view1 = atomic.getAtomicView();
              addView(view1, parentView);
            }
            // if this component is a viewable digraph
            if (iod instanceof ViewableDigraph) {
              // call this method recursively to get this digraph's
              // components' views created
              ViewableDigraph digraph = (ViewableDigraph) iod;
              createViews(digraph, parentView);
              detmCouplings( (ViewableDigraph) iod);
            }
            modelView.repaint();
          }

          public void modelRemoved(ViewableComponent iod, ViewableDigraph parent) {

            DigraphView parentView = parent.getDigraphView();
            if (iod instanceof ViewableAtomic) {
              removeView( ( (ViewableAtomic) iod).getAtomicView(), parentView);
            }
            else if (iod instanceof ViewableDigraph) {
              destroyModelView( (ViewableDigraph) iod, parentView);
            }
            modelView.repaint();
          }

          public void destroyModelView(ViewableDigraph model,
                                       ComponentView parentView) {
            String srcName, destName, compName = "";
            // for each component in the digraph
            Iterator i = model.getComponents().iterator();
            while (i.hasNext()) {
              Object component = i.next();
              // if this component is a viewable atomic
              if (component instanceof ViewableAtomic) {
                compName = ( (ViewableAtomic) component).getName();
                removeView( ( (ViewableAtomic) component).getView(),
                           (JComponent) (model.getView()));
              }
              // if this component is a viewable digraph
              if (component instanceof ViewableDigraph) {
                compName = ( (ViewableDigraph) component).getName();
                destroyModelView( (ViewableDigraph) component, model.getView());
              }
              //need to remove the coupling connected to that component from the CouplingsPanel
              int csize = couplings.size(); // the size of the couplings
              for (int j = csize - 1; j >= 0; j--) { // a special way to check all the elements in the Arraylist while removing element dynamicly
                Coupling coupling = (Coupling) couplings.get(j);
                srcName = (coupling.sourceView).getViewableComponent().getName();
                destName = (coupling.destView).getViewableComponent().getName();
                if (srcName.compareTo(compName) == 0 ||
                    destName.compareTo(compName) == 0) {
                  couplings.remove(j);
                }
              }
            }
            removeView(model.getView(), (JComponent) parentView);
          }

          public void couplingAdded(IODevs src, String p1, IODevs dest, String p2) {
            if (! (src instanceof ViewableComponent &&
                   dest instanceof ViewableComponent)) {
              // skip this coupling - it can't be displayed
              System.out.println("Coupling could not be displayed."
                                 + "\n\tFrom: " + src.getName()
                                 + ", port " + p1
                                 + "\n\tTo: " + dest.getName()
                                 + ", port " + p2);
              return;
            }
            Coupling coupling = new Coupling();
            coupling.sourceView = ( (ViewableComponent) src).getView();
            coupling.sourcePortName = p1;
            coupling.destView = ( (ViewableComponent) dest).getView();
            coupling.destPortName = p2;

            addCoupling(coupling);
            repaint();
          }


          public void couplingRemoved(IODevs src, String p1, IODevs dest, String p2) {
            String srcName, destName;
            ViewableDigraph parent;
            for (int i = 0; i < couplings.size(); i++) {
              Coupling coupling = (Coupling) couplings.get(i);
              srcName = (coupling.sourceView).getViewableComponent().getName();
              ViewableComponent srcView = (coupling.sourceView).getViewableComponent();
              if (srcView instanceof ViewableDigraph) {
                parent = ( (ViewableDigraph) srcView).getMyParent();
              }
              else {
                parent = ( (ViewableAtomic) srcView).getMyParent();
              }
              destName = (coupling.destView).getViewableComponent().getName();
              ViewableComponent destView = (coupling.destView).getViewableComponent();
              if (srcName.compareTo(src.getName()) == 0 &&
                  coupling.sourcePortName.compareTo(p1) == 0 &&
                  destName.compareTo(dest.getName()) == 0 &&
                  coupling.destPortName.compareTo(p2) == 0) {
                couplings.remove(i);
                //modelRemoved(destView,parent);
                //                     removeView(coupling.destView, parent.getDigraphView());

                break;
              }
            }
            	
          }

        /**
         * An object associating a content-view with various information
         * about its movement along a path within the model-view.
         */
        protected class ContentViewMovement
        {
            /**
             * The content-view to be moved.
             */
            protected ContentView view;

            /**
             * The path of steps along which the content view is to move.
             */
            protected List path;

            /**
             * The index of the current step on the path along which
             * the content view is moving.
             */
            protected int currentStepIndex;

            /**
             * The x and y offsets to take with each step along the current line.
             */
            protected double dx, dy;

            /**
             * The current location of this view along the current line, with more
             * precision than just integer coordinates, so that this view
             * stays centered on the line as it moves.
             */
            protected Point2D.Double location;

            /**
             * How many moves it will take to get to the current destination.
             */
            protected int movesRequired;

            /**
             * How many moves have been made so far towards the current
             * destination.
             */
            protected int movesDone;
        }

        /**
         * Moves each content view in its list along a series of steps
         * (i.e. couplings) to its final destination port.
         */
        protected class MoveContentViewThread extends Thread
        {
            /**
             * The content view movements this thread is currently performing.
             */
            protected List movements = new ArrayList();

            /**
             * Tells this thread to execute the given content-view movement.
             *
             * @param   movement        The content-view movement to execute.
             */
            public void addContentViewMovement(ContentViewMovement movement)
            {
                movements.add(movement);
            }

            /**
             * See parent method.
             */
            public void run()
            {
                // keep doing this
                while (true) {
                    moveContentViews();

                    // pause so the animation doesn't go by too quickly
                    Util.sleep(20);
                }
            }

            /**
             * Performs the actual movements of the content views.
             */
            protected void moveContentViews()
            {
                // for each content view movement currently being performed
                for (int i = 0; i < movements.size(); i++) {
                    ContentViewMovement movement = (ContentViewMovement)
                        movements.get(i);

                    // if, for the current step of this movement, no moves
                    // have yet been performed
                    if (movement.movesDone == 0) {
                        // if the destination component of the current step
                        // is hidden
                        ContentPathStep step = (ContentPathStep)
                            movement.path.get(movement.currentStepIndex);
                        if (step.view.getViewableComponent().isHidden()) {
                            // move on to the next step
                            movement.currentStepIndex++;

                            // if this was the last step in the movement
                            if (movement.currentStepIndex >= movement.path.size()) {
                                discardMovement(movement);
                            }

                            continue;
                        }

                        // if the current step is the first one in this
                        // movement's path, or is a later step but no
                        // previous step could assign the movement a
                        // location
                        JComponent view = (JComponent)movement.view;
                        if (movement.currentStepIndex == 0
                            || movement.location == null) {
                            // use this step as the starting location for the
                            // movement of the content view
                            Point start = modelView.getLocation(
                                (JComponent)step.view);
                            PointUtil.translate(start,
                                step.view.getPortLocation(step.portName));
                            int viewX = start.x - view.getWidth() / 2,
                                viewY = start.y - view.getHeight() / 2;
                            view.setLocation(viewX, viewY);

                            // show the content view
                            view.setVisible(true);

                            // remember the content view's starting location
                            movement.location = new Point2D.Double(
                                viewX, viewY);

                            // go on to the next step in the movement
                            movement.currentStepIndex++;

                            // if this was the last step in the movement
                            if (movement.currentStepIndex >= movement.path.size()) {
                                discardMovement(movement);
                            }

                            continue;
                        }

                        // detm the starting location for this step
                        Point start = new Point(
                            (int)movement.location.x + view.getWidth() / 2,
                            (int)movement.location.y + view.getHeight() / 2);

                        // detm the finish location for this step
                        Point finish = modelView.getLocation((JComponent)step.view);
                        PointUtil.translate(finish,
                            step.view.getPortLocation(step.portName));

                        // compute the x and y offsets to take with each step
                        // along the line
                        movement.location = new Point2D.Double(start.x, start.y);
                        double angle = Math.atan2(finish.y - start.y,
                            finish.x - start.x);
                        
                        movement.dx = speed * Math.cos(angle);
                        movement.dy = speed * Math.sin(angle);

                        // detm how many moves it will take to get to the destination
                        Point2D.Double location = movement.location;
                        movement.movesRequired =
                            (int)Math.rint(location.distance(finish) / speed);
                        movement.movesDone = 0;

                        // start the content view centered over the source port location
                        location.x -= view.getWidth() / 2;
                        location.y -= view.getHeight() / 2;
                        view.setLocation((int)Math.rint(location.x),
                            (int)Math.rint(location.y));
                    }

                    // if not all the moves for the current step in the
                    // path have been done
                    if (movement.movesDone < movement.movesRequired) {
                        // move the content view one more step along the line
                        Point2D.Double location = movement.location;
                        location.x += movement.dx;
                        location.y += movement.dy;
                        movement.view.setLocation((int)Math.rint(location.x),
                            (int)Math.rint(location.y));
                        movement.movesDone++;
                    }

                    // otherwise
                    else {
                        // move on to the next step
                        movement.movesDone = 0;
                        movement.currentStepIndex++;

                        // if the content view is at the end of the path
                        if (movement.currentStepIndex >= movement.path.size()) {
                            discardMovement(movement);
                        }
                    }
                }
            }

            /**
             * Removes the given movement and its associated objects from
             * further consideration, so they may be gc'd.
             *
             * @param   movement        The movement object to discard.
             */
            protected void discardMovement(ContentViewMovement movement)
            {
                contentPathMap.remove(movement.view.getContent());
                contentViewMovementMap.remove(movement.path);
                movements.remove(movement);
            }
        }

        /**
         * A panel, which should cover the entire model-view, on which are drawn
         * the lines meant to represent the couplings between the components
         * in the model.
         */
        protected class CouplingsPanel extends JPanel
        {
            public CouplingsPanel()
            {
                setOpaque(false);
            }

            public void paint(Graphics g)
            {
                // if the couplings are currently supposed to be shown
                if (showCouplings || alwaysShowCouplings) {
                    // for each coupling
                    g.setColor(Color.lightGray);
                    for (int i = 0; i < couplings.size(); i++) {
                        Coupling coupling = (Coupling)couplings.get(i);

                        // if either the source of destination views of the
                        // coupling are hidden
                        if (coupling.sourceView.getViewableComponent().
                            isHidden()
                            || coupling.destView.getViewableComponent().
                            isHidden()) {
                            // don't draw this coupling
                            continue;
                        }

                        // detm the pixel location within this model-view
                        // of the source port of the coupling
                        Point source = ModelView.this.getLocation(
                            (JComponent)coupling.sourceView);
                        PointUtil.translate(source,
                            coupling.sourceView.getPortLocation(
                            coupling.sourcePortName));

                        // detm the pixel location within this model-view
                        // of the destination port of the coupling
                        Point dest = ModelView.this.getLocation(
                            (JComponent)coupling.destView);
                        PointUtil.translate(dest,
                            coupling.destView.getPortLocation(
                            coupling.destPortName));

                        // draw this coupling's line
                        g.drawLine(source.x, source.y, dest.x, dest.y);
                    }
                }
            }
        }

        /**
         * Informs this model-view that the simulation has been restarted.
         */
        public void simulationRestarted()
        {
            removeContentViews();
        }

        /**
         * Returns the location of the given descendant component within
         * this view.
         *
         * @param   component       The descendent component whose location is
         *                          desired.
         * @return                  The location of the component, relative to
         *                          the upper-left corner of this view.
         */
        public Point getLocation(JComponent component)
        {
            return ComponentUtil.getLocationRelativeToAncestor(component, this);
        }

        /**
         * Adds a coupling to this view's list of couplings.
         *
         * @param   coupling        The coupling to add.
         */
        public void addCoupling(Coupling coupling) {couplings.add(coupling);}

        /**
         * Clears this view's list of couplings.
         */
        public void clearCouplings() {couplings.clear();}
    }

    /**
     * Creates an atomic-view for each viewable atomic in the given
     * digraph model, as well as for those recursively found contained
     * within in the given model's children models.  Each new
     * atomic-view is added to the model-view.
     *
     * @param   model       The model for whose atomic components views are
     *                      to be created.
     * @param   parent      The parent component to which the given model's
     *                      views are to be added.
     */
    protected void createViews(ViewableDigraph model, JComponent parent)
    {
        // tell the model to create a view for itself
        model.createView(modelView);

        // if the given model isn't to be displayed as a black box
        if (!model.isBlackBox()) {
            // tell the model to lay itself out for the viewer (but don't
            // let any problems in that process cause things to halt, as it
            // is not a critical objective)
            try {
                // if the override layout method doesn't get the layout done
                if (!model.layoutForSimViewOverride()) {
                    // call the automatically-generated layout method
                    model.layoutForSimView();
                }
            } catch (Exception e) {e.printStackTrace();}
        }

        // add the model's view to the given parent
        DigraphView view = model.getDigraphView();
        modelView.addView(view, parent);        

        // if the given digraph is the top-level digraph in the model being viewed
        if (parent == modelView) {
            // set the location of the digraph's view to the upper-left hand
            // corner of the model-view
            view.setLocation(new Point(20, 20));            
        }

        // for each component in the digraph
        Iterator i = model.getComponents().iterator();
        while (i.hasNext()) {
            Object component = i.next();

            // if the given digraph is itself a black box, or is hidden
            if (model.isBlackBox() || model.isHidden()) {
                // if this component is viewable
                if (component instanceof ViewableComponent) {
                    // tell this component it's hidden
                    ViewableComponent comp = (ViewableComponent)component;
                    comp.setHidden(true);
                }
            }

            // if this component is a viewable atomic
            if (component instanceof ViewableAtomic) {
                // tell the viewable atomic to create a view for itself
                ViewableAtomic atomic = (ViewableAtomic)component;
                atomic.createView(modelView);

                // add the atomic view to the model's view
                AtomicView view1 = atomic.getAtomicView();
                modelView.addView(view1, view);

                // if this atomic is the whole model being viewed (and thus,
                // is wrapped in a wrapper digraph)
                if (model.getName().equals(wrapperDigraphName)) {
                    // center the atomic in the model-view
                    view1.setLocation(
                        modelViewScrollPane.getWidth() / 2 - view.getWidth() / 2,
                        modelViewScrollPane.getHeight() / 2 - view.getHeight() / 2);                    
                }
            }

            // if this component is a viewable digraph
            if (component instanceof ViewableDigraph) {
                // call this method recursively to get this digraph's
                // components' views created
                ViewableDigraph digraph = (ViewableDigraph)component;
                createViews(digraph, view);
            }
            
        }
    }

    
    

    /**
     * Creates an instance of the model class of the given name (including
     * the package name).  Also, creates the views and coordinator for the
     * model instance.
     *
     * @param   name        The name of the model class to instantiate.
     */
    public void useModelClass(FModel rootModel, String sourcePath)
    {
    	model = ((FCoupledModel)rootModel).getModel();       
        this.sourcePath = sourcePath;

        // get rid of any old views
        modelView.removeAllViews();

        // create a coordinator
       // coordinator = new SimViewCoordinator(model, modelView);
       // coordinator.initialize();

       
        // create the new views and lay them out
        createViews(model, modelView);


        // add all the coupings in the model to the model-view
        modelView.clearCouplings();
        detmCouplings(model);

        // get the model-view scrollpane resized to take into account
        // the possibly new model-view size
        ((JComponent)modelViewScrollPane.getParent()).revalidate();       
    }
    

    /**
     * A coupling between a source port on one devs component view, and
     * a destination port on another.
     */
    protected class Coupling
    {
        /**
         * The source and destination component views.
         */
        public ComponentView sourceView, destView;

        /**
         * The source and destination port names.
         */
        public String sourcePortName, destPortName;
    }

    /**
     * Determines all the couplings present within the given model, and adds
     * them to the model-view for display.
     *
     * @param   model       The model for which to find all the couplings.
     */
    protected void detmCouplings(ViewableDigraph model)
    {
        detmCouplings((ViewableComponent)model);

        // for each component in the model
        Iterator i = model.getComponents().iterator();
        while (i.hasNext()) {
            Object component = i.next();

            // if this component is a viewable digraph
            if (component instanceof ViewableDigraph) {
                // call this method recursively to get this digraph's
                // components' couplings detm'd
                ViewableDigraph digraph = (ViewableDigraph)component;
                detmCouplings(digraph);
            }

            // else, if this component is a viewable component
            else if (component instanceof ViewableComponent) {
                detmCouplings((ViewableComponent)component);
            }
        }
    }

    /**
     * Determines all the couplings for which a port on the given component
     * is the source, and adds those couplings to the model-view for display.
     *
     * @param   comp       The devs component whose couplings are to be found.
     */
    protected void detmCouplings(ViewableComponent comp)
    {
        // find all the couplings for which an outport of the component
        // is the source
        detmCouplings(comp, comp.getOutportNames());

        // if the component is a digraph
        if (comp instanceof ViewableDigraph) {
            // find all the couplings for which an inport of the component
            // is the source
            detmCouplings(comp, comp.getInportNames());
        }
    }

    /**
     * Determines all the couplings for which a port from the given list
     * (on the given component) is the source, and adds those couplings
     * to the model-view for display.
     *
     * @param   comp        The devs component to which the ports belong.
     * @param   portNames   The list of port names on the above component
     *                      to look for couplings.
     */
    protected void detmCouplings(ViewableComponent comp, List portNames)
    {
        // for each port in the given list
        for (int i = 0; i < portNames.size(); i++) {
            String portName = (String)portNames.get(i);

            // ask the given component's simulator or coordinator for the
            // couplings for which this port is a source
            List couplings = null;
            if (comp instanceof ViewableAtomic) {
                couplings = ((coupledSimulator)((atomic)comp).getSim()).
                    getCouplingsToSourcePort(portName);
            }
            else if (comp instanceof ViewableDigraph) {
                couplings = ((digraph)comp).getCoordinator().
                    getCouplingsToSourcePort(portName);
            }

            // for each coupling to this port
            for (int j = 0; j < couplings.size(); j++) {
                Pair pair = (Pair)couplings.get(j);

                // create a coupling object and store this coupling's
                // source component-view and port
                Coupling coupling = new Coupling();
                coupling.sourceView = comp.getView();
                coupling.sourcePortName = portName;

                // if the component at the destination end of this coupling
                // is not a viewable-component
                entity destEntity = (entity)pair.getKey();
                String destPortName = (String)pair.getValue();
                if (!(destEntity instanceof ViewableComponent)) {
                    // skip this coupling - it can't be displayed
                    System.out.println("Coupling could not be displayed."
                        + "\n\tFrom: " + comp.getName()
                        + ", port " + portName
                        + "\n\tTo: " + destEntity.getName()
                        + ", port " + destPortName);
                    continue;
                }

                // store this coupling's destination component-view and port
                coupling.destView = ((ViewableComponent)destEntity).getView();
                coupling.destPortName = destPortName;

                // add the coupling to the model-view
                modelView.addCoupling(coupling);
            }
        }
    }

    /**
     * A step in a content-path list of such steps.
     */
    protected class ContentPathStep
    {
        /**
         * At which view the content should be displayed for this step.
         */
        public ComponentView view;

        /**
         * At which port on the above view the content should be
         * displayed for this step.
         */
        public String portName;
    }

    /**
     * Returns this sim-view's model-view.
     */
    public ModelView getModelView() {return modelView;}

    /**
     * A key used to find a particular content-path in the content-path-map.
     */
    protected class ContentPathKey
    {
        /**
         * The latest incarnation of the content traversing the path.
         */
        ContentInterface content;

        /**
         * The current component the above content has reached in its path.
         */
        String componentName;

        /**
         * Constructs a key.
         */
        public ContentPathKey(ContentInterface content_, String componentName_)
        {
            content = content_;
            componentName = componentName_;
        }

        /**
         * Equates the given object to this key if it is of the same class,
         * if its content port and values match this key's,
         * and if its component name matches this key's.
         */
        public boolean equals(Object o)
        {
            if (o instanceof ContentPathKey) {
                ContentPathKey pair = (ContentPathKey)o;
                return content.equals(pair.content) &&
                    componentName.equals(pair.componentName);
            }

            return false;
        }

        /**
         * Returns a hash-code for this key that is based on a combination
         * of its component-name and its content's port-name and value.
         */
        public int hashCode()
        {
            return (componentName + content.getPort() + content.getValue())
                .hashCode();
        }
    }

   

    /**
     * Saves the current top-level model's layout (within this sim-view)
     * to its source code file.
     */
    public void saveModelLayout() {saveModelLayout(model);}

    /**
     * Saves the given model's layout (within this sim-view)
     * to its source code file.
     */
    protected void saveModelLayout(ViewableDigraph model)
    {
        // if no model is currently being viewed, or the given model
        // is being viewed as black box (or is hidden), then abort this method
        if (model == null || model.isBlackBox() || model.isHidden()) return;

        // if the model's layout hasn't changed since its last save
        if (!model.getLayoutChanged()) {
            // just look into whether the children's layouts need to be
            // saved
            saveLayoutsOfChildren(model);
            return;
        }

        // detm the file name of the java source code file for the current
        // model
        String className = model.getClass().getName().replace('.', '/');

        // if we can't load the model's source code into memory as a
        // big string
        File file = new File(sourcePath+ "/" + className + ".java");
        String code = FileUtil.getContentsAsString(file);

        // if we can find a previously generated layoutForSimView method
        int index = code.indexOf("void layoutForSimView()");
        if (index != -1) {
            // find the index of the first line of the method's
            // autogenerated comment
            int startIndex = code.lastIndexOf("/**", index);
            startIndex = code.lastIndexOf("\n", startIndex);

            // find the index of the end of the last line of the
            // method's body
            int endIndex = code.indexOf("}", index);
            endIndex = code.indexOf("\n", endIndex);

            // remove the method and its comment
            code = code.substring(0, startIndex)
                + code.substring(endIndex, code.length());
        }

        // find the ending brace in the file, which is assumed to be the
        // closing bracket of the only class in the file; the method will
        // be inserted on the line just before this bracket
        index = code.lastIndexOf("}");
        index = code.lastIndexOf("\n", index);

        // build the comment and declaration of the method
        StringBuffer method = new StringBuffer("\n");
        method.append("    /**\n");
        method.append("     * Automatically generated by the SimView program.\n");
        method.append("     * Do not edit this manually, as such changes will get overwritten.\n");
        method.append("     */\n");
        method.append("    public void layoutForSimView()\n");
        method.append("    {\n");

        // if the model isn't currently displayed as a black box
        if (!model.isBlackBox()) {
            // add the call to set the model's preferred size
            method.append("        preferredSize = new Dimension(");
            Dimension size = ((JComponent)model.getView()).getSize();
            method.append(size.width);
            method.append(", ");
            method.append(size.height);
            method.append(");\n");
        }

        // for each child component of the model
        Iterator i = model.getComponents().iterator();
        while (i.hasNext()) {
            // if this component isn't a viewable-component, skip it
            Object next = i.next();
            if (!(next instanceof ViewableComponent)) continue;
            ViewableComponent component = (ViewableComponent)next;

            // if this component is hidden, skip it
            if (component.isHidden()) continue;

            // add the call to set this component's location
            method.append("        ");
            method.append("((ViewableComponent)withName("
                + component.getLayoutName());
            method.append(")).setPreferredLocation(new Point(");
            Point location = component.getPreferredLocation();
            method.append(location.x);
            method.append(", ");
            method.append(location.y);
            method.append("));\n");
        }

        // add the closing brace of the method
        method.append("    }\n");

        // insert the method into the code
        code = code.substring(0, index) + method
            + code.substring(index + 1, code.length());

        // write the updated source code back to the java file
        file = new File(file.getPath());
        if(model.getComponents().size() != 1){
        try {
        	FileWriter fw = new FileWriter(file);
            BufferedWriter out = new BufferedWriter(fw);
            out.write(code, 0, code.length());
            out.flush();
            fw.close();
        } catch (IOException e) {e.printStackTrace();}
        }
        // tell the model its layout now hasn't changed since its last save
        model.setLayoutChanged(false);

        saveLayoutsOfChildren(model);
    }

    /**
     * Saves the layouts (within this sim-view) of the children components
     * of the given model to their associated source code files.
     */
    protected void saveLayoutsOfChildren(ViewableDigraph model)
    {
        // for each child component of the model
        Iterator i = model.getComponents().iterator();
        while (i.hasNext()) {
            // if this component isn't a viewable-component, skip it
            Object next = i.next();
            if (!(next instanceof ViewableComponent)) continue;
            ViewableComponent component = (ViewableComponent)next;

            // if this component is itself a viewable digraph
            if (component instanceof ViewableDigraph) {
                ViewableDigraph digraph = (ViewableDigraph)component;

                // call this method recursively to get this digraph's
                // layout method created/updated
                saveModelLayout(digraph);
            }
        }
    }   
  }

