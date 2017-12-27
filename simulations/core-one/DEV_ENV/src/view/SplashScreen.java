/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
package view;

import javax.swing.*;
import java.awt.*;
import java.util.Calendar;

public class SplashScreen
{
    private static final int SLEEP_INTERVAL = 100;
    private JPanel imageHolder;
    private JWindow window;
    private long startTime;
    private long minSplashTime;

    public SplashScreen() 
    {
        imageHolder = new JPanel(new BorderLayout());
        imageHolder.setBorder(BorderFactory.createCompoundBorder(
		              BorderFactory.createEtchedBorder(),BorderFactory.createEtchedBorder()));
        window = new JWindow();
        window.getContentPane().add(imageHolder);
        minSplashTime = 3500;
    }

    /*Sets minimum splash time in seconds, time must be >= 1*/
    public void setMinimumSplashTime(int time)
    {
        minSplashTime = 1000 * ((int)Math.max(time,1));
    }
    
    public void showAsDialog(Component owner, String title)
    {
        window.getContentPane().removeAll();
        JOptionPane.showMessageDialog(owner,imageHolder,title,JOptionPane.PLAIN_MESSAGE);
        window.getContentPane().add(imageHolder);
    }
    
    public void startSplashScreen()
    {
        window.setVisible(true);
        window.toFront();
        startTime = Calendar.getInstance().getTime().getTime();
    }
    
    public void endSplashScreen (JFrame application)
    {
        long endTime = Calendar.getInstance().getTime().getTime();
	
        while ((endTime - startTime) < minSplashTime)
	{
            endTime += SLEEP_INTERVAL;
            try 
            {
                Thread.sleep(SLEEP_INTERVAL);
            }
            catch (Exception e) 
            {
                System.err.println("Error in Splash Screen: " + e);
            }
	}
        
        application.setVisible(true);
        application.toFront();
        window.setVisible(false);
    }

    public void setSplashImage(Image image)
    {	
        Dimension frameDim = new Dimension(image.getWidth(null),image.getHeight(null));
        window.setSize(frameDim);
        // Centers the Frame
        Dimension screenDim = Toolkit.getDefaultToolkit().getScreenSize(); 
        window.setLocation(new Point((screenDim.width - frameDim.width) / 2,
                              (screenDim.height - frameDim.height) / 2));
        imageHolder.removeAll();
        imageHolder.add(new JLabel(new ImageIcon(image)));
        window.repaint();        	
    }
}
