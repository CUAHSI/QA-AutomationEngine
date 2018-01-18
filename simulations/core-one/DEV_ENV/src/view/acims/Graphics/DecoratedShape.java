/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
package view.acims.Graphics;

import java.awt.*;

import view.acims.Math.*;
import view.acims.diagrams.DComponent;


public class DecoratedShape extends DComponent{
	
	public static final int CIRCLE = 8;
	public static final int FILLED_CIRCLE = 9;
	public static final int FILLED_INNER_CIRCLE = 11;
	public static final int FILLED_INNER_OVAL = 7;
	public static final int FILLED_OVAL = 5;
	public static final int FILLED_RECTANGLE = 1;
	public static final int FILLED_ROUNDED_RECTANGLE = 3;
	public static final int FILLED_ROUNDED_SQUARE = 15;
	public static final int FILLED_SQUARE = 13;
	public static final int INNER_CIRCLE = 10;
	public static final int INNER_OVAL = 6;
	public static final int OVAL = 4;
	public static final int RECTANGLE = 0;
	public static final int ROUNDED_RECTANGLE = 2;
	public static final int ROUNDED_SQUARE = 14;
	public static final int SQUARE = 12;
	
	protected Graphics2D g;
	protected int decShape = ROUNDED_RECTANGLE;
	protected Point start = new Point(0,0);
	protected Point center = start;
	protected int xLength = 0;
	protected int yLength = 0;
	protected String label = "";
	protected Point labelPos;
	protected int labelOffset = 5;
	private int strLen = 0;
	protected Color backgroundColor = Color.WHITE;
	protected Color lineColor = Color.BLACK;
	protected Color textColor = lineColor;
	private int fontWidth = 7;
	private int innrShpOffst = 4;
	private Font  font = new Font("Arial", Font.BOLD, 12);
	private boolean fixedDimensions = false;
	
	public DecoratedShape() {
	}
	
	public void drawDComponent(Graphics2D g2D){
		g = g2D;
		setColorScheme();
		switch(decShape){
		case RECTANGLE:
		case FILLED_RECTANGLE:
		case SQUARE:
		case FILLED_SQUARE:
			g.setColor(backgroundColor);
			g.fillRect((int)start.getX(),(int)start.getY(),xLength,yLength);
			g.setColor(lineColor);
			g.drawRect((int)start.getX(),(int)start.getY(),xLength,yLength);
			break;
		case ROUNDED_RECTANGLE:
		case FILLED_ROUNDED_RECTANGLE:
		case ROUNDED_SQUARE:
		case FILLED_ROUNDED_SQUARE:
			g.setColor(backgroundColor);
			g.fillRoundRect((int)start.getX(),(int)start.getY(),xLength,yLength,5,5);
			g.setColor(lineColor);
			g.drawRoundRect((int)start.getX(),(int)start.getY(),xLength,yLength,5,5);
			break;
		case OVAL:
		case FILLED_OVAL:
		case CIRCLE:
		case FILLED_CIRCLE:
			g.setColor(backgroundColor);
			g.fillOval((int)start.getX(),(int)start.getY(),xLength,yLength);
			g.setColor(lineColor);
			g.drawOval((int)start.getX(),(int)start.getY(),xLength,yLength);
			break;
		case INNER_CIRCLE:
		case FILLED_INNER_CIRCLE:
		case INNER_OVAL:
		case FILLED_INNER_OVAL:
			g.setColor(Color.BLACK);
			g.drawOval((int)start.getX(),(int)start.getY(),xLength,yLength);
			g.setColor(backgroundColor);
			g.fillOval((int)start.getX()+innrShpOffst,(int)start.getY()+innrShpOffst,
					xLength-(innrShpOffst*2),yLength-(innrShpOffst*2));
			g.setColor(lineColor);
			g.drawOval((int)start.getX()+innrShpOffst,(int)start.getY()+innrShpOffst,
					xLength-(innrShpOffst*2),yLength-(innrShpOffst*2));
		}
		drawLabel();
		setColorScheme();
	}
	
	public Point getCenter(){
		return center;
	}
	
	public Point getClosestPointOnDComp(Point p){
		switch(decShape){
		case RECTANGLE:
		case FILLED_RECTANGLE:
		case SQUARE:
		case FILLED_SQUARE:
		case ROUNDED_RECTANGLE:
		case FILLED_ROUNDED_RECTANGLE:
		case ROUNDED_SQUARE:
		case FILLED_ROUNDED_SQUARE:
			return Math2D.closestPointOnRectangle(p,start,xLength,yLength);
		default:
			return Math2D.closestPointOnArc(p,start,xLength,yLength,0,2*Math.PI);
		}
	}
	
	public Point getDimensions(){
		return new Point(xLength,yLength);
	}
	
