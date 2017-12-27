/**
 * DRelation is an abstraction of the graphical and functional 
 * interactions between 
 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponents</a> 
 * in a
 * <a href="{@docRoot}/com/acims/Diagrams/Diagram.html">Diagram</a>. 
 * It defines attributes and methods DRelation specializations 
 * must implement.
 * <p> 
 * Specializations of DRelation describe the interactions between 
 * two components of like or differing type. However, the 
 * <a href="{@docRoot}/com/acims/diagrams/DiagramRelationship.html">Relationship</a> 
 * class binds a DRelation object to 
 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
 * objects to form a relationship.
 * <p>
 * It is the responsibility of a 
 * <a href="{@docRoot}/com/acims/Diagrams/DiagramAttributeSet.html">DiagramAttributeSet</a> 
 * specialization to determine the correct DRelation 
 * specialization for a relationship and return the correct 
 * it to the 
 * <a href="{@docRoot}/com/acims/diagrams/Diagram.html">Diagram</a>. 
 * <p>
 * A useful specialization of DRelation is 
 * <a href="{@docRoot}/com/acims/Graphics/DecoratedLine.html">DecoratedLine</a>.
 * <p>
 * @see <a href="{@docRoot}/com/acims/Diagrams/Diagram.html">Diagram</a>
 * @see <a href="{@docRoot}/com/acims/Diagrams/DiagramAttributeSet.html">DiagramAttributeSet</a>
 * @see <a href="{@docRoot}/com/acims/Graphics/DecoratedLine.html">DecoratedLine</a>
 * @author Robert Flasher 
 * @version 1.1
 *
 */

package view.acims.diagrams;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Point;


public abstract class DRelation {

	/**
	 * Canvas where DRelation is drawn
	 */
	protected Graphics2D g;
	/**
	 * Starting point of the DRelation on a xy plane.
	 */
	protected Point start;
	/**
	 * End point of the DRelation on a xy plane.
	 */
	protected Point end;
	/**
	 * Name of the DRelation on a xy plane.
	 */
	protected String label = "";
	/**
	 * Length of the DRelation on a xy plane. 
	 * <p>
	 * Useful in calculations where the length of the DRelation is
	 * needed rather than its position.
	 */
	protected double dRelationLength = 0;
	/**
	 * Text color of the DRelation's name, if it is displayed.
	 * <p>
	 * The default is black.
	 */
	protected Color textColor = Color.BLACK;
	/**
	 * The color of the DRelation.
	 * <p>
	 * Default is black.
	 */
	protected Color lineColor = textColor;
	/**
	 * The background color of the canvas.
	 * <p>
	 * The default is white.
	 */
	protected Color backgroundColor = Color.WHITE;
	/**
	 * Description of the type when many DRelation types 
	 * exist in a Diagram.
	 */
	protected String type = "line";
	/**
	 * Draws the DRelation graphical representation on the 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Graphics2D.html">Graphics2D</a> 
	 * object g2D.
	 * <p>
	 * This method is called by 
	 * <a href="{@docRoot}/com/acims/diagrams/Diagram.html">Diagram</a> 
	 * when it is ready for the DRelation's graphics 
	 * representation to be drawn to the Diagram's graphics 
	 * context (g2D).
	 *
	 * @param g2D <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Graphics2D.html">Graphics2D</a> 
	 * object where the DComponent is drawn.
	 */
	public abstract void drawDRelation(Point begin, Point end, Graphics2D g2D, String XLabel);
	/**
	 * Returns the name of the DRelation.
	 * 
	 * @return Name of the DRelation.
	 */
	public abstract String getLabel();
	/**
	 * Returns the DRelation type description.
	 * @return {@link #type}
	 */
	public abstract String getType();
	/**
	 * Determines whether the  
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * p resides on the DRelation.
	 * @param p <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * to be tested.
	 * @return True if 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * p is on the DRelation, otherwise false.
	 */
	public abstract boolean isOnDRelation(Point p);
	/**
	 * Sets the name of the DRelation.
	 * <p>
	 * @param text New name of the DRelation
	 */
	public abstract void setLabel(String text);
	/**
	 * Sets the DRelation type.
	 * @param relType Sets {@link #type}
	 */
	public abstract void setType(String relType);
	/**
	 * Sets the colors of the DRelation.
	 * @param lblColor text color
	 * @param lnColor line color
	 * @param bgColor background color
	 */
	public abstract void setColors(Color lblColor, Color lnColor, Color bgColor);
}
