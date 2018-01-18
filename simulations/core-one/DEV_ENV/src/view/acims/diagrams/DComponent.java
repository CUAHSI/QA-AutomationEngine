/**
 * DComponent specializations are the component types in a   
 * <a href="{@docRoot}/com/acims/diagrams/Diagram.html">Diagram</a>. 
 * The DComponent abstract class defines the attributes and methods 
 * DComponent specializations must implement. 
 * <p> 
 * It is the responsibility of a 
 * <a href="{@docRoot}/com/acims/Diagrams/DiagramAttributeSet.html">DiagramAttributeSet</a> 
 * specialization to determine the suitable DComponent 
 * specialization and return the object to the 
 * <a href="{@docRoot}/com/acims/diagrams/Diagram.html">Diagram</a>. 
 * <p>
 * A specialized DComponent class with many useful shapes is 
 * <a href="{@docRoot}/com/acims/Graphics/DecoratedShape.html">DecoratedShape</a>.
 * <p>
 * @see <a href="{@docRoot}/com/acims/diagrams/Diagram.html">Diagram</a>
 * @see <a href="{@docRoot}/com/acims/diagrams/DiagramAttributeSet.html">DiagramAttributeSet</a>
 * @see <a href="{@docRoot}/com/acims/Graphics/DecoratedShape.html">DecoratedShape</a>
 * @author Robert Flasher
 * @version 1.1
 *
 */

package view.acims.diagrams;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Point;

import view.acims.Graphics.*;

public abstract class DComponent {

	/**
	 * Fill color of the DComponent where white is the default.
	 */
	protected Color backgroundColor = Color.WHITE;
	
	/**
	 * Upper left corner of the DComponent.
	 */
	protected Point start = new Point(0,0);
	
	/**
	 * Center of the DComponent. 
	 */
	protected Point center = start;
	
	/**
	 * Shape of DComponent. 
	 */
	protected int dCompShape = DecoratedShape.FILLED_RECTANGLE;
	/**
	 * Canvas where DComponent is drawn. 
	 */
	protected Graphics2D g;
	
	/**
	 * The name of the DComponent.
	 */
	protected String label = "";
	
	/**
	 * Description of the type of DComponent.
	 */
	protected String type = "Component";
	
	/**
	 * Color of DComponent outline where black is default.
	 */
	protected Color lineColor = Color.BLACK;
	
	/**
	 * Color of DComponent's text where black is default.
	 */
	protected Color textColor = lineColor;
	
	/**
	 * Length of the DComponent in the x direction.
	 */
	protected int xLength = 0;
	
	/**
	 * Length of the DComponent in the y direction.
	 */
	protected int yLength = 0;
	
	/**
	 * Draws the DComponent's graphical representation on the 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Graphics2D.html">Graphics2D</a> 
	 * object g2D.
	 * <p>
	 * This method is called by 
	 * <a href="{@docRoot}/com/acims/diagrams/Diagram.html">Diagram</a> 
	 * when it is ready for the DComponent's graphics 
	 * representation to be drawn to the Diagram's graphics 
	 * context (g2D).
	 * @param g2D <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Graphics2D.html">Graphics2D</a> 
	 * object where the DComponent is drawn.
	 */
	public abstract void drawDComponent(Graphics2D g2D);
	
	/**
	 * Returns the 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * located at the center of the DComponent.
	 * @return Center of the DComponent.
	 */
	public abstract Point getCenter();
	
	/**
	 * Return the 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * on the DComponent closest to 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * p.
	 * @param p <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * on a two dimensional plane.
	 * @return <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * on the DComponent closest to p.
	 */
	public abstract Point getClosestPointOnDComp(Point p);
	
	/**
	 * The 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * with the x and y lengths of the DComponent.
	 * <p>
	 * @return <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * = (x length of the DComponent, y length of the DComponent).
	 */
	public abstract Point getDimensions();
	
	/**
	 * Returns the name of the DComponent.
	 * <p>
	 * @return Name of the DComponent.
	 */
	public abstract String getLabel();
	
	/**
	 * Returns the DComponent type description.
	 * @return {@link #type}
	 */
	public abstract String getType();
	/**
	 * Returns the 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * located at the upper left hand corner of the DComponent.
	 * @return <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * location of the DComponent.
	 */
	public abstract Point getPosition();
	
	/**
	 * Determines whether the  
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * p resides on the DComponent.
	 * @param p <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * to be tested.
	 * @return True if 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * p is on the DComponent, otherwise false.
	 */
	public abstract boolean isOnDComp(Point p);
	
	/**
	 * Sets the two dimensional size of the DComponent.
	 * <p>
	 * @param dim 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * dim = (x length of DComponent, y length of Component).
	 */
	public abstract void setDimensions(Point dim);
	/**
	 * Positions the upper left corner of the DComponent on the 
	 * <a href="{@docRoot}/com/acims/diagrams/Diagram.html">Diagram</a>
	 * at 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * nPos.
	 * @param nPos <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * nPos = (new x-coordinate of the DComponent, new y-coordinate of the DComponent)
	 */
	public abstract void setDCompPosition(Point nPos);
	/**
	 * Sets the required attributes of the DComponent.
	 * <p>
	 * This method sets the position of the DComponent, the type of DComponent, 
	 * and the name of the DComponent using the input parameter. It, also, 
	 * sets initial dimension lengths.
	 * <p>
	 * Generally, this method is called by a 
	 * <a href="{@docRoot}/com/acims/diagrams/DiagramAttributeSet.html">DiagramAttributeSet</a> 
	 * specialization after the DComponent is added to the 
	 * <a href="{@docRoot}/com/acims/diagrams/Diagram.html">Diagram</a> 
	 * by a user program before the Diagram calls 
	 * {@link #drawDComponent(Graphics2D)}. 
	 * @param pos <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * location of the DComponent in a two dimesional plane.
	 * @param shape int value that represents a type or shape when
	 * a specialized DComponent implementation defines more than
	 * one type or shape.
	 * @param text Name of the DComponent.
	 */
	public abstract void setShape(Point pos, int shape, String text);
	
	/**
	 * Sets the DComponent type description.
	 * @param compType Sets {@link #type}
	 */
	public abstract void setType(String compType);
}
