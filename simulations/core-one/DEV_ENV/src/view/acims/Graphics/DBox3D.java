/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
package view.acims.Graphics;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.image.BufferedImage;

import view.acims.Math.*;
import view.acims.diagrams.DComponent;


public class DBox3D extends DComponent {

	public final static int RECTANGLE3D = 0;
	
	public DBox3D(){}
	
	public DBox3D(Color bg){
		backgroundColor = bg;
	}
	
	public void drawDComponent(Graphics2D g2D) {
		int squares = 5;
		g = g2D;
		
		g.setColor(backgroundColor);
		g.fillRect(0,0,xLength,yLength);
		
		for(int i = 0; i < squares; ++i){
			if((i%2) == 1){
				g.setColor(Color.GRAY);
				if(i == 1){
					g.setStroke(new BasicStroke(2.0f));
				}
				else{
					g.setStroke(new BasicStroke(1.1f));
				}
			}
			else if (i == 0 || (i == (squares-1))){
				g.setColor(Color.DARK_GRAY);
				if(i == 0){
					g.setStroke(new BasicStroke(3.0f));
				}
				else{
					g.setStroke(new BasicStroke(1.2f));
				}
			}
			else{
				g.setColor(Color.LIGHT_GRAY);
				g.setStroke(new BasicStroke(2.5f));
			}
			g.drawLine(start.x+i,
						start.y+i,
						start.x+xLength-i,
						start.y+i);
			g.drawLine(start.x+i,
					start.y+yLength-i,
					start.x+xLength-i,
					start.y+yLength-i);
			g.drawLine(start.x+i,
					start.y+i,
					start.x+i,
					start.y+yLength-i);
			g.drawLine(start.x+xLength-i+1,
					start.y+i,
					start.x+xLength-i+1,
					start.y+yLength-i);
		}
	}

	public Point getCenter() {
		Point temp = Math2D.scalarMultiply(0.5,new Point(xLength,yLength));
		return Math2D.addVectors(start,temp);
	}

	public Point getClosestPointOnDComp(Point p) {
		return Math2D.closestPointOnRectangle(p,start,xLength,yLength);
	}

	public Point getDimensions() {
		return new Point(xLength,yLength);
	}

	public String getLabel() {
		return label;
	}

	public String getType() {
		return type;
	}

	public Point getPosition() {
		return start;
	}

	public boolean isOnDComp(Point p) {
		return Math2D.isOnRectangle(p,start,xLength,yLength);
	}

	public void setColors(Color c){
		backgroundColor = c;
	}
	
	public void setDimensions(Point dim) {
		xLength = dim.x;
		yLength = dim.y;
	}

	public void setDCompPosition(Point nPos) {
		start = nPos;
	}
	
	public void setShape(Point pos, int shape, String text) {
		start = pos;
		dCompShape = RECTANGLE3D;
		label = text;
	}

	public void setType(String compType) {
		type = compType;
	}

}
