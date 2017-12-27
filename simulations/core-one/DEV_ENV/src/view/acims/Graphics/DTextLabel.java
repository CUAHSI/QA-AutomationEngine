/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
package view.acims.Graphics;

import java.awt.*;

import view.acims.Math.*;


public class DTextLabel extends DecoratedShape {
	private double textAngle = 0;
	private Point begin = new Point(0,0);
	private Color textColor = Color.BLACK;
	private Color lineColor = Color.YELLOW;
	private Color backgroundColor = Color.YELLOW;
	
	public DTextLabel(){
		super.dCompShape = DecoratedShape.FILLED_RECTANGLE;
		super.textColor = this.textColor;
		super.lineColor = this.lineColor;
		super.backgroundColor = this.backgroundColor;
	}
	
	public void drawDComponent(Graphics2D g2D){
		g2D.translate(begin.x,begin.y);
		g2D.rotate(textAngle);
		super.setDCompPosition(new Point(0,0));
		super.drawDComponent(g2D);
		super.setDCompPosition(begin);
		g2D.rotate(-textAngle);
		g2D.translate(-begin.x,-begin.y);
	}
	
	public Point getCenter(){
		return Math2D.rotatePoint(super.center,textAngle);
	}
	
	public Point getClosestPointOnDComp(Point p){
		Point temp = Math2D.rotateVector(super.getPosition(),p,-textAngle);
		temp = Math2D.closestPointOnRectangle(temp,super.getPosition(),
				super.getDimensions().x,super.getDimensions().y);
		return Math2D.rotateVector(super.getPosition(),temp,textAngle);
	}
	
	public String getType(){return type;}
	
	public double getTextAngle(){
		return Math.toDegrees(textAngle);
	}
	
	public boolean isOnDComp(Point p){
		Point temp = Math2D.rotateVector(super.start,p,-textAngle);
		return Math2D.isOnRectangle(temp,super.start,super.xLength,super.yLength);
	}
	
	public void setDCompPosition(Point pos){
		super.start = pos;
		begin = super.start;
		super.setLabelLen();
		setCharacteristics();
	}
	
	private void setCharacteristics(){
		super.center = new Point((int)(super.xLength/2),(int)(super.yLength/2));
		super.labelPos = Math2D.addVectors(super.start,new Point(super.labelOffset,(int)(super.yLength/1.75)));
	}
	
	public void setShape(Point pos, String text){
		setDCompPosition(pos);
		super.label = text;
		super.setLabelLen();
		setCharacteristics();
	}
	
	public void setTextAngle(int angle){
		textAngle = Math.toRadians(angle);
	}
	
}
