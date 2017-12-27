/**
 * A view meant to depict aspects of a digraphs devs component, such as
 * which child devs components its contains.
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

import model.modeling.*;
import util.*;
import view.simView.*;


public class DigraphView extends JPanel implements ComponentView
{
    /**
     * A cache of the size values for when this view displays its digraph
     * as a black box.
     */
    protected int blackBoxWidth, blackBoxHeight;

    /**
     * A mapping of port names to port boxes that are associated with this view.
     */
    protected Map nameToPortBox = new HashMap();

    /**
     * The middle portion of this view, that displays the digraph's
     * subcomponent views.
     */
    protected JPanel componentsPanel;

    /**
     * The simview model-view that contains this view,
     * to which this view might add components, such as content views.
     */
    protected SimView.ModelView modelView;

    /**
     * The digraph being depicted.
     */
    protected ViewableDigraph digraph;

    /**
     * The font used when drawing this digraph's name, along with the
     * font's associated metrics object, and the dimensions of the name
     * string when drawn in this font.
     */
    protected Font nameFont = new Font("SansSerif", Font.PLAIN, 12);
    protected FontMetrics nameFontMetrics = getFontMetrics(nameFont);
    protected int nameWidth, nameAscent = nameFontMetrics.getAscent();

    /**
     * Constructs a digraph view on the given digraph.
     *
     * @param   digraph_        The digraph on which to construct this view.
     * @param   modelView_      The sim-view model-view that will contain this
     *                          view.
     */
    public DigraphView(ViewableDigraph digraph_, SimView.ModelView modelView_)
    {
        digraph = digraph_;
        modelView = modelView_;
        
        setOpaque(false);
        setOpaque(false);

        setLayout(new BoxLayout(this, BoxLayout.X_AXIS));

        // create the drag-listener for this view
        DragViewListener dragListener = new DragViewListener(this, modelView);

        // add the inports panel
        JPanel inportsPanel;
        JPanel panel = inportsPanel = new JPanel();
        panel.setOpaque(false);
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        add(panel);

        ComponentViewUtil.createPortBoxes(panel, digraph.getInportNames(),
            true, false, nameToPortBox, digraph, modelView, dragListener);

        // add the components panel
        panel = componentsPanel = new ComponentsPanel();
        panel.setOpaque(false);
        panel.setLayout(null);
        add(panel);
        panel.addMouseListener(dragListener);
        panel.addMouseMotionListener(dragListener);
        
        // add the outports panel
        JPanel outportsPanel;
        panel = outportsPanel = new JPanel();
        panel.setOpaque(false);
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        add(panel);

        ComponentViewUtil.createPortBoxes(panel, digraph.getOutportNames(),
            false, true, nameToPortBox, null, modelView, dragListener);

        // cache the width of the name string
        String name = digraph.getName();
        nameWidth = nameFontMetrics.stringWidth(name);

        // cache the minimum size of this component when displayed as a
        // black box
        blackBoxWidth = nameWidth + 2 * 10
            + inportsPanel.getPreferredSize().width
            + outportsPanel.getPreferredSize().width;
        blackBoxHeight = Math.max(digraph.getNumInports(),
            digraph.getNumOutports()) * PortBox.nameFontAscent * 3 / 2;
        blackBoxHeight = Math.max(blackBoxHeight,
            nameFontMetrics.getHeight() + 2 * 5);
        
    }

    /**
     * Draws this view's border, and the name of the digraph.
     */
    public void paint(Graphics g)
    {
        // draw a line border around this view
        int width = getWidth();
        g.drawRect(0, 0, width - 1, getHeight() - 1);

        super.paint(g);
    }

    /**
     * Returns where this view would like its upper-left corner to be
     * positioned, relative to its parent component.
     */
    public Point getPreferredLocation() {return digraph.getPreferredLocation();}

    /**
     * Returns how large this view would like to be.
     */
    public Dimension getPreferredSize()
    {
        if (!digraph.isBlackBox()) {
            return digraph.getPreferredSize();
        }

        return new Dimension(blackBoxWidth, blackBoxHeight);
    }

    /**
     * Overrides the behavior of the parent method to add the given component
     * to this view's component's panel, rather than directly to this view.
     */
    public void add(Component comp, Object constraints)
    {
        // if the given component is an atomic-view or a digraph-view
        if (comp instanceof AtomicView || comp instanceof DigraphView) {
            // add it to the components-panel, instead of directly to this
            // digraph-view
            componentsPanel.add(comp, constraints);
            return;
        }

        super.add(comp, constraints);
    }

     // allows dymic model removal
    public void remove(Component comp,Object constraints){
        if (comp instanceof AtomicView || comp instanceof DigraphView) {
            // add it to the components-panel, instead of directly to this
            // digraph-view
            componentsPanel.remove(comp);
            return;
        }
        super.remove(comp);
    }

    /**
     * Returns the offset within this view of the lollipop circle
     * of the port-box associated with the port of the given name.
     *
     * @param   portName        The port whose port-box pollipop location
     *                          should be returned.
     * @return                  The offset of the port-box's lollipop within
     *                          this view.
     */
    public Point getPortLocation(String portName)
    {
        return ComponentViewUtil.getPortLocation(this, portName, nameToPortBox);
    }

    /**
     * Returns the viewable devs component on which this is a view.
     */
    public ViewableComponent getViewableComponent() {return digraph;}

    /**
     * Returns the viewable-digraph on which this is a view.
     */
    public ViewableDigraph getDigraph() {return digraph;}

    /**
     * Injects all test inputs on their associated inports.
     */
    public void injectAll() {ComponentViewUtil.injectAll(this);}

    /**
     * The panel that displays the subcomponent's of this view's digraph.
     */
    protected class ComponentsPanel extends JPanel
    {
        /**
         * A cache of the rectangle enclosing this panel's name display.
         * This rectangle is the only area within this entire view 
         * that the view's tooltip will be shown.
         */
        protected Rectangle nameBox = new Rectangle();
        
        /**
         * Constructor.
         */
        public ComponentsPanel() 
        {
            // when the mouse cursor enters this panel
            addMouseListener(new MouseAdapter() {
                public void mouseEntered(MouseEvent e) {
                    updateTooltip();
                }
            });
            
        }

        /**
         * See parent method.
         */
        public void paint(Graphics g)
        {
            // if we haven't yet cached the rectangular area
            // enclosing this panel's name display
            if (nameBox.height == 0) {
                // do so
                nameBox.x = getWidth() / 2 - nameWidth / 2;
                nameBox.y = 0;
                nameBox.width = nameWidth;
                nameBox.height = nameAscent;
            }
            
            
            
            
            // draw the component's name centered at the top of this view
            g.setFont(nameFont);
            String name = digraph.getName();
            g.drawString(name, getWidth() / 2 - nameWidth / 2, nameAscent);

            // don't let the digraph's subcomponents be drawn if the
            // digraph is being displayed as a black box
            if (digraph.isBlackBox()) return;

            super.paint(g);
        }
        
        /**
         * See parent method.
         */
        public String getToolTipText(MouseEvent event)
        {
            // if the mouse is over this view's name display
            if (nameBox.contains(event.getPoint())) {
                // display a tooltip
                return getToolTipText();
            }
            
            // otherwise, don't display any tooltip
            return null;
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
            text.append(StringUtil.replaceAll(
                digraph.getTooltipText(), "\n", "<br>"));

            // add the closing html
            text.append("</font></body></html>");

            setToolTipText(text.toString());
        }
    }
    
    public SimView.ModelView getModelView(){return this.modelView;}

}