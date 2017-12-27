/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
package view.modeling;


import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import util.*;
import view.simView.*;

/**
 * A mouse-event listener that allows its associated view to be dragged
 * about its parent view.
 */
public class DragViewListener extends MouseInputAdapter
{
    /**
     * The displacement during the drag between the mouse cursor
     * and the upper-left corner of this view.
     */
    protected Point cursorDeltaFromView;

    /**
     * The view on which this listener is supposed to listen for drag events.
     */
    protected JComponent view;

    /**
     * The model-view containing the component-view on which to listen.
     */
    protected SimView.ModelView modelView;

    /**
     * Whether the current drag is for a resize, rather than a move.
     */
    protected boolean resizing;

    /**
     * The resize mouse cursor currently in use.  While a resize isn't in
     * process, this will be null.
     */
    protected Cursor resizeCursor;

    /**
     * Constructs a drag-view-listener on the given view.
     *
     * @param   view        The devs-component-view on which to listen for
     *                      drag events.
     */
    public DragViewListener(JComponent view_, SimView.ModelView modelView_)
    {
        view = view_;
        modelView = modelView_;
    }

    /**
     * See parent method.
     */
    public void mousePressed(MouseEvent e)
    {
        e = convertEvent(e);

        // this may be the start of a drag, so remember where the
        // mouse cursor is in relation to this view, that this
        // delta may be maintained during the drag
        cursorDeltaFromView = e.getPoint();

        // if this listener's view is a digraph-view
        resizing = false;
        if (view instanceof DigraphView) {
            // if the mouse cursor is in a position to initiate a resize
            if (resizeCursor != null) {
                // the drag is actually for a resize, not a move
                resizing = true;
            }
        }
    }

    /**
     * If warranted, converts the coordinates of the given mouse-event
     * to the coordinate space of this listener's associated view.  This
     * is necessary when this listener is added to a component that is
     * not the associated draggable view itself.
     *
     * @param       The mouse event whose coordinates might need to
     *              be converted.
     * @return      The (perhaps) converted event.
     */
    protected MouseEvent convertEvent(MouseEvent e)
    {
        // if the event source isn't the view that can be dragged
        if (e.getSource() != view) {
            // convert the mouse event coordinates to the coordinate
            // space of the draggable view
            e = SwingUtilities.convertMouseEvent((Component)e.getSource(),
                e, view);
        }

        return e;
    }

    /**
     * See parent method.
     */
    public void mouseMoved(MouseEvent e)
    {
        // this method only applies to digraph-views
        if (!(view instanceof DigraphView)) return;

        // this method only applies if a resize isn't currently in progress
        if (resizing) return;

        e = convertEvent(e);

        // if the move occurred within the resize area of the view
        Point location = e.getPoint();
        detmResizeCursor(location);
        if (resizeCursor != null) {
            // use the resize mouse cursor
            modelView.setCursor(resizeCursor);
        }

        // otherwise
        else {
            // use the normal mouse cursor
            modelView.setCursor(Cursor.getDefaultCursor());
        }
    }

    /**
     * See parent method.
     */
    public void mouseExited(MouseEvent e)
    {
        if (!resizing) {
            // use the normal mouse cursor
            modelView.setCursor(Cursor.getDefaultCursor());
        }
    }

    /**
     * See parent method.
     */
    public void mouseReleased(MouseEvent e)
    {
        resizing = false;

        // use the normal mouse cursor
        modelView.setCursor(Cursor.getDefaultCursor());
    }

