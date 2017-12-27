/**
 * A view meant to depict aspects of an atomic devs component, such as
 * its name, its state, and its ports.
 *
 * @author      Jeff Mather
 */

package view.modeling;

import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.util.List;
import javax.swing.*;
import javax.swing.event.*;

import GenCol.*;


import model.modeling.*;
import model.simulation.*;
import util.*;
import view.simView.*;


public class AtomicView extends JPanel implements ComponentView
{
    /**
     * A mapping of port names to port boxes that are associated with this view.
     */
    protected Map nameToPortBox = new HashMap();

    /**
     * The atomic devs component this view is to depict.
     */
    protected ViewableAtomic atomic;

    /**
     * The main body portion of this view, which displays the name and state
     * of the associated atomic component.
     */
    protected CompBox compBox;

    /**
     * The panels displaying the inports and outports of the atomic component.
     */
    protected JPanel inportsPanel, outportsPanel;

    /**
     * The simview model-view that contains this view,
     * to which this view might add components, such as content views.
     */
    protected SimView.ModelView modelView;

    /**
     * Constructs a view on the given atomic component.
     *
     * @param   atomic_         The component to be viewed.
     * @param   modelView_      The sim-view model-view that will contain this
     *                          view.
     */
    public AtomicView(ViewableAtomic atomic_, SimView.ModelView modelView_)
    {
        atomic = atomic_;
        modelView = modelView_;

        setOpaque(false);

        setLayout(new BoxLayout(this, BoxLayout.X_AXIS));

        // add the inports panel
        JPanel panel = inportsPanel = new JPanel();
        panel.setOpaque(false);
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        add(panel);

        ComponentViewUtil.createPortBoxes(panel, atomic.getInportNames(),
            true, true, nameToPortBox, atomic, modelView, null);

        // add the component box
        compBox = new CompBox();
        add(compBox);

        // add the outports panel
        panel = outportsPanel = new JPanel();
        panel.setOpaque(false);
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        add(panel);

        ComponentViewUtil.createPortBoxes(panel, atomic.getOutportNames(),
            false, false, nameToPortBox, atomic, modelView, null);
    }

    /**
     * The main body portion of this view, which displays the name and state
     * of the associated atomic component.
     */
    protected class CompBox extends JPanel
    {
        /**
         * The font used when drawing the atomic's name, along with the
         * font's associated metrics object.
         */
        protected Font nameFont = new Font("SansSerif", Font.BOLD, 12);
        protected FontMetrics nameFontMetrics = getFontMetrics(nameFont);

        /**
         * The font used when drawing the atomic's phase, along with the
         * font's associated metrics object.
         */
        protected Font phaseFont = new Font("SansSerif", Font.BOLD, 14);
        protected FontMetrics phaseFontMetrics = getFontMetrics(phaseFont);

        /**
         * The width (in pixels) of the atomic's name string.
         */
        protected int nameWidth = nameFontMetrics.stringWidth(atomic.getName());

        /**
         * Constructor.
         */
        public CompBox() 
        {
            // this ensures my tooltip will show up right away even if the mouse
            // starts over me when I'm first shown
            setToolTipText("");
            
            // when the mouse cursor enters this comp-box
            addMouseListener(new MouseAdapter() {
                public void mouseEntered(MouseEvent e) {
                    updateTooltip();
                }
            });

            // add a drag-listener 
            DragViewListener listener = new DragViewListener(
                AtomicView.this, modelView);
            addMouseListener(listener);
            addMouseMotionListener(listener);
        }
        
        /**
         * Limits this box's size to its preferred size.
         */
        public Dimension getMaximumSize() {return getPreferredSize();}

