/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
package view.modeling;

import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.util.List;
import javax.swing.*;
import javax.swing.event.*;

import model.modeling.*;
import model.simulation.*;
import util.*;
import view.simView.*;

/**
 * A panel that displays a depiction of a port.
 */
public class PortBox extends JPanel
{
    /**
     * The viewable-component to which this box's port belongs.
     */
    protected ViewableComponent component;

    /**
     * The model-view containing this port-box's component.
     */
    protected SimView.ModelView modelView;

    /**
     * The name of the port being depicted.
     */
    protected String portName;

    /**
     * A cache of the width value of the port's name when drawn in
     * the port label font.
     */
    protected int labelWidth;

    /**
     * Whether the associated port is an inport.
     */
    protected boolean in;

    /**
     * Whether this port-box's pin is to extend to the left (vs. to the right).
     */
    protected boolean extendsLeft;

    /**
     * This x ordinate of the center of the pin within this port-box.
     */
    protected int pinX;

    /**
     * The width of this port-box's pin circle (in pixels).
     */
    final protected int pinWidth = 8;

    /**
     * The width of the space between the pin and the name label
     * (in pixels).
     */
    final protected int spaceBetweenPinAndName = 8;

    /**
     * The length of the line connecting the pin circle to the edge of
     * this port-box (in pixels).
     */
    final protected int lineLength = 4;

    /**
     * The font used when drawing the port name, and its associated
     * metrics object.
     */
    static protected Font nameFont = new Font("SansSerif", Font.PLAIN, 10);
    static protected FontMetrics nameFontMetrics = (new JPanel()).getFontMetrics(nameFont);
    static public int nameFontAscent = nameFontMetrics.getAscent();

    /**
     * Constructs a view on the given port, taking into account whether
     * the port is an inport or an outport.
     *
     * @param   portName_       The name of the port being depicted.
     * @param   in_             Whether the port is an inport or an outport.
     * @param   extendsLeft_    Whether this port-box's pin is to extend
     *                          to the left (vs. to the right).
     * @param   component_      The component to which the port belongs,
     *                          for test-input functionality.
     * @param   modelView_      The model-view containing the above atomic
     *                          (this may also be left null).
     */
    public PortBox(String portName_, boolean in_, boolean extendsLeft_,
        ViewableComponent component_, SimView.ModelView modelView_)
    {
        portName = portName_;
        in = in_;
        extendsLeft = extendsLeft_;
        component = component_;
        modelView = modelView_;

        // cache the name string width
        labelWidth = nameFontMetrics.stringWidth(portName);

        setOpaque(false);

        // if this port is an inport, and we were given a component
        if (in && component != null) {
            // when this port-box is clicked
            addMouseListener(new MouseAdapter() {
                public void mouseClicked(MouseEvent event) {
                    // if the control-key is being pressed, only the 
                    // test-inputs for this port will be displayed; 
                    // otherwise, all test-inputs for this component will
                    // be displayed
                    List inputs = event.isControlDown() ?
                        component.getTestInputs(portName) :
                        component.getTestInputs();
                                             
                        
                    // show this port-box's popup menu
                    Dialog dialog = new InputsDialog(inputs);
                    Point location = new Point(PortBox.this.getLocation());
                    SwingUtilities.convertPointToScreen(
                        location, PortBox.this);
                    dialog.setLocation(location);
                    dialog.setVisible(true);
                    
                }
            });
        }

        // add this mouse listener
        addMouseListener(new MouseAdapter() {
            // when the mouse enters this port-box
            public void mouseEntered(MouseEvent e) {
                modelView.mouseEnteredPort();
            }

            // when the mouse exits this port-box
            public void mouseExited(MouseEvent e) {
                modelView.mouseExitedPort();
            }
        });
    }