    /**
     * Determines which resize cursor to use (if any), based on the mouse
     * occupying the given location within this listener's associated view.
     *
     * @param   location    The position of the mouse cursor within this
     *                      listener's associated view.
     */
    protected void detmResizeCursor(Point location)
    {
        // if the mouse location is within any of the borders of this
        // listener's associated view, determine the appropriate resize
        // cursor type
        final int borderWidth = 6;
        int type = Cursor.DEFAULT_CURSOR;
        final int x = location.x, y = location.y,
            width = view.getWidth(), height = view.getHeight();
        if (x >= width - borderWidth && y >= height - borderWidth) {
            type = Cursor.SE_RESIZE_CURSOR;
        }
        else if (x >= width - borderWidth && y < borderWidth) {
            type = Cursor.NE_RESIZE_CURSOR;
        }
        else if (x < borderWidth && y >= height - borderWidth) {
            type = Cursor.SW_RESIZE_CURSOR;
        }
        else if (x < borderWidth && y < borderWidth) {
            type = Cursor.NW_RESIZE_CURSOR;
        }
        else if (x < borderWidth) {
            type = Cursor.W_RESIZE_CURSOR;
        }
        else if (y < borderWidth) {
            type = Cursor.N_RESIZE_CURSOR;
        }
        else if (x >= width - borderWidth) {
            type = Cursor.E_RESIZE_CURSOR;
        }
        else if (y >= height - borderWidth) {
            type = Cursor.S_RESIZE_CURSOR;
        }

        // obtain the cursor of the type detm'd above
        resizeCursor = (type != Cursor.DEFAULT_CURSOR) ?
            Cursor.getPredefinedCursor(type) : null;
    }

    /**
     * See parent method.
     */
    public void mouseDragged(MouseEvent e)
    {
    	
        e = convertEvent(e);

        // if the drag is for a resize
        Point location = e.getPoint();
        if (resizing) {
            // update the view's size to make it extend to the drag point
            resizeView(location);
            view.revalidate();

            // update the associated viewable-digraph's preferred size
            ViewableDigraph digraph = (ViewableDigraph)
                ((ComponentView)view).getViewableComponent();
            digraph.setPreferredSize(
                new Dimension(location.x, location.y));
        }

        // otherwise, the drag is for a move
        else {
            // move this view by the distance dragged
            PointUtil.translate(location, view.getLocation());
            PointUtil.negativeTranslate(location, cursorDeltaFromView);
            view.setLocation(location);

            // if the view is a component-view
            if (view instanceof ComponentView) {
                // update the associated viewable component's preferred
                // location
                ((ComponentView)view).getViewableComponent().
                    setPreferredLocation(location);

                // for each parent component of the view up its ancestry chain
                // (until we find this view's parent digraph-view, or the
                // model-view itself)
                Container parent = view.getParent();
                while (true) {
                    // if this parent is itself a digraph view
                    if (parent instanceof DigraphView) {
                        // tell the parent's associated viewable-digraph that its
                        // layout has changed
                        ((DigraphView)parent).getDigraph().setLayoutChanged(true);
                        break;
                    }

                    // if the next ancestor up is the model-view, or is null,
                    // then quit
                    parent = parent.getParent();
                    if (parent == modelView || parent == null) break;
                }
            }
        }

        // couplings might need to be redrawn, so repaint the whole model-view
        modelView.repaint();
    }

    /**
     * Resizes this listener's associated view based on the given
     * drag-location, as well as the direction of the resize being performed.
     *
     * @param   dragLocation    The position of the mouse cursor performing
     *                          the drag, using the coordinate space of the
     *                          associated view.
     */
    protected void resizeView(Point dragLocation)
    {
        // if no resize is being performed, quit
        if (resizeCursor == null) return;

        // perform the appropriate resize of the view, according to
        // the direction of the resize
        final int x = dragLocation.x, y = dragLocation.y,
            viewx = view.getX(), viewy = view.getY(),
            width = view.getWidth(), height = view.getHeight();
        int type = resizeCursor.getType();
        if (type == Cursor.SE_RESIZE_CURSOR) {
            view.setSize(x, y);
        }
        else if (type == Cursor.NW_RESIZE_CURSOR) {
            view.setBounds(viewx + x, viewy + y, width - x, height - y);
        }
        else if (type == Cursor.SW_RESIZE_CURSOR) {
            view.setBounds(viewx + x, viewy, width - x, y);
        }
        else if (type == Cursor.NE_RESIZE_CURSOR) {
            view.setBounds(viewx, viewy + y, x, height - y);
        }
        else if (type == Cursor.N_RESIZE_CURSOR) {
            view.setBounds(viewx, viewy + y, width, height - y);
        }
        else if (type == Cursor.S_RESIZE_CURSOR) {
            view.setBounds(viewx, viewy, width, y);
        }
        else if (type == Cursor.W_RESIZE_CURSOR) {
            view.setBounds(viewx + x, viewy, width - x, height);
        }
        else if (type == Cursor.E_RESIZE_CURSOR) {
            view.setBounds(viewx, viewy, x, height);
        }
    }
}

