/**
 * This abstract class must be implemented whenever a 
 * <a href="{@docRoot}/com/acims/Diagrams/Diagram.html">Diagram</a> 
 * is implemented. DiagramAttributeSet specializations fullfill 
 * four responsibilities to support the implementation of
 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponents</a> 
 * and 
 * <a href="{@docRoot}/com/acims/Diagrams/DRelations.html">DRelations</a> 
 * specializations within a diagram. First, DiagramAttributeSet 
 * specializations define the possible DComponents and DRelations 
 * specializations that can be used in a 
 * Diagram's implementation. Second, DiagramAttributeSets 
 * provide logic to determine, which DComponent or DRelation 
 * specialization to initialize and return to the Diagram 
 * when there is more than on possibility.
 * Third, it enables interactions between DComponents 
 * defined by DRelations specializations. 
 * Finally, it sets most of the DComponent and DRelation 
 * attributes.
 * 
 * @author Robert Flasher
 *
 */

package view.acims.diagrams;

import java.awt.Color;
import java.awt.Font;
import java.awt.Point;
import java.util.Vector;

import view.acims.Graphics.DecoratedLine;
import view.acims.Graphics.DecoratedShape;



public abstract class DiagramAttributeSet {
	/**
	 * The
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * outline color and 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * line color where black is the default.
	 */
	protected Color lineColor = Color.BLACK;
	/**
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * fill color where white is the default.
	 */
	protected Color fillColor = Color.WHITE;
	/**
	 * Text color where black is the default.
	 */
	protected Color labelColor = lineColor;
	/**
	 * The shape of the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * implemented, where the default is 
	 * <a href="{@docRoot}/com/acims/Graphics/DecoratedShape.html#ROUNDED_RECTANGLE">
	 * ROUNDED_RECTANGLE</a>.
	 */
	protected int dComponentShape = DecoratedShape.ROUNDED_RECTANGLE;
	/**
	 * Abstract description of the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a>.
	 * <p>
	 * An example would be "State" for a state chart.
	 */
	protected String dComponentDescription = "shape";
	/**
	 * Point dComponentDimensions = (x length of DComponent, y length of DComponent)
	 */
	protected Point dComponentDimensions = new Point(0,0);
	/**
	 * Is true if the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * is an arc line, and false otherwise. The default is false.
	 */
	protected boolean arc = false;
	/**
	 * Pixel height of the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * half ellipse arc line when arc is true. 
	 */
	protected int arcHeight = 25;
	/**
	 * Abstract description of the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a>.
	 * <p>
	 * An example would be "Transition" for a state chart.
	 */
	protected String dRelationDescription = "connector";
	/**
	 * End shape of a 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * line, where the default is 
	 * <a href="{@docRoot}/com/acims/Graphics/DecoratedLine.html#NO_CAP">
	 * NO_CAP</a>
	 * <p>
	 * If end caps are used, they must be implemented as part of the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * specialization used.
	 */
	protected int endCap = DecoratedLine.NO_CAP;
	/**
	 * The height in pixels of a 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a>'s 
	 * line end cap.
	 */
	protected int endCapHeight = 0;
	/**
	 * The Width in pixels of a 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a>'s 
	 * line end cap.
	 */
	protected int endCapWidth = 0;
	/**
	 * The font used for 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponents</a> 
	 * or 
	 * <a href="{@docRoot}/com/acims/Diagrams/Line.html">DRelations</a>, where
	 * the default is "Arial", bold, and 12 pt.
	 */
	protected Font font = new Font("Arial", Font.BOLD, 12);
	
