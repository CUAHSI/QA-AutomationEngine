/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
package view.acims.Graphics;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.BasicStroke;
import java.awt.Point;
import java.util.*;

import view.acims.Math.*;
import view.acims.diagrams.*;


public class DXAxisRelation extends DRelation {
	public final static int xAxis = 0;
	
	protected DecoratedLine axis;
	protected DTextLabel nameLabelH;
	protected DTextLabel nameLabelV;
	private Vector unitNames;
	private int numUnits = 0;
	private int unitLength = 0;
	private int shift = 0;
	
	public DXAxisRelation(String name){
		label = name;
		axis = new DecoratedLine(" ");
		axis.setArc(0);
		axis.setEndCap(DecoratedLine.FILLED_ARROW_CAP,8,8);
		nameLabelH = new DTextLabel();
		nameLabelV = new DTextLabel();
	}
	
	public void drawDRelation(Point begin, Point end, Graphics2D g2D, String XLabel) {
		g2D.setStroke(new BasicStroke(2.0f));
		axis.drawDRelation(begin,end,g2D, XLabel);
		nameLabelH.setColors(textColor,backgroundColor,backgroundColor);
		nameLabelV.setColors(textColor,backgroundColor,backgroundColor);
		Point len = Math2D.subtractVectors(begin,end);
		Point temp = Math2D.addVectors(len,new Point(0,15));
		temp = Math2D.addVectors(begin,temp);
		temp = Math2D.subtractVectors(new Point(temp.x/2,0),temp);
		nameLabelH.setShape(temp, XLabel);
		nameLabelH.drawDComponent(g2D);
		nameLabelV.setTextAngle(-90);
		nameLabelV.setShape(Math2D.addVectors(begin,new Point(-23,-20)),label);
		nameLabelV.drawDComponent(g2D);
		
		int stX = begin.x;
		int stY = begin.y;
		int next = stX+shift;
		g2D.setColor(lineColor);
		for(int i =0; i <numUnits; ++i){
			if(next >= begin.x){
				String nextLabel = (String)unitNames.remove(0);
				g2D.drawLine(next,stY-3,next,stY+3);
				g2D.drawString(nextLabel,next-5,stY+15);
			}
			else{
				--i;
			}
			next += unitLength;
		}
	}

	public String getLabel() {
		return label;
	}

	public String getType() {
		return type;
	}

	public boolean isOnDRelation(Point p) {
		return axis.isOnDRelation(p);
	}

	public void setLabel(String text) {
		label = text;
	}

	public void setType(String relType) {
		type = relType;
	}
	
	public void setUnitLabels(Vector lb){
		unitNames = new Vector(10,1);
		for(int i = 0; i < lb.size(); ++i){
			unitNames.add(lb.get(i));
		}
		Integer offst = (Integer)unitNames.remove(0);
		shift = offst.intValue();
		offst =(Integer)unitNames.remove(0);
		unitLength = offst.intValue();
		numUnits = unitNames.size();
	}

	public void setColors(Color lblColor, Color lnColor, Color bgColor) {
		axis.setColors(lblColor,lnColor,bgColor);
		lineColor = lnColor;
		textColor = lblColor;
		backgroundColor = bgColor;
	}
}