	public String getLabel(){
		return label;
	}
	
	public int getShape(){
		return decShape;
	}
	
	public void setFont(Font f){
		font = f;
	}
	
	public Point getPosition(){
		return start;
	}
	
	public String getType(){return super.type;}
	
	public boolean isOnDComp(Point p){
		return isOnShape((int)p.getX(),(int)p.getY());
	}
	
	private boolean isOnShape(int x, int y){
		Point inPoint = new Point(x,y);
		switch(decShape){
		case RECTANGLE:
		case FILLED_RECTANGLE:
		case SQUARE:
		case FILLED_SQUARE:
		case ROUNDED_RECTANGLE:
		case FILLED_ROUNDED_RECTANGLE:
		case ROUNDED_SQUARE:
		case FILLED_ROUNDED_SQUARE:
			return Math2D.isOnRectangle(inPoint,start,xLength,yLength);
		case OVAL:
		case FILLED_OVAL:
		case CIRCLE:
		case FILLED_CIRCLE:
		case INNER_CIRCLE:
		case FILLED_INNER_CIRCLE:
		case INNER_OVAL:
		case FILLED_INNER_OVAL:
			return Math2D.isOnEllipse(inPoint,start,xLength,yLength,0);
		}
		return false;
	}
	
	public void setDCompPosition(Point pos){
		start = pos;
		setLabelLen();
		setCharacteristics();
	}
	
	public void setShapePosition(int x, int y){
		start = new Point(x,y);
		setLabelLen();
		setCharacteristics();
	}
	
	public void setShape(Point pos, String text){
		start = pos;
		label = text;
		setLabelLen();
		setCharacteristics();
	}
	
	public void setShape(int x, int y, String text){
		start = new Point(x,y);
		label = text;
		setLabelLen();
		setCharacteristics();
	}
	
	public void setShape(Point pos, int shape, String text){
		start = pos;
		decShape = shape;
		label = text;
		setLabelLen();
		setCharacteristics();
	}
	
	public void setShape(int x, int y, int shape, String text){
		start = new Point(x,y);
		decShape = shape;
		label = text;
		setLabelLen();
		setCharacteristics();
	}
	
	public void setColors(Color lblColor, Color lnColor, Color bgColor){
		textColor = lblColor;
		lineColor = lnColor;
		backgroundColor = bgColor;
	}
	
	public void setDimensions(Point dim){
		fixedDimensions = true;
		setDimensions((int)dim.getX(),(int)dim.getY());
	}
	
	public void setDimensions(int length, int width){
		if(length > 0){
			strLen = length-10;
			if(decShape < CIRCLE){
				yLength = width;
			}
		}
		setCharacteristics();
	}
	
	public void setType(String compType){
		super.type = compType;
	}
	
	private void drawLabel(){
		if(label != "")
		{
			g.setFont(font);
			g.setColor(textColor);
			g.drawString(label,(int)labelPos.getX(),(int)labelPos.getY());
		}
	}
	
	private void setCharacteristics(){
		if(yLength == 0){
			yLength = 30;
		}
		xLength = strLen+10;
		switch(decShape){
		case INNER_CIRCLE:
		case FILLED_INNER_CIRCLE:
		case INNER_OVAL:
		case FILLED_INNER_OVAL:
			xLength += innrShpOffst;
			if(decShape >= CIRCLE){
				yLength = xLength;
			}
			else{
				yLength += innrShpOffst;
			}
			labelOffset += (int)(innrShpOffst/2);
			break;
		case CIRCLE:
		case FILLED_CIRCLE:
		case SQUARE:
		case FILLED_SQUARE:
		case ROUNDED_SQUARE:
		case FILLED_ROUNDED_SQUARE:
			yLength = xLength;
			break;
		}
		
		center = new Point((int)(xLength/2),(int)(yLength/2));
		labelPos = Math2D.addVectors(start,new Point(labelOffset,(int)(yLength/1.75)));
	}
	
	protected void setLabelLen(){
		int charSize = fontWidth;
		if(label == ""){
			strLen = 20;
		}
		else if(!fixedDimensions){
			strLen = label.length()*charSize;
		}
	}
	
	private void setColorScheme(){
		switch(decShape){
		case FILLED_RECTANGLE:
		case FILLED_ROUNDED_RECTANGLE:
		case FILLED_OVAL:
		case FILLED_INNER_OVAL:
		case FILLED_CIRCLE:
		case FILLED_INNER_CIRCLE:
		case FILLED_SQUARE:
		case FILLED_ROUNDED_SQUARE:
			if(textColor == lineColor){
				textColor = backgroundColor;
			}
			Color temp = lineColor;
			lineColor = backgroundColor;
			backgroundColor = temp;
			break;
		}
	}
}
