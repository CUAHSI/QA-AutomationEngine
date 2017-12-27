/**
 * This class creates line objects on a Graphics2D object. It provides 
 * both arc and straight lines. There are several end cap types to
 * choose from. Optional textual labels are located above and parallel 
 * to DecoratedLines when displayed.
 * @author Robert Flasher
 * @version 1.0
 */

package view.acims.Graphics;


import java.awt.*;

import view.acims.Math.*;
import view.acims.diagrams.DRelation;


public class DecoratedLine extends DRelation{
	
	/**
	 * Static value used to set end cap of line to an arrow.
	 * <p>
	 * example: line.setEndCap(DecoratedLine.ARROW_CAP);
	 */
	public static final int ARROW_CAP = 3;
	
	/**
	 * Static value used to set end cap of line to a circle.
	 * <p>
	 * example: line.setEndCap(DecoratedLine.CIRCLE_CAP);
	 */
	public static final int CIRCLE_CAP = 9;
	
	/**
	 * Static value used to exclude an end cap from the line. This
	 * is the default.
	 */
	public static final int NO_CAP = 0;
	
	/**
	 * Static value used to set end cap of line to a diamond.
	 * <p>
	 * example: line.setEndCap(DecoratedLine.DIAMOND_CAP);
	 */
	public static final int DIAMOND_CAP = 5;
	
	/**
	 * Static value used to set end cap of line to a filled arrow.
	 * <p>
	 * example: line.setEndCap(DecoratedLine.FILLED_ARROW_CAP);
	 */
	public static final int FILLED_ARROW_CAP = 4;
	
	/**
	 * Static value used to set end cap of line to a filled circle.
	 * <p>
	 * example: line.setEndCap(DecoratedLine.FILLED_CIRCLE_CAP);
	 */
	public static final int FILLED_CIRCLE_CAP = 10;
	
	/**
	 * Static value used to set end cap of line to a filled diamond.
	 * <p>
	 * example: line.setEndCap(DecoratedLine.FILLED_DIAMOND_CAP);
	 */
	public static final int FILLED_DIAMOND_CAP = 6;
	
	/**
	 * Static value used to set end cap of line to a filled oval.
	 * <p>
	 * example: line.setEndCap(DecoratedLine.FILLED_OVAL_CAP);
	 */
	public static final int FILLED_OVAL_CAP = 8;
	
	/**
	 * Static value used to set end cap of line to a filled rectangle.
	 * <p>
	 * example: line.setEndCap(DecoratedLine.FILLED_RECT_CAP);
	 */
	public static final int FILLED_RECT_CAP = 2;
	
	/**
	 * Static value used to set end cap of line to an oval.
	 * <p>
	 * example: line.setEndCap(DecoratedLine.OVAL_CAP);
	 */
	public static final int OVAL_CAP = 7;
	
	/**
	 * Static value used to set end cap of line to a rectangle.
	 * <p>
	 * example: line.setEndCap(DecoratedLine.RECT_CAP);
	 */
	public static final int RECT_CAP = 1;
	
	/**
	 * Instantiates and returns a DecoratedLine object.
	 * <p>
	 * DecoratedLine cannot be directly instantiated by classes outside 
	 * the com.acims.Graphics package or classes without an inheritance
	 * relationship with DecoratedLine. Therefore, this static method 
	 * returns a new instance of DecoratedLine. 
	 * <p>
	 * An example invokation of this method by a class to receive an
	 * instance of a DecoratedLine object:
	 * <p>
	 * DecoratedLine line = DecoratedLine.getDecoratedLineContext(g);
	 * 
	 * @param g2D The Graphics2D object where the line will be drawn.
	 * @return A new DecoratedLine object.
	 */
	//public static DecoratedLine getDecoratedLineContext(){
		//return new DecoratedLine();
	//}
	
	private boolean arc = false;
	private int arcHeight = 0;
	private Color backgroundColor = Color.WHITE;
	private int capAngle = 0;
	private Point end;
	private int endCap = NO_CAP;
	private int endCapHeight = 20;
	private int endCapWidth = 25;
	private Graphics2D g;
	private Color lineColor = Color.BLACK;
	private double lineLength = 0;
	private int lineOffset = 0;
	private double retLineAngle = -Math.PI/4;
	private int retLineL = 70;
	private int retLineW = 15;
	private boolean returnLine = false;
	private boolean returnLineEnabled = true;
	private Point start;
	private String label = "";
	private Font font = new Font("Arial", Font.BOLD, 12);
	private double textAngle = 0;
	private Color textColor = Color.BLACK;
	private int textOffsetX = 0;
	private int textOffsetY = -3;
	private int lengthLineCovered = 0;
	
	
	public DecoratedLine(String lbl){
		label = lbl;
	}
	
