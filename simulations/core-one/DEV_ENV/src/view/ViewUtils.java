/** A collection of utility methods for primary use by
 * classes in the view package.
 *
 * @author  Ranjit Singh 
 */

package view;

import java.awt.event.ActionListener;
import java.awt.*;
import javax.swing.*;
import java.util.List;
import java.util.Hashtable;
import java.util.LinkedList;

public class ViewUtils 
{    
    
    /** Dimension of the main GUI window.*/    
    public static final Dimension FRAME_DIM = new Dimension(950,700); 
    
    /** Title of the main GUI window.*/
    public static final String FRAME_TITLE = "DEVS-Suite Ver 3.0.0"; 
    
    /**Image Paths*/
    public static final String SPLASH_SCREEN_ICON = "/graphics/DEVS-SuiteLogo.png";
    public static final String INITIAL_SC         = "/graphics/stateChart1.gif";
    public static final String SIMULATING_SC      = "/graphics/stateChart2.gif";
    public static final String PAUSE_SC           = "/graphics/stateChart3.gif";
    public static final String END_SC             = "/graphics/stateChart4.gif";
    public static final String NEW_MENU			  = "/graphics/New_menu.png";
    public static final String OPEN_MENU		  = "/graphics/Open_menu.png";
    public static final String SAVE_MENU		  = "/graphics/Save_menu.png";
    public static final String CLEAN_MENU		  = "/graphics/Clean_menu.png";
    public static final String SETTING_MENU       = "/graphics/Setting_menu.png";
    public static final String HELP_MENU          = "/graphics/Help_menu.png";
    public static final String EXPAND_MENU        = "/graphics/Expand_menu.png";
    public static final String COLLAPSE_MENU      = "/graphics/Collapse_menu.png";
    public static final String STEP				  = "/graphics/Step.png";
    public static final String PAUSE			  = "/graphics/Pause.png";
    public static final String STEPN              = "/graphics/Stepn.png";
    public static final String RUN 				  = "/graphics/Run.png";
    public static final String RSET  			  = "/graphics/Rset.png";
    public static final String LOGO  			  = "/graphics/MS_Logo.gif";
    /** Uninstantiable Utility Class. (for static calls only)
     */    
    private ViewUtils() {}
    
    /** Returns an ImageIcon whose image is loaded from the given pathname.
     * If the pathname is invalid, this method will return null.
     * @param path Pathname to the icon to load.
     * @return ImageIcon whose image is loaded from the given pathname.  Returns null
     * if the path name is invalid.
     */    
    public static Image loadFullImage (String path) 
    {
        Image image = null;
        try 
        {
            MediaTracker tracker = new MediaTracker(new JLabel());
            image = Toolkit.getDefaultToolkit().getImage(ViewUtils.class.getResource(path));
            tracker.addImage(image,1);
            tracker.waitForAll();
        }
        catch (Exception e)
        {
            System.err.println(e);
            System.err.println(e);
        }
        return image;	
    }

    
    
    /** Returns a JMenu that contains the given items.  Sets each
     * item to listen to the given ActionListener.
     *
     * @param parent The JMenu to add items to, or a String to
     * call the new JMenu.
     * @param items Array of Strings, JMenuItems or null's.  JMenuItems
     * are created from the Strings then added.  A null
     * will translate into a menu divider.  Items will
     * be added in linear order from index 0.
     * @param target An ActionListener to add to each of the JMenuItems.
     * Note this value may be null.
     *
     * @return JMenu that contains the given items.  Sets each
     * item to listen to the given ActionListener.  Return
     * null if an error occurs.
     */    
    public static JMenu makeMenu(Object parent, Object[] items, Object target)
	{  
		JMenu menu = null;
		
		if (parent instanceof JMenu)
			menu = (JMenu)parent;
        
		else if (parent instanceof String)
			menu = new JMenu((String)parent);
		
		if (menu != null) 
			for (int i = 0; i < items.length; i++) 
			{  
				if (items[i] == null)
					menu.addSeparator();
				else
					menu.add(makeMenuItem(items[i], target));
			}
      return menu;
    }

    /** Returns a JMenuItem that is connected to the the given ActionListener.
     *
     * @param item A JMenuItem or String.
     * @param target An ActionListener (or null).
     * @return JMenuItem that is connected to the the given ActionListener
     * (or nothing if the ActionListener is null).  Returns null if an
     * error occurs.
     */    
	public static JMenuItem makeMenuItem (Object item, Object target)
	{  	
		JMenuItem menuItem = null;
		if (item instanceof String)
			menuItem = new JMenuItem((String)item);
		else if (item instanceof JMenuItem)
			menuItem = (JMenuItem)item;
		
		if (menuItem != null) 
			if (target instanceof ActionListener)
				menuItem.addActionListener((ActionListener)target);
		return menuItem;
   }

   //Converts the given list of 'Strings' to an encoded integer (via seed)
   //and places the encoded key with the original value into the legend.
   public static List integerEncode(List list, Hashtable legend, int seed)
   {
       List encodedList = new LinkedList();
       for (int i = 0; i < list.size(); i++)
       {
           Object nextVal = list.get(i);
           if (nextVal == null)
               encodedList.add(null);
           else
           {
               String next = nextVal.toString();
               Object value = legend.get(next);
               if (value == null)
               {
                   value = new Integer(seed++);
                   legend.put(next,value);
               }
               encodedList.add(value);
           }
       }
       return encodedList;
   }
}