        /**
         * Returns how big this box should be sized.
         */
        public Dimension getPreferredSize()
        {
            Dimension size = new Dimension();

            // the preferred with is the maximum of the string width of the
            // atomic's name and a fixed amount
            size.width = Math.max(nameWidth + 10, 100);

            // the preferred height is the maximum of the
            // phase name text height, and the height needed to display
            // the in- or out-ports names when arranged vertically
            size.height = Math.max((phaseFontMetrics.getAscent() + 2) * 3,
                Math.max(atomic.getNumInports(), atomic.getNumOutports()) *
                PortBox.nameFontAscent * 3 / 2);

            return size;
        }

        /**
         * Draws the name, phase, sigma, etc. of the associated atomic
         * component in this box.
         */
        public void paint(Graphics g)
        {
            // fill my background
            g.setColor(atomic.getBackgroundColor());
            g.fillRect(0, 0, getWidth(), getHeight());

            // draw my atomic's name
            g.setColor(Color.black);
            g.setFont(nameFont);
            g.drawString(atomic.getName(),
                getWidth() / 2 - nameWidth / 2,
                nameFontMetrics.getAscent() + 2);

            // draw my atomic's phase
            g.setColor(Color.blue);
            g.setFont(phaseFont);
            String phase = atomic.getFormattedPhase();
            if (phase == null) phase = "no phase";
            g.drawString(phase,
                getWidth() / 2 - phaseFontMetrics.stringWidth(phase) / 2,
                getHeight() / 2 + phaseFontMetrics.getAscent() / 2 - 1);

            // draw my atomic's sigma
            g.setColor(Color.black);
            g.setFont(nameFont);
            String sigma = "\u03C3 = " + atomic.getFormattedSigma();
            g.drawString(sigma,
                getWidth() / 2 - nameFontMetrics.stringWidth(sigma) / 2,
                getHeight() - 4);
         }
    }

    /**
     * Informs this view that the phase of the associated atomic component
     * has changed.
     */
    public void phaseChanged() {repaint();}

    /**
     * Informs this view that the sigma of the associated atomic component
     * has changed.
     */
    public void sigmaChanged() {repaint();}

    /**
     * Limits the size of this atomic view to its preferred size.
     */
    public Dimension getMaximumSize() {return getPreferredSize();}

    /**
     * Returns the preferred size of this atomic view's comp-box, plus
     * added width to hold its inports and outports panels.
     */
    public Dimension getPreferredSize()
    {
        Dimension size = compBox.getPreferredSize();
        size.width += inportsPanel.getPreferredSize().width +
            outportsPanel.getPreferredSize().width;
        return size;
    }

    /**
     * Updates this atomic view's tooltip text with the current state from
     * the atomic.
     */
    protected void updateTooltip()
    {
        StringBuffer text = new StringBuffer();

        // add the opening html
        text.append(HtmlUtil.yellowTooltipHeader);

        // add the atomic's state
        text.append(StringUtil.replaceAll(atomic.getTooltipText(), "\n", "<br>"));

        // add the closing html
        text.append("</font></body></html>");

        compBox.setToolTipText(text.toString());
    }

    /**
     * Returns the offset within this atomic view of the lollipop circle
     * of the port-box associated with the port of the given name.
     *
     * @param   portName        The port whose port-box pollipop location
     *                          should be returned.
     * @return                  The offset of the port-box's lollipop within
     *                          this atomic view.
     */
    public Point getPortLocation(String portName)
    {
        return ComponentViewUtil.getPortLocation(this, portName, nameToPortBox);
    }

    /**
     * Injects all test inputs on their associated inports.
     */
    public void injectAll() {ComponentViewUtil.injectAll(this);}

    /**
     * Returns where this view would like its upper-left corner to be
     * positioned, relative to its parent component.
     */
    public Point getPreferredLocation() {return atomic.getPreferredLocation();}

    /**
     * Returns the viewable devs component on which this is a view.
     */
    public ViewableComponent getViewableComponent() {return atomic;}

    /**
     * Returns the viewable atomic on which this is a view.
     */
    public ViewableAtomic getAtomic() {return atomic;}
    
    public SimView.ModelView getModelView(){return this.modelView;}
}