	private void drawEndCap(){
		switch(endCap){
		case FILLED_ARROW_CAP:
			g.fillArc((int)end.getX()-(endCapWidth/2),
					  (int)end.getY()-(endCapHeight/2), endCapWidth,
					  endCapHeight, capAngle, 60);
			break;
		case ARROW_CAP:
			g.translate(start.getX(),start.getY());
			g.rotate(textAngle);
			g.translate(lineLength-endCapWidth,0);
			if(arc){
				g.rotate(Math.PI/10);
				g.translate(0,-endCapHeight/2);
			}
			g.setColor(backgroundColor);
			g.drawLine(0,0,endCapWidth,0);
			g.setColor(lineColor);
			g.drawLine(0,-(endCapHeight/2),0,(endCapHeight/2));
			g.drawLine(0,-(endCapHeight/2),endCapWidth,0);
			g.drawLine(0,(endCapHeight/2),endCapWidth,0);
			if(arc){
				g.translate(0,endCapHeight/2);
				g.rotate(-Math.PI/10);
			}
			g.translate(-(lineLength-endCapWidth),0);
			g.rotate(-textAngle);
			g.translate(-start.getX(),-start.getY());
			break;
		case RECT_CAP:
		case FILLED_RECT_CAP:
		case DIAMOND_CAP:
		case FILLED_DIAMOND_CAP:
			g.translate(start.getX(),start.getY());
			g.rotate(textAngle);
			g.translate(lineLength-endCapWidth,-(endCapHeight/2));
			if(arc){
				g.rotate(Math.PI/10);
				g.translate(0,-endCapHeight/2);
			}
			if(endCap == DIAMOND_CAP ||
			   endCap == FILLED_DIAMOND_CAP){
				g.translate(endCapWidth/2,0);
				g.rotate(Math.PI/4);
			}
			if(endCap == RECT_CAP ||
			   endCap == DIAMOND_CAP){
				g.drawRect(0,0, endCapWidth, endCapHeight);;
				g.setColor(backgroundColor);
			}
			g.fillRect(0,0, endCapWidth, endCapHeight);
			if(endCap == DIAMOND_CAP ||
			   endCap == FILLED_DIAMOND_CAP){
				g.rotate(-Math.PI/4);
				g.translate(-endCapWidth/2,0);
			}
			if(arc){
				g.translate(0,endCapHeight/2);
				g.rotate(-Math.PI/10);
			}
			g.translate(-(lineLength-endCapWidth),(endCapHeight/2));
			g.rotate(-textAngle);
			g.translate(-start.getX(),-start.getY());
			g.setColor(lineColor);
			break;
		case OVAL_CAP:
		case FILLED_OVAL_CAP:
		case CIRCLE_CAP:
		case FILLED_CIRCLE_CAP:
			g.translate(start.getX(),start.getY());
			g.rotate(textAngle);
			g.translate(lineLength-endCapWidth,-(endCapHeight/2));
			if(arc){
				g.rotate(Math.PI/10);
				g.translate(0,-endCapHeight/2);
			}
			if(endCap == OVAL_CAP || endCap == CIRCLE_CAP){
				g.drawOval(0,0, endCapWidth, endCapHeight);
				g.setColor(backgroundColor);
			}
			g.fillOval(0,0, endCapWidth, endCapHeight);
			if(arc){
				g.translate(0,endCapHeight/2);
				g.rotate(-Math.PI/10);
			}
			g.translate(-(lineLength-endCapWidth),(endCapHeight/2));
			g.rotate(-textAngle);
			g.translate(-start.getX(),-start.getY());
			g.setColor(lineColor);
			break;
		}
	}
	
	private void drawLine(){
		g.drawArc(0,lineOffset,(int)lineLength,arcHeight,0,180);
	}
	
	public void drawDRelation(Point begin, Point end, Graphics2D g2D){
		drawLine((int)begin.getX(), (int)begin.getY(), (int)end.getX(), (int)end.getY(), g2D);
	}
	
	public void drawDRelation(Point begin, Point end, Graphics2D g2D, String XLabel){
		drawLine((int)begin.getX(), (int)begin.getY(), (int)end.getX(), (int)end.getY(), g2D);
	}
	
