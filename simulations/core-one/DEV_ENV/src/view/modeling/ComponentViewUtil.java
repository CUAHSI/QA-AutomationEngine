
/**
 * Utility methods involving (or used by) devs component views.
 *
 * @author  Jeff Mather
 */

package view.modeling;


import java.awt.*;
import java.util.*;
import java.util.List;
import javax.swing.*;

import GenCol.*;


import model.modeling.*;
import model.simulation.*;
import util.*;
import view.simView.*;

public class ComponentViewUtil
{
    /**
     * Creates port boxes for the given list of names, and adds them to the
     * given panel.
     *
     * @param   portsPanel      The panel to which to add the port boxes.
     * @param   names           The list of port names for which to create
     *                          port boxes.
     * @param   in              Whether the ports are in- or out-ports.
     * @param   extendLeft      Whether the ports' pins are to be drawn
     *                          extending left (vs. right).
     * @param   nameToPortBox   The map to which to add a mapping of the
     *                          port names to their port-boxes.
     * @param   component       The component that contains the ports.
     * @param   modelView       The model-view that contains the above
     *                          atomic (this may also be left null).
     * @param   dragViewListener
     *                          If provided, is a drag-view-listener of
     *                          the parent component which needs to listen
     *                          for mouse events that would normally be
     *                          intercepted by the port-boxes (as they
     *                          overlap the parent).
     */
    static public void createPortBoxes(JPanel portsPanel, List names,
        boolean in, boolean extendLeft, Map nameToPortBox,
        ViewableComponent component, SimView.ModelView modelView,
        DragViewListener dragViewListener)
    {
        // sort the port names in the given list according to alphabetical
        // order (but numeric order when it comes to embedded numeric
        // substrings)
        TreeSet sortedNames = new TreeSet(new NumericStringComparator());
        sortedNames.addAll(names);

        // for each sorted port name
        Iterator i = sortedNames.iterator();
        while (i.hasNext()) {
            String name = (String)i.next();

            // add a port box with this name to the given ports panel
            PortBox box = new PortBox(name, in, extendLeft, component,
                modelView);
            portsPanel.add(box);
            box.setAlignmentX(extendLeft ? 1f : 0f);
            nameToPortBox.put(name, box);

            // if a drag-view listener was supplied
            if (dragViewListener != null) {
                // add it to this port-box
                box.addMouseListener(dragViewListener);
                box.addMouseMotionListener(dragViewListener);
            }
        }
    }

    /**
     * Returns the offset within the given component view of the
     * lollipop circle of the port-box associated with the port
     * of the given name.
     *
     * @param   view            The component view displaying the port.
     * @param   portName        The port whose port-box pollipop location
     *                          should be returned.
     * @param   nameToPortBox   The component view's mapping of port-names
     *                          to their port-boxes.
     * @return                  The offset of the port-box's lollipop within
     *                          the given component view.
     */
    static public Point getPortLocation(ComponentView view, String portName,
        Map nameToPortBox)
    {
        // if the port-box for the given port-name cannot be found on this
        // component
        PortBox box = (PortBox)nameToPortBox.get(portName);
        if (box == null) {
            // note that we used to print out an error message here, but
            // with models that contains hundreds of components, doing so
            // (even using a scheme where only one message per
            // port-name/view combo is displayed) causes unacceptable
            // slowdown

            return new Point();
        }

        // return the location of the port's pin
        Point location = ComponentUtil.getLocationRelativeToAncestor(
           box, (JComponent)view);
        PointUtil.translate(location, box.getPinLocation());
        return location;
    }

    /**
     * Injects all test inputs for the given view on their associated inports.
     */
    static public void injectAll(ComponentView view)
    {
        // for each inport on the atomic
        message m = new message();
        ViewableComponent component = view.getViewableComponent();
        Iterator i = component.getInportNames().iterator();
        while (i.hasNext()) {
            // if this inport has test inputs
            List inputs = component.getTestInputs((String)i.next());
            if (inputs != null) {
                // for each test input
                Iterator j = inputs.iterator();
                while (j.hasNext()) {
                    // add a content for this input to the message to
                    // be injected
                    TestInput input = (TestInput)j.next();
                    m.add(new content(input.portName, input.value));
                }
            }
        }

        // inject the message into the component's simulator
        component.getSimulator().simInject(0, m);
    }

}