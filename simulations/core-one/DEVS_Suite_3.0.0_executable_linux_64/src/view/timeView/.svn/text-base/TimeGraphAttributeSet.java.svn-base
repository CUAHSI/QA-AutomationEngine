/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */  

package view.timeView;

import java.awt.*;
import java.util.Vector;

import view.acims.Graphics.*;
import view.acims.diagrams.DComponent;
import view.acims.diagrams.DRelation;
import view.acims.diagrams.DiagramAttributeSet;
import view.acims.diagrams.Diagram.Relationship;


class TimeGraphAttributeSet extends DiagramAttributeSet {
	//Graph attributes Types
	public final static String frame = "3D Frame";
	public final static String xAxis = "X AXIS";
	public final static String eventArrow = "Event";
	public final static String hGraphLine = "hGraph";
	public final static String vGraphLine = "vGraph";
	public final static String dataPoint = "Point";
	
	private Vector unitLabels;
	private Point diagramSize = new Point(800,600);
	private boolean labelVisible = false;
	
	/**
	 * This class store attributes of the TimeView
	 */
	
	TimeGraphAttributeSet(){
		lineColor = Color.BLACK;                 //line color
		labelColor = Color.BLACK;                //label color
		fillColor = Color.white;
		dComponentShape = DBox3D.RECTANGLE3D;
		endCapWidth = 8;
		endCapHeight = 8;
	}
	
	/**
	 * Set each component's attributes
	 */
	public DRelation getDRelationContext(String desc) {
		DRelation rel = null;
	
		if(dRelationDescription.equals(xAxis)){ //Attributes for x-axis
			DXAxisRelation x = new DXAxisRelation(desc);
			x.setType(xAxis);
			x.setColors(labelColor,lineColor,fillColor);
			rel = (DRelation)x;
		}
		else if(dRelationDescription.equals(eventArrow)){ //Attributes for event arrow
			DecoratedLine event = new DecoratedLine(desc);
			event.setType(eventArrow);
			event.setArc(0);
			event.setColors(labelColor,lineColor,fillColor);
			event.setEndCap(DecoratedLine.FILLED_ARROW_CAP,endCapWidth,endCapHeight);
			rel = (DRelation)event;
		}
		else if(dRelationDescription.equals(hGraphLine)){ //Attributes for horiontal line
			DecoratedLine graph = new DecoratedLine(desc);
			graph.setType(hGraphLine);
			graph.setArc(0);
			graph.setColors(labelColor,lineColor,fillColor);
			graph.setEndCap(DecoratedLine.NO_CAP);
			graph.setReturnLineEnabled(false);
			rel = (DRelation)graph;
		}
		else if(dRelationDescription.equals(vGraphLine)){ //Attributes for vertical line
			DecoratedLine graph = new DecoratedLine(desc);
			graph.setType(vGraphLine);
			graph.setArc(0);
			graph.setColors(labelColor,lineColor,fillColor);
			graph.setEndCap(DecoratedLine.NO_CAP);
			graph.setReturnLineEnabled(false);
			rel = (DRelation)graph;
		}
		return rel;
	}
	
	/**
	 * Set unit labels
	 * @param in
	 */
	public void setUnitLabels(Vector in){
		unitLabels = in;
	}

	/**
	 * construct x-axis using labels
	 */
	public void setDRelation(Relationship c, Vector ln, Vector sh, String op) {
		DRelation rel = c.getRelationship();
		if(rel.getType().equals(xAxis)){
			DXAxisRelation xAxs = (DXAxisRelation)rel;
			xAxs.setUnitLabels(unitLabels);
		}
	}

	/**
	 * return component context
	 */
	public DComponent getDComponentContext(String desc) {
		DComponent comp = null;
		if(dComponentDescription.equals(frame)){
			DBox3D f = new DBox3D(fillColor);
			f.setType(frame);
			f.setDimensions(diagramSize);
			comp = (DComponent)f;
		}
		else if(dComponentDescription.equals(dataPoint)){
			DTransparentPoint p = new DTransparentPoint();
			p.setType(dataPoint);
			p.setLabelVisible(labelVisible);
			comp = (DComponent)p;
		}
		return comp;
	}
	
	public void setDataLabelVisible(boolean v){
		labelVisible = v;
	}

	/**
	 * set component's attributes
	 */
	public void setDComponent(DComponent sh, String name, Point pos) {
		sh.setShape(pos,0,name);
	}
	
	/*
	private DComponent getComponent(String name, Vector in){
		for(int i = 0; i < in.size();++i){
			if(((DComponent)in.get(i)).getLabel().equals(name)){
				return ((DComponent)in.get(i));
			}
		}
		return null;
	}*/

}