    /**
     * Draws this port-box's pin and port name.
     */
    public void paint(Graphics g)
    {
        // draw the pin head
        g.setColor(Color.black);
        int width = getWidth();
        int pinHeight = pinWidth;
        pinX = extendsLeft ? width - lineLength - pinWidth : 0 + lineLength;
        g.fillOval(pinX, getHeight() / 2 - pinHeight / 2 + 1,
            pinWidth, pinHeight);

        // draw the pin line
        int lineY = getHeight() / 2 + 1;
        g.drawLine(extendsLeft ? width : 0, lineY, pinX, lineY);

        // draw the port name
        g.setColor(Color.black);
        g.setFont(nameFont);
        final int nameX = !extendsLeft ? pinWidth + spaceBetweenPinAndName :
            width - pinWidth - spaceBetweenPinAndName - labelWidth;
        g.drawString(portName, nameX,
            getHeight() / 2 + nameFontAscent / 3 + 1);
    }

    /**
     * Returns the offset within this port-box of the center of
     * its pin graphic.
     */
    public Point getPinLocation()
    {
        return new Point(pinX + pinWidth / 2, getHeight() / 2 + 1);
    }

    /**
     * Returns the total width of this port-box's pin and name label.
     */
    public Dimension getPreferredSize()
    {
        int width = lineLength + pinWidth + spaceBetweenPinAndName * 2
            + labelWidth;
        return new Dimension(width, super.getPreferredSize().height);
    }

    /**
     * Limits the width of this port-box to its preferred width.
     */
    public Dimension getMaximumSize()
    {
        return new Dimension(getPreferredSize().width, Integer.MAX_VALUE);
    }

    /**
     * A dialog of test-inputs-to-inject when this port box is clicked.
     */
    protected class InputsDialog extends JDialog
    {
        /**
         * Constuctor.
         *
         * @param   inputs      The test inputs to display in this dialog.
         */
        public InputsDialog(List inputs)
        {
            super((Frame)SwingUtilities.getWindowAncestor(PortBox.this),
                "Inputs");
            
            setModal(true);
            
            Container pane = getContentPane();
            pane.setLayout(new BorderLayout());
            

            // add the inputs list
            final JList list = new JList();
            list.setFont(new Font("SansSerif", Font.PLAIN, 10));
            pane.add(new JScrollPane(list), BorderLayout.CENTER);
            int maxSize=0;
            ListIterator li=inputs.listIterator();
            
            while(li.hasNext())
            {
            	Object item=li.next();
            	int currsize=(item.toString()).length();
            	System.err.println(currsize);
            	maxSize=(maxSize<=currsize)?currsize:maxSize;
      	    }
            
            System.err.println("Biggest Size "+maxSize);
            
            
            setSize(maxSize*6, 90+(inputs.size())*15);
            
            //pane.add(new JScrollPane(list), BorderLayout.CENTER);
          
            //VigneshAdd
            System.err.println(inputs.toArray().length);

            // if any inputs were given
            if (inputs != null) {
                // add them to the list control
                list.setListData(inputs.toArray());
            }

            // add a flow-layout panel at the bottom
            JPanel panel = new JPanel();
            panel.setLayout(new FlowLayout());
            pane.add(panel, BorderLayout.SOUTH);

            // add the inject button
            JButton button = new JButton("inject");
            button.setFont(new Font("SansSerif", Font.PLAIN, 10));
            panel.add(button);

            // when the inject button is clicked
            button.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    // hide this dialog
                    InputsDialog.this.setVisible(false);

                    // inject the selected inputs
                    inject(list.getSelectedValues());
                }
            });
        }

        /**
         * Injects the given list of inputs into this port-box's port
         * as a single message.
         *
         * @param   inputs      The test inputs to inject.
         */
        protected void inject(Object[] inputs)
        {
            // there must be at least one input in the given list
            if (inputs.length == 0) return;
            
            // for each test input
            message m = new message();
            double e = Double.MAX_VALUE;
            for (int i = 0; i < inputs.length; i++) {
                // add a content for this input to the message to
                // be injected
                TestInput input = (TestInput)inputs[i];
                m.add(new content(input.portName, input.value));

                // if this input has the smallest e value so far, record
                // that e value
                e = Math.min(e, input.e);
            }

            // inject the message into the component's simulator with the
            // least e value found above
            component.getSimulator().simInject(e, m);

            // inform the model view
            modelView.inputInjected();
        }
    }
}

