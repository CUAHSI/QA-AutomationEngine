/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
package view;

import java.awt.*;
import javax.swing.*;
import java.util.*;

public class WorkspaceView extends JDesktopPane
{
    private WindowManager windowManager;
    public WorkspaceView()
    {
        super();
        windowManager = new WorkspaceView.WindowManager(this);
    }
    
    public void cascadeWindows()            {windowManager.cascadeWindows();}
    public void tileWindowsHorizontal()     {windowManager.tileWindowsHorizontal();}
    public void tileWindowsVertical()       {windowManager.tileWindowsVertical();}
    public void arrangeWindows()            {windowManager.arrangeWindows();}
            
            
    private class WindowManager
    {
        public static final short CASCADE         = 0;
        public static final short TILE_HORIZONTAL = 1;
        public static final short TILE_VERTICAL   = 2;
        
        private int iconifiedMargin;
        private int separationMargin;
        private double scalingFactor;
        private JDesktopPane desktopPanel;
        
        //Window Setup Information
        private ArrayList activeWindowList;
        private int desktopWidth;
        private int desktopHeight;
        
        public WindowManager(JDesktopPane desktopPanel)
        {
            this.desktopPanel = desktopPanel;
            //Initialize variables to defaults
            iconifiedMargin   = 40;
            separationMargin  = 25;
            scalingFactor     = .75;
        }
        
        public int getWindowIconifiedMargin()               {return iconifiedMargin;}
        public int getSeparationMargin()                    {return separationMargin;}
        public double getScalingFactor()                    {return scalingFactor;}
        public void setWindowIconifiedMargin(int p1)        {iconifiedMargin  = p1;}
        public void setWindowSeparationMargin(int p1)       {separationMargin = p1;}
        public void setScalingFactor(double p1)             {scalingFactor    = p1;}
        
        private void refreshWindowInfo()
        {
            JInternalFrame[] windows = desktopPanel.getAllFrames();
            activeWindowList = new ArrayList(windows.length);
            boolean iconifiedWindowPresent = false;
            for (int i = 0; i < windows.length; i++)
            {
                if (windows[i].isIcon())
                    iconifiedWindowPresent = true;
                else if (windows[i].isVisible())
                    activeWindowList.add(windows[i]);                
            }
            
           desktopWidth  = desktopPanel.getWidth();
           desktopHeight = desktopPanel.getHeight();
            if (iconifiedWindowPresent)
               desktopHeight -= iconifiedMargin;
        }
        
        public void cascadeWindows()
        {
            refreshWindowInfo();
            int nextWindowX  = 0;
            int nextWindowY  = 0;
            int newWidth     = 0;
            int newHeight    = 0;

            for (int i = activeWindowList.size()-1; i >=0; i--)
            {
                JInternalFrame next = (JInternalFrame) activeWindowList.get(i);
                newWidth  = (int)(desktopWidth*scalingFactor);
                newHeight = (int)(desktopHeight*scalingFactor);
                if ((nextWindowX + newWidth > desktopWidth) || 
                    (nextWindowY + newHeight > desktopHeight))
                    nextWindowX = nextWindowY = 0;
                next.setLocation(nextWindowX,nextWindowY);
                if (next.isResizable())
                    next.setSize(newWidth,newHeight);
                next.moveToFront();
                nextWindowX += separationMargin;
                nextWindowY += separationMargin;
            }
        }
        
        public void tileWindowsHorizontal()
        {
            refreshWindowInfo();
            int newWidth  = 0;
            int newHeight = 0;
            int nextLocY  = 0;
            
            for (int i = 0; i < activeWindowList.size(); i++)
            {
                JInternalFrame next = (JInternalFrame) activeWindowList.get(i);
                newWidth = desktopWidth;
                newHeight =(int)(desktopHeight/activeWindowList.size());
                next.setLocation(0,nextLocY);
                nextLocY += newHeight;
                if (next.isResizable())
                    next.setSize(newWidth,newHeight);   
            }
        }
        
        public void tileWindowsVertical()
        {
            refreshWindowInfo();
            int newWidth  = 0;
            int newHeight = 0;
            int nextLocX  = 0;
            
            for (int i = 0; i < activeWindowList.size(); i++)
            {
                JInternalFrame next = (JInternalFrame) activeWindowList.get(i);
                newWidth = (int)(desktopWidth/activeWindowList.size());
                newHeight = desktopHeight;
                next.setLocation(nextLocX,0);
                nextLocX += newWidth;
                if (next.isResizable())
                    next.setSize(newWidth,newHeight);
            }
        }   
        
        public void arrangeWindows()
        {
            refreshWindowInfo();
            int rows,cols,remainder,newWidth,newHeight,rCounter;
            int nextLocX = 0;
            int nextLocY = 0;
            
            rows = (int)Math.round(Math.sqrt((double)activeWindowList.size()));
            cols = activeWindowList.size() / rows;
            remainder = activeWindowList.size() % rows;
            
            newWidth  = (int) (desktopWidth/(double)cols);
            newHeight = (int) (desktopHeight/(double)rows);
            rCounter  = 1;
            
            for (int i = 0; i < activeWindowList.size(); i++)
            {
                JInternalFrame next = (JInternalFrame) activeWindowList.get(i);
                next.setLocation(nextLocX,nextLocY);
                if (rCounter > rows-remainder)
                    newWidth = (int)(desktopWidth/(double)(cols+1));
                
                if (next.isResizable())
                    next.setSize(newWidth,newHeight);
                if (nextLocX < desktopWidth-newWidth-10)
                    nextLocX += newWidth;
                else
                {
                    nextLocY += newHeight;
                    nextLocX = 0;
                    if (rCounter <= rows-remainder)
                        rCounter++;
                }
            }
        }
    }
}