	/**
	 * Returns the pixel height for a half ellipse  
	 * DRelation.
	 * <p>
	 * @return {@link #arcHeight}
	 */
	public int getArcHeight(){
		return arcHeight;
	}
	/**
	 * Sets the pixel height for a half ellipse  
	 * DRelation.
	 * <p>
	 * @param height new {@link #arcHeight}
	 */
	public void setArcHeight(int height){
		arcHeight = height;
	}
	/**
	 * Returns the end cap type.
	 * @return {@link #endCap}
	 */
	public int getEndCap(){
		return endCap;
	}
	/**
	 * Sets the end cap type.
	 * @param endCapShape new {@link #endCap}
	 */
	public void setEndCap(int endCapShape){
		endCap = endCapShape;
	}
	/**
	 * Returns the pixel height of the end cap.
	 * @return {@link #endCapHeight}
	 */
	public int getEndCapHeight(){
		return endCapHeight;
	}
	/**
	 * Sets the pixel height of the end cap.
	 * @param height new {@link #endCapHeight}
	 */
	public void setEndCapHeight(int height){
		endCapHeight = height;
	}
	/**
	 * Returns the pixel width of the end cap.
	 * @return {@link #endCapWidth}
	 */
	public int getEndCapWidth(){
		return endCapWidth;
	}
	/**
	 * Sets the pixel width of the end cap.
	 * @param width new {@link #endCapWidth}
	 */
	public void setEndCapWidth(int width){
		endCapWidth = width;
	}
	/**
	 * Returns the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * fill 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Color.html">Color</a>.
	 * <p>
	 * @return {@link #fillColor} 
	 */
	public Color getFillColor(){
		return fillColor;
	}
	/**
	 * Sets the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * fill 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Color.html">Color</a>.
	 * <p>
	 * @param fill new {@link #fillColor} 
	 */
	public void setFillColor(Color fill){
		fillColor = fill;
	}
	/**
	 * Returns text 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Color.html">Color</a>.
	 * <p>
	 * @return {@link #labelColor} 
	 */
	public Color getLabelColor(){
		return labelColor;
	}
	/**
	 * Sets text 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Color.html">Color</a>.
	 * <p>
	 * @param lbColor new {@link #labelColor} 
	 */
	public void setLabelColor(Color lbColor){
		labelColor = lbColor;
	}
	/**
	 * Returns the  
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * outline and 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * line 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Color.html">Color</a>.
	 * <p>
	 * @return {@link #lineColor}
	 */
	public Color getLineColor(){
		return lineColor;
	}
	/**
	 * Sets the  
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * outline and 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * line 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Color.html">Color</a>.
	 * <p>
	 * @param lnColor new {@link #lineColor}
	 */
	public void setLineColor(Color lnColor){
		lineColor = lnColor;
	}
	/**
	 * Returns the {@link #dComponentShape} (type) identified by the 
	 * String s.
	 * @return {@link #dComponentShape}
	 */
	public int getDComponentShape(){
		return dComponentShape;
	}
	/**
	 * Sets the default {@link #dComponentShape}
	 * @param shape sets {@link #dComponentShape}
	 */
	public void setDComponentShape(int shape){
		dComponentShape = shape;
	}
	/**
	 * Returns the lengths of new instances of 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a>
	 * in the x and y directions. 
	 * @return {@link #dComponentDimensions}
	 */
	public Point getDComponentDimensions(){
		return dComponentDimensions;
	}
	/**
	 * Sets the x and y lengths of 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent(s)</a> 
	 * to be initialized.
	 * <p>
	 * These dimensions will be used to set the size of all 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponents</a> 
	 * being initialized until it is called again.
	 * @param d The 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * d = (x length of shape, y length of shape)
	 */
	public void setDComponentDimensions(Point d){
		dComponentDimensions = d;
	}
	/**
	 * Returns an instance of the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * specialization identified by desc.
	 * <p>
	 * The desc description helps to identify the type of DRelation 
	 * specialization that is needed. For instance,let's say there are two
	 * specializations ADRelation and BDRelation. A good value for desc would be
	 * "A". This method's implementation in a DiagramAttributeSet 
	 * specialization would return an instance of ADRelation.
	 * @param desc Description of the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * specialization object to be returned.
	 * @return A 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * specialization object.
	 */
	public abstract DRelation getDRelationContext(String desc);
	/**
	 * Sets the attribute values of a 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * consistent with the input operation.
	 * <p>
	 * If op = "ADD", then the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * part of 
	 * <a href="{@docRoot}/com/acims/Diagrams/Diagram.Relationship.html">
	 * Relationship</a> c should be set with any attributes of
	 * interest for the utilized 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * specialization. Some of the 
	 * attribues to be set could include: {@link #arc}, 
	 * {@link #arcHeight}, {@link #endCap}, {@link #endCapHeight} 
	 * and other attributes specific to the DRelation specialization. 
	 * The one 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * method that must be called by this method during an "ADD" is 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html#setLabel(java.lang.String)">
	 * setLabel(String)</a> 
	 * <p>
	 * The "ADD" operations must be implemented for 
	 * all DiagramAttributeSet
	 * specializations. Other operations can be implemented as
	 * needed to enable interaction along a DRelation between 
	 * DComponents.
	 * <p>
	 * This method is called by 
	 * <a href="{@docRoot}/com/acims/Diagrams/Diagram.html">Diagram</a> 
	 * whenever a user program calls a Diagram to perform an 
	 * operation affecting a DRelation object before the 
	 * DRelation is drawn or redrawn to the graphics context.
	 * 
	 * @param c <a href="{@docRoot}/com/acims/Diagrams/Diagram.Relationship.html">Relationship</a> 
	 * that contains the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * to be set.
	 * @param ln A <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/util/Vector.html">Vector</a>
	 * containing all the 
	 * <a href="{@docRoot}/com/acims/Diagrams/Diagram.Relationship.html">Relationships</a>  
	 * in the Diagram.
	 * @param sh A <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/util/Vector.html">Vector</a>
	 * containing all the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponents</a> 
	 * in the Diagram.
	 * @param op <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/lang/String.html">String</a> 
	 * description of the operation to be performed.
	 */
	public abstract void setDRelation(Diagram.Relationship c, Vector ln, Vector sh, String op);
	/**
	 * Returns an instance of the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * specialization described by desc.
	 * <p>
	 * The desc description helps to identify the shape and type of 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponents</a>  
	 * specialization that is needed. For instance,let's say there are two
	 * specializations ADComponent and BDComponent. A good value for desc would be
	 * "A". This method's implementation in a DiagramAttributeSet 
	 * specialization would return an instance of ADComponent.
	 * @param desc Description of the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * specialization object to be returned.
	 * @return A DComponent specialization instance.
	 */
	public abstract DComponent getDComponentContext(String desc);
	/**
	 * Returns the default
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * description if the input
	 * value is "Shape" or the default
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DRelation</a> 
	 * description otherwise.
	 * 
	 * @param desc General category description of "Shape" or "Line"
	 * @return a {@link #dComponentDescription} if the input
	 * value is "Shape" or {@link #dRelationDescription} otherwise. 
	 */
	public String getType(String desc){
		if(desc.equals("Shape")){
			return dComponentDescription;
		}
		return dRelationDescription;
	}
	/**
	 * Sets the default
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * description 
	 *  
	 * @param desc new {@link #dComponentDescription} 
	 */
	public void setComponentType(String desc){
		dComponentDescription = desc;
	}
	/**
	 * Sets the default
	 * <a href="{@docRoot}/com/acims/Diagrams/DRelation.html">DComponent</a> 
	 * description 
	 *  
	 * @param desc new {@link #dComponentDescription} 
	 */
	public void setRelationType(String desc){
		dRelationDescription = desc;
	}
	/**
	 * Returns The set 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Font.html">Font</a>.
	 * @return {@link #font}
	 */
	public Font getFont(){
		return font;
	}
	/**
	 * Sets the  
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Font.html">Font</a>.
	 * @param f new {@link #font}
	 */
	public void setFont(Font f){
		font = f;
	}
	/**
	 * Changes the location of a 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * to the location 
	 * <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * nPos.
	 * <p>
	 * This will be implemented by calling the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html#setDComponentPosition(java.awt.Point)">
	 * setDComponentPosition(Point)</a> method of a
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a>
	 * specialization.
	 * @param sh <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * to be placed at position nPos. 
	 * @param nPos <a href="http://java.sun.com/j2se/1.5.0/docs/api/java/awt/Point.html">Point</a> 
	 * position where the top left hand corner of the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * sh is to be placed
	 */
	public void relocateDComponent(DComponent sh, Point nPos){
		sh.setDCompPosition(nPos);
	}
	/**
	 * Sets the important attributes of a 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * specialization object. 
	 * <p>
	 * The method of 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * that must be called by this method is 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html#setDComponent(java.awt.Point, int, java.lang.String)">
	 * setDComponent(Point, int, String)</a>. 
	 * <p>
	 * This method is called by Diagram after a user program 
	 * request a change or additon of a DComponent before 
	 * the DComponent is drawn or redrawn.
	 * @param sh The 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * for which the attributes are to be set
	 * @param name The name of the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a> 
	 * instance.
	 * @param pos The position of the top left corner of the 
	 * <a href="{@docRoot}/com/acims/Diagrams/DComponent.html">DComponent</a>. 
	 * */
	public abstract void setDComponent(DComponent sh, String name, Point pos);
}