	private void drawLine(int beginX, int beginY, int endX, int endY, Graphics2D g2D){
		g = g2D;
		start = new Point(beginX,beginY);
		end = new Point(endX,endY);
		lineLength = Math2D.distancePointToPoint(start,end);
		textAngle = Math2D.angleOfLine(start,end);
		capAngle = (int)(Math.toDegrees(textAngle));
		textOffsetX = getTextOffset();
		
		if(lineLength == 0){
			textOffsetX = 0;
			if(returnLineEnabled){
				returnLine = true;
				drawReturnLine();
			}
			return;
		}
		
		capAngle = (180-capAngle-30)-arcHeight;
		lineOffset = -(int)(arcHeight/2);
		if(textOffsetY > lineOffset){
			textOffsetY = lineOffset;
		}
		
		g.setColor(lineColor);
		g.translate(start.getX(),start.getY());
		g.rotate(textAngle);
		drawLine();
		g.setColor(textColor);
		drawString();
		g.rotate(-textAngle);
		g.translate(-start.getX(), -start.getY());
		g.setColor(lineColor);
		drawEndCap();
	}
	
	private void drawReturnLine(){
		end.setLocation(start.getX()+(retLineL/2),start.getY()-retLineW);
		g.translate(start.getX(),start.getY());
		g.rotate(retLineAngle);
		g.drawOval(0,0,retLineL,retLineW);
		g.translate(60,0);
		g.rotate(-retLineAngle);
		drawString();
		g.rotate(retLineAngle);
		g.translate(-60,0);
		g.rotate(-retLineAngle);
		g.translate(-start.getX(),-start.getY());
		drawEndCap();
	}
	private void drawString(){
		if(label != ""){
			g.setFont(font);
			g.drawString(label, textOffsetX, textOffsetY);
		}
	}
	
	public boolean getArc(){return arc;}
	
	public int getArcHeight(){return arcHeight;}
	
	public int getEndCapHieght(){return endCapHeight;}
	
	public int getEndCapShape(){return endCap;}
	
	public int getEndCapWidth(){return endCapWidth;}
	
	public String getLabel(){return label;}
	
	public String getType(){return super.type;}
	
	private int getTextOffset(){
		int charSize = 6;
		int offset = (int)((((lineLength-lengthLineCovered)-(label.length()*charSize))/2)+lengthLineCovered);
		if(offset < 0){
			offset = 0;
		}
		
		return offset;
	}
	
	public boolean isOnDRelation(Point p){
		return isOnLine((int)p.getX(),(int)p.getY());
	}
	
	private boolean isOnLine(int x, int y){
		boolean result = false;
		int curX = x;
		int curY = y;
		double distance = 0;
		Point p = new Point(curX,curY);
		
		if(returnLine){
			distance = Math2D.distancePointToArc(p,start,retLineL,
					   retLineW,retLineAngle,2*Math.PI);
		}
		else if(arc){
			Point temp = new Point((int)start.getX(),(int)(start.getY()+(arcHeight/2)));
			temp = Math2D.rotateVector(temp,start,textAngle);
			temp = Math2D.transposePoint(temp,arcHeight/2,-Math.PI/2);
			distance = Math2D.distancePointToArc(p,temp,(int)lineLength,arcHeight,textAngle,-Math.PI);
		}
		else{
			distance = Math2D.distancePointToVector(p,start,end);
		}
		
		if(distance <= 3){
			result = true;
		}
		
		return result;
	}
	
	public void setArc(int arcH){
		arcHeight = arcH;
		arc = (arcHeight != 0);
	}
	
	public void setColors(Color lblColor, Color lnColor, Color bgColor){
		textColor = lblColor;
		lineColor = lnColor;
		backgroundColor = bgColor;
	}
	
	public void setEndCap(int shape){
		setEndCap(shape, endCapWidth, endCapHeight);
	}
	
	public void setEndCap(int shape, int width, int height){
		endCap = shape;
		endCapHeight = height;
		endCapWidth = width;
		
		switch(endCap){
		case FILLED_ARROW_CAP:
			endCapHeight=endCapHeight*2;
			endCapWidth=endCapWidth*2;
			break;
		case DIAMOND_CAP:
		case FILLED_DIAMOND_CAP:
		case CIRCLE_CAP:
		case FILLED_CIRCLE_CAP:
			endCapHeight = endCapWidth;
			break;
		}
	}
	
	public void setFont(Font f){
		font = f;
	}
	
	public void setLabel(String text){
		label = text;
	}
	
	public void setReturnLineEnabled(boolean enable){
		returnLineEnabled = enable;
	}
	
	public void setType(String relType){
		super.type = relType;
	}
	
	public void setLineCovered(int length){
		lengthLineCovered = length;
	}
}
