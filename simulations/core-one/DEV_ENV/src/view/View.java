/**
  * Facade connection: View provides the VIEW functionalities
 * Integrated the Timeview and Simview into the original tracking environment
 * 
 * @modified Sungung Kim
 * @date 5/12/2008
 */

package view;


//Facade Connections
import facade.modeling.FAtomicModel;
import facade.modeling.FCoupledModel;
import facade.modeling.FModel;
import facade.simulation.*;

//Standard API Imports
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.KeyEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.*;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.TreeSet;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import javax.swing.*;
import javax.swing.event.TreeSelectionEvent;
import javax.swing.event.TreeSelectionListener;
import javax.swing.table.DefaultTableModel;
import javax.swing.text.DefaultEditorKit;
import javax.swing.text.Document;
import javax.swing.text.Keymap;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.tree.TreeSelectionModel;







import model.modeling.*;
import controller.ControllerInterface;
import util.WindowUtil;
import view.jwizard.PageFactory;
import view.jwizard.WizardContainer;
import view.jwizard.WizardListener;
import view.jwizard.WizardPage;
import view.jwizard.WizardSettings;
import view.jwizard.pagetemplates.TitledPageTemplate;
import view.simView.*;
import view.timeView.Graph;
import view.timeView.GraphFactory;

public class View extends JFrame implements ViewInterface
{
    public static JFrame PARENT_FRAME;
    private JToolBar DEVSToolBar;
    
    private int consoleTabIndex = 0;
    
    private ConsoleComponent console;
    
    //private ModelTrackingComponent tracking;
    private TrackingControl tracking;
    
    private FModelView modelView;          //Tree structured model viewer
    private FSimulatorView simulatorView;  //Controller viewer
    private FSimulatorSCView simSCView;
    private ControllerInterface controller;
    private SimView sim;
    private SplashScreen splashScreen;    
    private JMenuItem[] modelMenus;
    public static JMenuItem[] controlMenus;
    
    public static JButton[] ButtonControls;
    
    //Panel component
    //viewOptions = simPane + consolePane
    //splitPane   = left + viewOptions
    private JSplitPane viewOptions, splitPane;
    private JPanel simPane, consolePane, leftPane;
    
    public String modelName;
	public static String curPackages;
    private String lastModelViewed;
	private String currentDirectory;
	private String modelsPath;
    private String sourcePath;
    
		
	//The flags for the selection of view options
	public static boolean isSimView  = false;
	public static boolean isTracking = false;
	
	public static JTabbedPane tabbedPane;
    
    public View(ControllerInterface controller) 
    {
        super(ViewUtils.FRAME_TITLE);
        
        //Start screen
        splashScreen = new SplashScreen();
        splashScreen.setSplashImage(ViewUtils.loadFullImage(ViewUtils.SPLASH_SCREEN_ICON));
        splashScreen.startSplashScreen();
        
        setSize(ViewUtils.FRAME_DIM);
        
        //Center of the Frame
        Dimension screenDim = Toolkit.getDefaultToolkit().getScreenSize(); 
        setLocation(new Point((screenDim.width  - ViewUtils.FRAME_DIM.width) / 2,
                              (screenDim.height - ViewUtils.FRAME_DIM.height) / 2));
        
        PARENT_FRAME = this;
        this.controller = controller;
               
        //Construct UI for the DevsSuite
        UIconstruct(); 	               
        
        final ControllerInterface c = controller;
        
        addWindowListener(new java.awt.event.WindowAdapter() 
        {
            public void windowClosing(WindowEvent evt) 
            {
            	if(isSimView)
            		sim.saveModelLayout();
            	c.systemExitGesture();
            }
        });
              
        splashScreen.endSplashScreen(this);
    }
    
    
    /**
     * this method create the UI for the DEVSSuite
     */
    private void UIconstruct(){   
    	
    	/*Added Logo for DEVS-Suite*/
		this.setIconImage(new ImageIcon(ViewUtils.loadFullImage(ViewUtils.LOGO)).getImage());
    	
    	//console panel & tracking control
    	console        = new ConsoleComponent();        
    	tracking       = new TrackingControl();
    	console.redirectOutAndErrStreams();
    	tabbedPane = new JTabbedPane();
        tabbedPane.setTabLayoutPolicy(JTabbedPane.SCROLL_TAB_LAYOUT);
    	
    	//Facade Components
        modelView      = new FModelView(controller, tracking);
        sim            = new SimView();
        simulatorView  = new FSimulatorView(controller);
        simSCView      = new FSimulatorSCView();        
    	
    	//The animation panel & console panel
        simPane        = new JPanel(new BorderLayout());    //panel for the animation
        
        consolePane    = new JPanel(new BorderLayout());
        consolePane.add(console, BorderLayout.CENTER);
        
        tabbedPane.add(consolePane, consoleTabIndex);
        tabbedPane.setTitleAt(consoleTabIndex, "Console");
        
        
        
        //View panel
        viewOptions    = new JSplitPane(JSplitPane.VERTICAL_SPLIT, simPane, tabbedPane);
        viewOptions.setDividerLocation(400);
        viewOptions.setOneTouchExpandable(true);
        
        //Left panel including model tree and controller
        leftPane       = new JPanel();        
        leftPane.setLayout(new BorderLayout());
        leftPane.add(modelView);
        leftPane.add(simulatorView,BorderLayout.SOUTH);
        
        //Main structure : Left(leftPane) and Right(viewOptions)
        splitPane      = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT,
			                       leftPane, viewOptions);
        splitPane.setDividerLocation(260);
        splitPane.setOneTouchExpandable(true);
        getContentPane().add(splitPane, java.awt.BorderLayout.CENTER);
	
        setJMenuBar(CreateMenuBar());        
        getContentPane().add(CreateToolBar(), java.awt.BorderLayout.NORTH);          
            
        console.setVisible(true);
    }
    
    /**
     * This method will create tool bar for the application
     * @return ToolBar
     */
    private JToolBar CreateToolBar(){
    	DEVSToolBar = new JToolBar();
  	   
    	//New simulation
  	   JButton button = new JButton(new ImageIcon(ViewUtils.loadFullImage(ViewUtils.NEW_MENU)));
  	   button.setToolTipText("New");
  	   DEVSToolBar.add(button);
  	   
  	   button.addActionListener(new ActionListener() {
             public void actionPerformed(ActionEvent e) {
            	 //if no model is selected, then call LoadModel()
            	 //else reload a model
            	 if(curPackages == null && modelName == null)
            		 new LoadWizard();
            	 else
            		 reloadModelAction();        
             }
         });
  	   
  	   //load a model
  	   button = new JButton(new ImageIcon(ViewUtils.loadFullImage(ViewUtils.OPEN_MENU)));
  	   button.setToolTipText("Load Model");
  	   DEVSToolBar.add(button);
  	   
  	   button.addActionListener(new ActionListener() {
             public void actionPerformed(ActionEvent e) {
          	  new LoadWizard();          
             }
         });
  	   
  	   //Separator
  	   DEVSToolBar.addSeparator();
  	   
  	   //save console log
  	   button = new JButton(new ImageIcon(ViewUtils.loadFullImage(ViewUtils.SAVE_MENU)));
  	   button.setToolTipText("Save Console Log");
  	   DEVSToolBar.add(button);
  	   
  	   button.addActionListener(new ActionListener() {
             public void actionPerformed(ActionEvent e) {
          	   getConsoleLog();         
             }
         }); 	   
  	   
  	   //Clean console
  	   button = new JButton(new ImageIcon(ViewUtils.loadFullImage(ViewUtils.CLEAN_MENU)));
  	   button.setToolTipText("Clean Console");
  	   DEVSToolBar.add(button);
  	   
  	   button.addActionListener(new ActionListener() {
             public void actionPerformed(ActionEvent e) {
            	 clearConsoleAction();	         
             }
         });
  	   
  	   //Console Setting
  	   button = new JButton(new ImageIcon(ViewUtils.loadFullImage(ViewUtils.SETTING_MENU)));
  	   button.setToolTipText("Console Setting");
  	   DEVSToolBar.add(button);
  	   
  	   button.addActionListener(new ActionListener() {
             public void actionPerformed(ActionEvent e) {
          	  console.customizeComponent(PARENT_FRAME);         
             }
         });  	   
  	   
  	   //Separator
  	   DEVSToolBar.addSeparator();
  	   
  	   //About
  	   button = new JButton(new ImageIcon(ViewUtils.loadFullImage(ViewUtils.HELP_MENU)));
  	   button.setToolTipText("About");
  	   DEVSToolBar.add(button);
  	   
  	   button.addActionListener(new ActionListener() {
             public void actionPerformed(ActionEvent e) {
            	 showAboutBox();        
             }
         });  	   	   
  	   
  	   //Separator
  	   DEVSToolBar.addSeparator();  	  
  	   
  	   DEVSToolBar.add(Box.createRigidArea(new Dimension(250,10)));
  	   
  	   creatController();
  	   
  	   DEVSToolBar.setFloatable(false);
  	   
  	   return DEVSToolBar;
    }
    
    private void creatController(){
    	
    	ButtonControls = new JButton[5];
    	
    	ButtonControls[0] = new JButton(new ImageIcon(ViewUtils.loadFullImage(ViewUtils.STEP)));
    	ButtonControls[0].setToolTipText("Step");
 	   	DEVSToolBar.add(ButtonControls[0]);
 	   	
 	   ButtonControls[0].addActionListener(new ActionListener() {
           public void actionPerformed(ActionEvent e) {
        	   controller.userGesture(controller.SIM_STEP_GESTURE,null);           
           }
       });
 	   
    	ButtonControls[1] = new JButton(new ImageIcon(ViewUtils.loadFullImage(ViewUtils.STEPN)));
    	ButtonControls[1].setToolTipText("Step(n)");
 	   	DEVSToolBar.add(ButtonControls[1]);
 	   
 	   ButtonControls[1].addActionListener(new ActionListener() {
           public void actionPerformed(ActionEvent e) {
        	   String val = JOptionPane.showInputDialog(View.PARENT_FRAME,"Number of steps to iterate: ");
               if (val != null)
                   try
                   {
                       Integer i = new Integer(val);
                       controller.userGesture(controller.SIM_STEPN_GESTURE,i);
                   }
                   catch (Exception exp){System.err.println(exp);}          
           }
       });
 	   	
    	ButtonControls[2] = new JButton(new ImageIcon(ViewUtils.loadFullImage(ViewUtils.RUN)));
    	ButtonControls[2].setToolTipText("Run");
 	   	DEVSToolBar.add(ButtonControls[2]);
   	   
 	   ButtonControls[2].addActionListener(new ActionListener() {
           public void actionPerformed(ActionEvent e) {
        	   controller.userGesture(controller.SIM_RUN_GESTURE,null);         
           }
       });
 	   	
    	ButtonControls[3] = new JButton(new ImageIcon(ViewUtils.loadFullImage(ViewUtils.PAUSE)));
    	ButtonControls[3].setToolTipText("Pause");
 	   	DEVSToolBar.add(ButtonControls[3]);
 	   
 	   ButtonControls[3].addActionListener(new ActionListener() {
           public void actionPerformed(ActionEvent e) {
        	   controller.userGesture(controller.SIM_PAUSE_GESTURE,null);          
           }
       });
 	   	
    	ButtonControls[4] = new JButton(new ImageIcon(ViewUtils.loadFullImage(ViewUtils.RSET)));
    	ButtonControls[4].setToolTipText("Reset");
 	   	DEVSToolBar.add(ButtonControls[4]);   	
 	   	
 	   ButtonControls[4].addActionListener(new ActionListener() {
           public void actionPerformed(ActionEvent e) {
        	   String msg = "Reset this Model?\n";
               msg += "All Tracking Data Will Be Lost";
               int option = JOptionPane.showConfirmDialog(View.PARENT_FRAME,msg,
                            "Reset Model?",JOptionPane.YES_NO_OPTION);
               if (option == JOptionPane.YES_OPTION)
                   controller.userGesture(controller.SIM_RESET_GESTURE,null);        
           }
       });
 	   	
 	   	for(int i=0; i<ButtonControls.length; i++){
 	   		ButtonControls[i].setVisible(false);
 	   	}
    	
    }
    
    /**
	 * This function creates the menubar
	 * @return menubar
	 */
    private JMenuBar CreateMenuBar(){	
		
		JMenuBar menuBar = new JMenuBar();		
        
        MenuActionListener menuListener = new MenuActionListener();

        modelMenus = new JMenuItem[7];
        modelMenus[0] = new JMenuItem("Reload Model",'R');
        modelMenus[1] = new JMenuItem("Save Tracking Log...",'T');
        modelMenus[2] = new JMenuItem("Tracking Log Settings...",'T');
        modelMenus[3] = new JMenuItem("Export to CSV...",'C');
        modelMenus[4] = new JMenuItem("Export to Encoded CSV...",'E');
        modelMenus[5] = new JMenuItem("Refresh Tracking Log",'R');
        modelMenus[6] = new JMenuItem("Save Console Log...",'S');       
        
        for (int i = 0; i < modelMenus.length-1; i++)
            modelMenus[i].setEnabled(false);
        
        controlMenus    = new JMenuItem[5];
        controlMenus[0] = new JMenuItem("Step",'S');
        controlMenus[1] = new JMenuItem("Step(n)",'N');
        controlMenus[2] = new JMenuItem("Run", 'R');
        controlMenus[3] = new JMenuItem("Pause", 'P');
        controlMenus[4] = new JMenuItem("Reset", 'E');
       
        
        for (int i = 0; i < controlMenus.length; i++)
        	controlMenus[i].setEnabled(false);
        
        // Create File Menu
        JMenu fileMenu = new JMenu("File");
        
        fileMenu.setMnemonic('F');
        
        menuBar.add(ViewUtils.makeMenu(fileMenu,
                               new Object[]
                               {new JMenuItem("Load Model...",'L'),
                                null,
                                modelMenus[6],
                                modelMenus[1],
                                null,
                                modelMenus[3],
                                modelMenus[4],
                                null,
                                new JMenuItem("Exit", 'x')
                               },menuListener));
        
        //Create Option Menu
        JMenu optionsMenu = new JMenu("Options");
        optionsMenu.setMnemonic('O');
        menuBar.add(ViewUtils.makeMenu(optionsMenu,
                               new Object[] 
                               {         
                                new JMenuItem("Clear Console",'C'),                                
                                new JMenuItem("Console Settings...",'S'),
                                null,
                                modelMenus[5],
        						modelMenus[2],
                               },menuListener));
       
        //Create Control Menu
        JMenu controlsMenu = new JMenu("Controls");
        controlsMenu.setMnemonic('C');
        menuBar.add(ViewUtils.makeMenu(controlsMenu,
                               new Object[] 
                               {         
        						controlMenus[0],
        						controlMenus[1],
        						controlMenus[2],
        						controlMenus[3],
                                null,
                                controlMenus[4],
                               },menuListener));
        
        JMenu helpMenu = new JMenu("Help");
        helpMenu.setMnemonic('H');
        menuBar.add(ViewUtils.makeMenu(helpMenu, 
                               new Object[] 
                              {new JMenuItem("About", 'A')},
                               menuListener));
        
        return menuBar;
    }
	
	 private class MenuActionListener implements ActionListener
	 {
	        public void actionPerformed(java.awt.event.ActionEvent actionEvent) 
	        {
	            String cmd = actionEvent.getActionCommand();
	            if (cmd.equalsIgnoreCase("Save Tracking Log..."))
	               saveTrackingReportAction();
	            else if (cmd.equalsIgnoreCase("Save Console Log..."))
	               getConsoleLog();
	            else if (cmd.equalsIgnoreCase("Export to CSV..."))
	               exportCSVAction();
	            else if (cmd.equalsIgnoreCase("Export to Encoded CSV..."))
	               exportEncodedCSVAction();
	            else if (cmd.equalsIgnoreCase("Console Settings..."))
	                console.customizeComponent(PARENT_FRAME);
	            else if (cmd.equalsIgnoreCase("Clear Console"))
	            	clearConsoleAction();	               
	            else if (cmd.equalsIgnoreCase("Tracking Log Settings..."))
	                tracking.trackingLogOption(PARENT_FRAME, cmd);
	            else if (cmd.equalsIgnoreCase("Load Model..."))
	            	new LoadWizard();
	            else if (cmd.equalsIgnoreCase("Refresh Tracking Log"))
	            	tracking.trackingLogOption(PARENT_FRAME, cmd);
	            else if (cmd.equalsIgnoreCase("Step"))
	            	controller.userGesture(controller.SIM_STEP_GESTURE,null);               
	            else if (cmd.equalsIgnoreCase("Step(n)")){
	            	String val = JOptionPane.showInputDialog(View.PARENT_FRAME,"Number of steps to iterate: ");
	                if (val != null)
	                    try
	                    {
	                        Integer i = new Integer(val);
	                        controller.userGesture(controller.SIM_STEPN_GESTURE,i);
	                    }
	                    catch (Exception exp){System.err.println(exp);}
	            }
	            else if (cmd.equalsIgnoreCase("Run"))
	            	controller.userGesture(controller.SIM_RUN_GESTURE,null);
	            else if (cmd.equalsIgnoreCase("Pause"))
	            	controller.userGesture(controller.SIM_PAUSE_GESTURE,null);
	            else if (cmd.equalsIgnoreCase("Reset")){
	            	String msg = "Reset this Model?\n";
	                msg += "All Tracking Data Will Be Lost";
	                int option = JOptionPane.showConfirmDialog(View.PARENT_FRAME,msg,
	                             "Reset Model?",JOptionPane.YES_NO_OPTION);
	                if (option == JOptionPane.YES_OPTION)
	                    controller.userGesture(controller.SIM_RESET_GESTURE,null);
	            }
	            else if (cmd.equalsIgnoreCase("About"))
	            	showAboutBox();
	            else if (cmd.equalsIgnoreCase("Exit")){
	            	sim.saveModelLayout();
	            	System.exit(0);
	            }	           
	        }           
	}	 
        
    private void showAboutBox()
    {
        splashScreen.showAsDialog(this,"About");
    }
    
    private void showSCAction()
    {
        try
        {
            if (simSCView.isIcon())
                simSCView.setIcon(false);
        }
        catch (Exception e){}
        simSCView.setVisible(true);
        simSCView.moveToFront();
    }
    
    private void clearConsoleAction()
    {
        int option = JOptionPane.showConfirmDialog(this,
        "Clear All Console Data?","Confirm Clear...",JOptionPane.YES_NO_OPTION);
        if (option == JOptionPane.YES_OPTION)
            console.clearConsole();
    }
    
    /**
     * Load Model
     */
    private void loadModelAction()
    {       
    	    if(curPackages!=null && modelName!=null)
    	    {
            String[] val   = {curPackages, modelName}; 
            controller.userGesture(controller.LOAD_MODEL_GESTURE,val);
    	    }
    }
    /**
     * Reload a model
     */
    private void reloadModelAction()
    {        
        int option = JOptionPane.showConfirmDialog(this,"Reload current model? (All log data will be lost)",
                                                   "Reload Model...", 
                                                   JOptionPane.OK_CANCEL_OPTION,
                                                   JOptionPane.QUESTION_MESSAGE);
        if (option == JOptionPane.OK_OPTION )
        {
        	String[] val   = {curPackages, modelName};
            controller.userGesture(controller.LOAD_MODEL_GESTURE,val);
        }
        
    }
    
    private void setGridBagComponent(int x, int y, GridBagLayout gbl, GridBagConstraints gbc,
                                     JPanel panel, Component component)
    {
        gbc.gridx = x;
        gbc.gridy = y;
        gbl.setConstraints(component, gbc);
        panel.add(component);
    }

    private void exportCSVAction()
    {
        if (modelView.getSelectedModel() == null)
        {
            JOptionPane.showMessageDialog(this,
            "Cannot Export, No Model Selected.",
            "Please choose a model first...",JOptionPane.WARNING_MESSAGE);
            return;
        }
        JFileChooser chooser = new JFileChooser(currentDirectory);
        chooser.setDialogTitle("Export CSV Tracking Data (.csv)");
        if (chooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION)
        {   
            currentDirectory = chooser.getCurrentDirectory().getAbsolutePath();
            String path = chooser.getSelectedFile().getAbsolutePath();
            String tst = path.toLowerCase();
            if (!(tst.endsWith(".csv")))
                path = path + ".csv";
            controller.userGesture(controller.EXPORT_TO_CSV_GESTURE,path);
        }
    }
    
    private void exportEncodedCSVAction()
    {
        if (modelView.getSelectedModel() == null)
        {
            JOptionPane.showMessageDialog(this,
            "Cannot Export, No Model Selected.",
            "Please choose a model first...",JOptionPane.WARNING_MESSAGE);
            return;
        }
        JFileChooser chooser = new JFileChooser(currentDirectory);
        chooser.setDialogTitle("Export Encoded CSV Tracking Data (.csv)");
        if (chooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION)
        {   
            currentDirectory = chooser.getCurrentDirectory().getAbsolutePath();
            String path = chooser.getSelectedFile().getAbsolutePath();
            String tst = path.toLowerCase();
            
            String[] exportPaths = new String[2];
            
            if (tst.endsWith(".htm") || tst.endsWith(".html"))
                exportPaths[0] = path;
            else
                exportPaths[0] = path + ".html";
           
            if (tst.endsWith(".csv"))
                exportPaths[1] = path;
            else
                exportPaths[1] = path + ".csv";
            
            controller.userGesture(controller.EXPORT_TO_ENCODED_CSV_GESTURE,exportPaths);
        }
    }
    
    private void saveTrackingReportAction()
    {
        JFileChooser chooser = new JFileChooser(currentDirectory);
        chooser.setDialogTitle("Save Tracking Log (.html)");
        if (chooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION)
        {   
            currentDirectory = chooser.getCurrentDirectory().getAbsolutePath();
            String path = chooser.getSelectedFile().getAbsolutePath();
            String tst = path.toLowerCase();
            if (!(tst.endsWith(".htm") || tst.endsWith(".html")))
                path = path + ".html";
            controller.userGesture(controller.SAVE_TRACKING_LOG_GESTURE,path);
        }
    }
    
    private void saveConsoleLogAction()
    {
        JFileChooser chooser = new JFileChooser(currentDirectory);
        chooser.setDialogTitle("Save Console Log (.txt)");
        if (chooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION)
        {   
            currentDirectory = chooser.getCurrentDirectory().getAbsolutePath();
            String path = chooser.getSelectedFile().getAbsolutePath();
            String tst = path.toLowerCase();
            if (!tst.endsWith(".txt"))
                path = path + ".txt";
            controller.userGesture(controller.SAVE_CONSOLE_LOG_GESTURE,path);
        }
        
    }
    
    /**
     * Add Tracking Column based on the output from the simulator
     */
    public void addTrackingColumn(double currentTime) 
    {
    		tracking.addTracking(currentTime);
    }
    
    /**
     * Load Simulator
     */
    public void loadSimulator(FSimulator simulator) 
    {
        simulatorView.loadSimulator(simulator);
        simSCView.loadSimulator(simulator);
        modelView.loadModel(simulator.getRootModel());
        simPane.removeAll();
        simPane.repaint();
        sim.useModelClass(simulator.getRootModel(), sourcePath);
        
        if(isSimView)
        	simPane.add(sim.getSimView());
       
        if(isTracking)
        	tracking.loadSimModel(simulator.getRootModel());
        
        for(int i=0; i<ButtonControls.length; i++){
  	   		ButtonControls[i].setVisible(true);
    	}
        for (int i = 0; i < modelMenus.length; i++)
           modelMenus[i].setEnabled(true);
        for (int i = 0; i < controlMenus.length; i++)
        	controlMenus[i].setEnabled(true);
        controlMenus[3].setEnabled(false);
    }
    
    public void synchronizeView() 
    {
        modelView.synchronizeView();
        simulatorView.synchronizeView();
        simSCView.synchronizeView();
    }
    
    public String getConsoleLog() 
    {
        return console.getTextString();
    }
    
    public String getHTMLTrackingLog() 
    {
        return tracking.getHTML();
    }
    
    public String[] getEncodedCSVExport() 
    {
        return tracking.getEncodedCSV(modelView.getSelectedModel());
    }
    
    public String getCSVExport() 
    {
        return tracking.getCSV(modelView.getSelectedModel());
    }
    
    public JPanel getConsole(){
    	return consolePane;
    }
    
    public void clearConsole()
    {
        console.clearConsole();
    }
    
    public void simlationControl(String gesture){
    	if(isTracking)
    		tracking.controlTimeView(gesture);
    	if(isSimView)
    		if (gesture.equals(ControllerInterface.SIM_RUN_GESTURE))
                SimView.modelView.runToOccur();
            else if (gesture.equals(ControllerInterface.SIM_STEP_GESTURE))
            	SimView.modelView.stepToBeTaken();                
    }
   
    public SimView getSim(){
    	return sim;
    }
	
    /**
	 * this class is used to load the wizard for model loading and tracking the model's components.
	 * @author Savitha
	 */
	private class LoadWizard
	{   
		final protected String settingsFileName = "SimView_settings";
	    protected boolean insecondPage=false;
	    protected List modelPackages;   
	    protected String modelsPackage;	 
	    protected  WizardLaunch test;
	    protected  JTree tree ;
	    protected JPanel trackPanel = new JPanel();
	    protected JScrollPane west ;
	   protected JPanel east = new JPanel();
	   
	   protected ArrayList<DefaultMutableTreeNode> trackedNodes = new ArrayList();
	   protected ArrayList<Tracker>trackers= new ArrayList();
	    public LoadWizard()
	    {
	    	isSimView  = false;
			isTracking = false;
			
	    	FirstPage firstpage = new FirstPage();
	    	WizardPage[]pages ={firstpage,new SecondPage()};
	    	test = new WizardLaunch(pages);
	        test.setVisible(true);
	    	
	          
	    }
       
	    /**
	     * Loads this program's settings from its settings files.
	    */
	    protected void loadSettings()
	    {
	        try {
	            // read in the settings from the settings file
	            InputStream in = new FileInputStream(settingsFileName);
	            ObjectInputStream s = new ObjectInputStream(in);
	            modelsPath = (String)s.readObject();
	            modelPackages = (List)s.readObject();            
	            curPackages = (String)s.readObject();	            
	            lastModelViewed = (String)s.readObject();
	            sourcePath = (String)s.readObject();
	        } catch (Exception e) {
	            System.out.println("Couldn't read settings from file.");
	           /* if (modelsPath == null) modelsPath = ".";
	            if (sourcePath == null) sourcePath = ".";*/
	            if (modelPackages == null) modelPackages = new ArrayList();
	        }
	    }

	    /**
	     * Saves this program's settings to its settings files.
	     */
	    protected void saveSettings()
	    {
	        try {
	            // write out the current settings to the settings file
	            FileOutputStream out = new FileOutputStream(settingsFileName);
	            ObjectOutputStream s = new ObjectOutputStream(out);
	            s.writeObject(modelsPath);
	            s.writeObject(modelPackages);
	            s.writeObject(curPackages);
	            s.writeObject(lastModelViewed);
	            s.writeObject(sourcePath);
	            s.flush();
	        } catch (IOException e) {e.printStackTrace();}
	    }

	    /**
	     * the first page in the configuration wizard.
	     * @author Savitha 
	     *
	     */
	   protected class FirstPage extends WizardPage {
	    	 
		   protected JComboBox packagesBox;
		   protected JComboBox modelsBox;	 
		   protected ConfigureDialog configureDialog;
		   JPanel center = new JPanel();
		   JPanel panel = new JPanel();
		   

	    	 public FirstPage()
	    	 {
	    		super("first", "model configuration");
	    		loadSettings();
	    		constructUI();
	    		
	    		 // load the last model viewed from the previous program execution
		        if (curPackages != null) {
		            packagesBox.setSelectedItem(curPackages);
		            
		        }
		        if (lastModelViewed != null) {
		            modelsBox.setSelectedItem(lastModelViewed);
		        }
	    		
	    	}

	    	 /**
	    	  * called by wizardPage to enable the next, previous, finish buttons
	    	  */
	    	public void rendering(List<WizardPage> path, WizardSettings settings){
	    		
	    		 if(isTracking)
				    {
				    	
				    	setFinishEnabled(false);
			            setNextEnabled(true);
				    }
				    else
				    {
					setFinishEnabled(true);
		            setNextEnabled(false);
				    }

	    			  
	    	   }
	    	
	    	private void constructUI()
	    	{    
	    		
	    		 setLayout(new BorderLayout()); 
	    	     setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));
	    	        
	    	       
	    	        panel.setOpaque(false);
	    	        panel.setLayout(new BorderLayout());
	    	        
	    	        add(panel);

	    	      
	    	        center.setLayout(new BoxLayout(center, BoxLayout.Y_AXIS));
	    	        
	    	        center.add(Box.createRigidArea(new Dimension(15,15)));
	    	        
	    	        JPanel selection = new JPanel();
	    	        selection.setLayout(new BoxLayout(selection, BoxLayout.X_AXIS));
	    	        selection.add(new JLabel("Package: "));
	    	        
	    	        
	    	        JComboBox combo = packagesBox = new JComboBox();
	    	        populatePackagesBox(combo);
	    	        selection.add(combo);

	    	        // this keeps the combo-box from taking up extra height
	    	        // unnecessarily under JRE 1.4
	    	        combo.setMaximumSize(new Dimension(combo.getMaximumSize().width,
	    	            combo.getMinimumSize().height));

	    	        // when the a choice is selected from the packages combo-box
	    	        packagesBox.addActionListener(new ActionListener() {
	    	            public void actionPerformed(ActionEvent e) {
	    	                // ignore the first choice when it is selected, as it is
	    	                // just an instructions string; also, ignore when no choice
	    	                // is selected
	    	                if (packagesBox.getSelectedIndex() <= 0) return;
	    	                // make the selected item the current model package name
	    	               curPackages = (String)packagesBox.getSelectedItem();           	
	    	               
	    	                populateModelsBox(modelsBox);
	    	            }
	    	        });
	    	        
	    	        
	    	        
	    	        center.add(selection);
	    	        center.add(Box.createRigidArea(new Dimension(15,15)));

	    	        selection = new JPanel();
	    	        selection.setLayout(new BoxLayout(selection, BoxLayout.X_AXIS));
	    	        selection.add(Box.createRigidArea(new Dimension(15,1)));
	    	        selection.add(new JLabel("Model: "));
	    	        
	    	        // add the models combo-box
	    	        combo = modelsBox = new JComboBox();
	    	        selection.add(combo);

	    	       
	    	        combo.setMaximumSize(new Dimension(combo.getMaximumSize().width,
	    	            combo.getMinimumSize().height));
	    	        
	    	        

	    	        // when the a choice is selected from the models combo-box
	    	        modelsBox.addActionListener(new ActionListener() {
	    	            public void actionPerformed(ActionEvent e) {
	    	                // ignore the first choice when it is selected, as it is
	    	                // just an instructions string; also, ignore when no choice
	    	                // is selected
	    	                if (modelsBox.getSelectedIndex() <= 0) return;

	    	                modelName = (String)modelsBox.getSelectedItem();
	    	                lastModelViewed = modelName;
	    	            }
	    	        });
	    	        
	    	        center.add(selection);
	    	        center.add(Box.createRigidArea(new Dimension(10,10)));
	    	        
	    	        selection = new JPanel(new GridLayout(1,1));
	    	        JCheckBox isSimViewSelected = new JCheckBox("SimView", isSimView);
	    	        isSimViewSelected.setHorizontalAlignment(SwingConstants.LEFT);
	    	       
	    	        selection.add(isSimViewSelected);
	    	      
	    	        
	    	        center.add(selection); 
	    	        center.add(Box.createRigidArea(new Dimension(10,10)));
	    	        
	    	        selection = new JPanel(new GridLayout(2,1));
	    	        
	    	        JCheckBox isTrackingSelected = new JCheckBox("Tracking", isTracking);
	    	        isTrackingSelected.setHorizontalAlignment(SwingConstants.LEFT);
	    	        selection.add(isTrackingSelected);
	    	        
	    	        center.add(selection); 
	    	       
	    	        
	    	        isSimViewSelected.addItemListener(
	    	        		new ItemListener() {
	    	        			public void itemStateChanged(ItemEvent e) {
	    	        	            if (e.getStateChange() == ItemEvent.SELECTED)
	    	        	            	isSimView = true;
	    	        	            else
	    	        	            	isSimView = false;
	    	        			}
	    	        		});
	    	       
	    	        isTrackingSelected.addItemListener(
	    	        		new ItemListener() {
	    	        			public void itemStateChanged(ItemEvent e) {
	    	        	            if (e.getStateChange() == ItemEvent.SELECTED)
	    	        	            {
	    	        	            	isTracking= true;
	    	        	            	  insecondPage = true;
	    	        	            	 setFinishEnabled(false);
	 	    	        	            setNextEnabled(true);
	    	        	            }
	    	        	            else
	    	        	            {
	    	        	            	isTracking = false;
	    	        	            	 insecondPage = false;
	    	        	            setFinishEnabled(true);
	    	        	            setNextEnabled(false);
	    	        	            }
	    	        	        }
	    	        		});
	    	       	
	    	      
	    	       
	    	        selection = new JPanel(new FlowLayout(FlowLayout.LEFT));
	    	      
	    	     
	    	        JButton button = new JButton("configure");
	    	        button.setFont(new Font("SansSerif", Font.BOLD, 12));
	    	        button.setHorizontalAlignment(SwingConstants.LEFT);
	    	        selection.add(button);
	    	        center.add(selection);
	    	        
	    	        selection = new JPanel();
	    	        center.add(selection);
	    	      
	    	        selection = new JPanel(new FlowLayout(FlowLayout.LEFT));
	    	        configureDialog = new ConfigureDialog(test);
	    	        selection.add(configureDialog.main);
 	               configureDialog.main.setVisible(false);
	    	       
	    	       center.add(selection);
	    	        
	    	        // when the configure button is clicked
	    	        button.addActionListener(new ActionListener() {
	    	            public void actionPerformed(ActionEvent e) {
	    	              
	    	            	 // display the configure dialog
	    	            	 configureDialog.main.setVisible(true);
	    		    	         

	    	               
	    	                
	    	            }
	    	        });
	    	        
 
	    	        
	    	       	        
	    	       
	    	        panel.add(center, BorderLayout.CENTER);
	    	       
	    	        
	    	       
	    	}
	    	
	    	
	    	   /**
		     * Adds the names of all java class files (which are assumed to
		     * be compiled devs java models) in the models-path to
		     * the given combo-box.
		     *
		     * @param   box     The combo-box to which to add the model names.
		     */
		    protected void populateModelsBox(JComboBox box)
		    {
		    	
		        // create a filename filter (to be used below) that will
		        // match against ".class" files (and ignore inner classes)
		    	TreeSet sortedFiles=null;
		        final String extension = ".class";
		        FilenameFilter filter =  new FilenameFilter() {
		            public boolean accept(File dir, String name) {
		                return name.endsWith(extension) && name.indexOf('$') == -1;
		            }
		        };
		        
		        // find all java class files (that aren't inner classes) in the
		        // models-path
		        
		        if(modelsPath.matches("(.*).jar(.*)"))
		        {
		         
				try {
					URL jar;
					String name;
					ArrayList classes = new ArrayList ();
					File path = new File(modelsPath);
					jar =path.toURI().toURL();
					ZipInputStream zip = new ZipInputStream( jar.openStream());
					
					while(true) {
					    ZipEntry entry = zip.getNextEntry();
					    if (entry == null)
					      break;
					   name= entry.getName();
					   
					   //for onejar
	                   if(name.startsWith("main")&& name.endsWith("main.jar"))
	                   {
	                	   ZipInputStream innerZip = new ZipInputStream(zip);
	                	   String innerName=null;
	                	   while(true)
	                	   {
	                		   ZipEntry innerEntry = innerZip.getNextEntry();
	                		   if(innerEntry==null)
	                		   break;
	                		   
	                		   innerName= innerEntry.getName();
	                		   
	                		   if (innerName.startsWith(curPackages) &&
	   		                        (innerName.endsWith (".class")) )
	   					    		{
	   					    	   String names[]= null;
	   					    	     if(innerName.matches("(.*)/(.*)"))
	   					    	     {
	   					    	    names = innerName.split("/");
	   					    	     }
	   					    	     else 				    	     {
	   					    	    	 names = innerName.split("\\");
	   					    	     }
	   					   
	   						            classes.add(names[names.length-1]);
	   					    	     }  
	   					    }
	                			   
	                		   
	                	   }
	                   
                       
					    if (name.startsWith(curPackages) &&
		                        (name.endsWith (".class")) )
					    		{
					    	   String names[]= null;
					    	     if(name.matches("(.*)/(.*)"))
					    	     {
					    	    names = name.split("/");
					    	     }
					    	     else 				    	     {
					    	    	 names = name.split("\\");
					    	     }
					   
						            classes.add(names[names.length-1]);
					    	     }  
					    }
					
					  if (classes.isEmpty()) {
				            JOptionPane.showMessageDialog(test,
				                "The selected models package does not appear to be available for loading.  " +
				                "Please select another.");
				            return;
				        }
					    
					sortedFiles = new TreeSet(classes);
		        
				
					

				} 
				catch (MalformedURLException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
				catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
		        }
		        else{
		     
		        File path = new File(modelsPath + "/" + curPackages.replace('.', '/'));
		        File[] files = path.listFiles(filter);
		        
		        
		        // if the models-path doesn't exist
		        if (files == null) {
		            JOptionPane.showMessageDialog(test,
		                "The selected models package does not appear to be available for loading.  " +
		                "Please select another.");
		            return;
		        }
		        
		        // sort the names of the java class files found above
		        sortedFiles = new TreeSet(Arrays.asList(files));
		        }
		        
		        box.removeAllItems();

		        box.addItem("Select a model");

		        // for each java class file in the models-path (we are assuming
		        // each such file to be a compiled devs java model)
		        Iterator i = sortedFiles.iterator();
		        while (i.hasNext()) {
		            // add this class file's name (minus its extension) to the box
		        	Object temp = i.next();
		        	 String name =null;
		        	if(temp instanceof File)
		        	{
		          name=    ((File)temp).getName();
		             
		        	}
		        	else
		        	{
 		        		 name = ((String)temp);
		        		
		        	}
		        	box.addItem(name.substring(0,
			                name.length() - extension.length()));
		           
		        }
		    }


		    /**
		     * Adds the names of all the user-specified java packages containing
		     * models to the given combo-box.
		     *
		     * @param   box     The combo-box to which to add the model names.
		     */
		    protected void populatePackagesBox(JComboBox box)
		    {
		        box.removeAllItems();

		        box.addItem("Select a package");
		      	      
		        // if the user has specified a list of model packages
		        if (modelPackages != null) {
		            // for each model package in the list
		            for (int i = 0; i < modelPackages.size(); i++) {
		                // add this package's name to the given combo-box
		                box.addItem((String)modelPackages.get(i));
		            }
		        }
		    }
	    	

		    
		    
		    /**
		     * A dialog in which the user may specify various program-wide settings.
		     */
		    class ConfigureDialog          
		    {
		        /**
		         * Constructs a configure-dialog.
		         *
		         * @param   owner       The parent frame of this dialog.
		         */
		    	
		    	 JPanel main = new JPanel();
		        public ConfigureDialog(JDialog owner)
		        {

		            constructUI();
		        }

		        /**
		         * Constructs the UI of this dialog.
		         */
		        protected void constructUI()
		        {
		            // have the close-window button do nothing for this dialog
		           
		           
		           
		            main.setLayout(new BoxLayout(main, BoxLayout.Y_AXIS));
		           main.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));
		           

		            // add the class path label
		            JLabel label = new JLabel("Path to packages of model classes (from current folder)");
		            label.setAlignmentX(0.0f);
		            main.add(label);

		            // add the class path field
		            final JTextField classPathField = new JTextField(modelsPath);
		            JTextField field = classPathField;
		            field.setAlignmentX(0.0f);
		            main.add(field);

		            // limit the height of the class path field
		            field.setMaximumSize(new Dimension(1000,
		                (int)(1.5 * getFontMetrics(field.getFont()).getHeight())));

		            main.add(Box.createRigidArea(new Dimension(0, 10)));

		            // add the source path label
		            label = new JLabel("Path to packages of model source files (from current folder)");
		            label.setAlignmentX(0.0f);
		            main.add(label);

		            // add the source path field
		            final JTextField sourcePathField = new JTextField(sourcePath);
		            field = sourcePathField;
		            field.setAlignmentX(0.0f);
		            main.add(field);

		            // limit the height of the source path field
		            field.setMaximumSize(new Dimension(1000,
		                (int)(1.5 * getFontMetrics(field.getFont()).getHeight())));

		            main.add(Box.createRigidArea(new Dimension(0, 10)));

		            // add the package names label
		            label = new JLabel("Model package names (one per line)");
		            label.setAlignmentX(0.0f);
		            main.add(label);

		            // add the package names text area
		            final JTextArea packagesArea = new JTextArea(modelsPath);
		            JTextArea area = packagesArea;
		            JScrollPane scrollPane = new JScrollPane(area);
		            scrollPane.setAlignmentX(0.0f);
		            main.add(scrollPane);

		            // for each entry in our model-packages list
		            String text = "";
		            for (int i = 0; i < modelPackages.size(); i++) {
		                // add this entry as a line to the text area's text
		                text += ((String)modelPackages.get(i)) + "\n";
		            }
		            area.setText(text);

		            // have ctrl-insert do a copy action in the text area
		            Keymap keymap = area.addKeymap(null, area.getKeymap());
		            KeyStroke key = KeyStroke.getKeyStroke(KeyEvent.VK_INSERT,
		                Event.CTRL_MASK);
		            keymap.addActionForKeyStroke(key, new DefaultEditorKit.CopyAction());

		            // have shift-insert do a paste action in the text area
		            key = KeyStroke.getKeyStroke(KeyEvent.VK_INSERT, Event.SHIFT_MASK);
		            keymap.addActionForKeyStroke(key,
		                new DefaultEditorKit.PasteAction());
		            area.setKeymap(keymap);

		            main.add(Box.createRigidArea(new Dimension(0, 10)));

		            JPanel panel = new JPanel();
		            panel.setOpaque(false);
		            panel.setLayout(new BoxLayout(panel, BoxLayout.X_AXIS));
		            panel.setAlignmentX(0.0f);
		            main.add(panel);

		            panel.add(Box.createHorizontalGlue());

		            // add the ok button
		            JButton button = new JButton("Ok");
		            button.setAlignmentX(0.0f);
		            panel.add(button);

		            // when the ok button is clicked
		            button.addActionListener(new ActionListener() {
		                public void actionPerformed(ActionEvent e) {
		                    // store the class path field entry
		                    modelsPath = classPathField.getText();
		                    
		                    
		                    
		                    if (modelsPath.equals("")) {
		                        modelsPath = ".";
		                    }

		                    // if there is a trailing slash on the class path entry
		                    if (modelsPath.endsWith("/")) {
		                        // remove it
		                        modelsPath = modelsPath.substring(0,
		                            modelsPath.length() - 1);
		                    }

		                    // store the source path field entry
		                    sourcePath = sourcePathField.getText();
		                    if (sourcePath.equals("")) {
		                        sourcePath = ".";
		                    }

		                    // if there is a trailing slash on the source path entry
		                    if (sourcePath.endsWith("/")) {
		                        // remove it
		                        sourcePath = sourcePath.substring(0,
		                            sourcePath.length() - 1);
		                    }

		                    // keep doing this
		                    modelPackages = new ArrayList();
		                    StringReader stringReader =
		                        new StringReader(packagesArea.getText());
		                    BufferedReader reader = new BufferedReader(stringReader);
		                    while (true) {
		                        // read the next line specified in the packages text
		                        // area
		                        String line = null;
		                        try {
		                            line = reader.readLine();
		                        } catch (IOException ex) {ex.printStackTrace(); continue;}

		                        // if there are no more lines
		                        if (line == null) break;

		                        // if this line is blank, skip it
		                        line = line.trim();
		                        if (line.equals("")) continue;

		                        // add this line's package name to our list of package
		                        // names
		                        modelPackages.add(line);
		                    }

		                    populatePackagesBox(packagesBox);
		                    
		                    saveSettings();

		                    main.setVisible(false);
		                }
		            });
		        }
		    }

		    
	    }
	    
	   /**
	    * The second page where the models are displayed in Tree view. When the model is clicked , the tracking options and variables are
	    * provided. The component is highlighted when tracked.
	    * @author Savitha
	    *
	    */
	private class SecondPage extends WizardPage{
		
	
		 public SecondPage()
		 {
			super("second", "Component Tracking");	   
			constructUI();
		}

		public void rendering(List<WizardPage> path, WizardSettings settings){
		        
			    /*if(isTracking)
			    insecondPage = true;*/
				setFinishEnabled(true);
	            setNextEnabled(false);
			    
		   }

		private void constructUI()
		{      
			   setLayout(new BorderLayout()); 
		       setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));
		       trackPanel.setOpaque(false);
		       trackPanel.setLayout(new BorderLayout());
		       add(trackPanel);	        
		}
		
		 @Override
	     public void updateSettings(WizardSettings settings) {
	        super.updateSettings(settings);
	        	        
	     }	  	
	}

	public class WizardLaunch extends JDialog {
  
		   public WizardLaunch(WizardPage[] pages){
			   
		      final WizardContainer wc =
		         new WizardContainer(new TestFactory(pages), new TitledPageTemplate());
		     
		      // add a wizard listener to update the dialog titles and notify the
		      // surrounding application of the state of the wizard:
		      wc.addWizardListener(new WizardListener(){
		         @Override
		         public void onCanceled(List<WizardPage> path, WizardSettings settings) {
		          
		            WizardLaunch.this.dispose();
		         }

		         @Override
		         public void onFinished(List<WizardPage> path, WizardSettings settings) {
		        	 WizardLaunch.this.dispose();
		        	 if(!insecondPage)
		        	 { 
		             lastModelViewed = modelName;
		        	 loadModelAction();	            	
		             saveSettings();	  
		             
		        	 }
		        	 else
		        	 {   
		        		 for(Tracker tracker:trackers)
		        		 {
		        		 if(tracker.getTrackingLogSelected()){
		                    	tracker.getTrackingControl().registerTrackingLog();                	
		                	}
		        		 if(tracker.getTimeViewSelected())
		                		tracker.getTrackingControl().registerTimeView(tracker.getGraphs(), tracker.getModelNum(), tracker.getxUnit(), tracker.gettimeIncrement(),tracker.getisBreakout());   
		        		 
		        		 }
		        	 }
		        		
		        	 
		         }

		         @Override
		         public void onPageChanged(WizardPage newPage, List<WizardPage> path) {
		            
		            // Set the dialog title to match the description of the new page:
		        	 trackPanel.removeAll();
		        	 lastModelViewed = modelName;
		        	 loadModelAction();	            	
		             saveSettings();
		             
		             //panel for JTree
		               tree= new JTree(modelView.getJTreeModel());
		               WizardTreeListener wlistener = new WizardTreeListener();
				        if(tree!=null)
				        {
				        tree.addTreeSelectionListener(wlistener);

				
				        }
				        
		               west = new JScrollPane(tree);
		               JSplitPane trackSplitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT,
		                       west, east);
		               trackSplitPane.setDividerLocation(150);
		               trackSplitPane.setOneTouchExpandable(true);
		               trackPanel.add(trackSplitPane, java.awt.BorderLayout.CENTER);
				       trackPanel.revalidate();
				       trackPanel.repaint();
		                WizardLaunch.this.setTitle(newPage.getDescription());
		         }
		      });
		      
		      this.setResizable(false);
		      
		      this.setDefaultCloseOperation(DISPOSE_ON_CLOSE);
		      this.getContentPane().add(wc);
		      this.setSize(650,600);
		      
		   }

		   /**
		    * Implementation of PageFactory to generate the wizard pages needed
		    * for the wizard.
		    */
		   private class TestFactory implements PageFactory{
			   private  WizardPage[] pages;
		       
		       
		      public TestFactory(WizardPage[]page)
		      {
		    	  pages =page;
		      }
			       
		      @Override
		      public WizardPage createPage(List<WizardPage> path,
		            WizardSettings settings) {
		         
		         
		         // Get the next page to display.  The path is the list of all wizard
		         // pages that the user has proceeded through from the start of the
		         // wizard, so we can easily see which step the user is on by taking
		         // the length of the path.  This makes it trivial to return the next
		         // WizardPage:
		         WizardPage page = pages[path.size()];
		         
		        
		         return page;
		      }
		      
		 
		   }
		  
		}
	
	//WizardTree Listener class use din second page
	 
	  protected class WizardTreeListener implements TreeSelectionListener
	    {   
		  
		  
	        public void valueChanged(TreeSelectionEvent e) 
	        {   
	            DefaultMutableTreeNode node = (DefaultMutableTreeNode)tree.getLastSelectedPathComponent();
	             if (node != null)
	             {
	           FModel model= (FModel)node.getUserObject();
	           
	           TrackComponent trackcomponent= new TrackComponent();
	           trackcomponent.UITracking(modelView.getTrackingControl().findTrackerFor(model),model);
	            }
	        }
	        
	        
	        private class TrackComponent
	        {
	        	
			    Tracker tracker ;
			    JCheckBox phase ;
		        JCheckBox sigma ;
		        JCheckBox tl ;
		        JCheckBox tn;
		        JCheckBox timeView;
		        JCheckBox htmltracking;
		        JCheckBox timeViewSep;
		        JCheckBox showZeroTimeAdvance;
		        JTextField phaseUnit;
		        JTextField sigmaUnit;		       
		        JTextField tlUnit;
		        JTextField tnUnit;
		        JTextField xUnit;
		        JTextField timeIncre;
		        private boolean atLeastOneInputTracked;
		        private boolean atLeastOneOutputTracked;
		        private boolean[] inputPorts;
		        private boolean[] outputPorts;
		        List inputPortNames;
		        List outputPortNames;
		        ArrayList graphs ;
		        String[] inputUnits;
		        String[] outputUnits;
                JButton trackButton = new JButton("track");
                boolean track[] ={false,false,false};
                
	             public void UITracking(Tracker t,FModel model)
	             {  
	            
	            	
	                tracker = t; 
	                graphs = tracker.getGraphs();
	    	        east.removeAll();
		            east.setLayout(new BoxLayout(east, BoxLayout.Y_AXIS));
		            
		            
		            
		            
		            JPanel selection = new JPanel();
		            selection.setLayout(new BoxLayout(selection, BoxLayout.X_AXIS));
		        
		        //different tracking options
		        JPanel timeViewPanel = new JPanel(new GridLayout(0,1));                
		         timeView = new JCheckBox("TimeView",tracker.getTimeViewSelected());
		         timeViewSep = new JCheckBox("TimeView Separate ",tracker.getTimeViewSelected());
		         htmltracking = new JCheckBox("Tracking Log", tracker.getTrackingLogSelected());
		      
		        timeViewPanel.add(timeView);        
		        timeViewPanel.add(htmltracking);
		        timeViewPanel.add(timeViewSep);
		        
		        timeView.addItemListener(
		        		new ItemListener() {
		        			public void itemStateChanged(ItemEvent e) {
		        				if (e.getStateChange() == ItemEvent.SELECTED)
		        				{
		        					tracker.setisBreakout(false);
		        					track[0]=true;
		        					trackButton.setEnabled(true);
		        				}  
		        				
		        				else
		        				{   
		        					track[0]=false;
		        					if((track[1]||track[2]))
		        						trackButton.setEnabled(true);
		        					else
		        						trackButton.setEnabled(false);
		        				}
		        			}
		        		});
		        timeViewSep.addItemListener(
		        		new ItemListener() {
		        			public void itemStateChanged(ItemEvent e) {
		        				if (e.getStateChange() == ItemEvent.SELECTED){
		        					tracker.setisBreakout(true);
		        					track[1]=true;
		        					trackButton.setEnabled(true);
		        				}
		        			
		        			else
	        				{  
		        				track[1]=false;
	        					if((track[0]||track[2]))
	        						trackButton.setEnabled(true);
	        					else
	        						trackButton.setEnabled(false);
	        				}
		        			}
		        		});
		           
		        htmltracking.addItemListener(
		        		new ItemListener() {
		        			public void itemStateChanged(ItemEvent e) {
		        				if (e.getStateChange() == ItemEvent.SELECTED)
		        				{
		        					
		        					track[2]=true;
		        					trackButton.setEnabled(true);
		        				}  
		        				
		        				else
		        				{   
		        					track[2]=false;
		        					if((track[0]||track[1]))
		        						trackButton.setEnabled(true);
		        					else
		        						trackButton.setEnabled(false);
		        				}
		        			}
		        		});
		        JPanel timeViewPanel2 = new JPanel();
		        timeViewPanel2.add(timeViewPanel);
		        JScrollPane timeViewScrollPane1 = new JScrollPane(timeViewPanel2);
		        timeViewScrollPane1.setBorder(BorderFactory.createTitledBorder("View Options"));
		        selection.add(timeViewScrollPane1);
		        
		        // phase, Sigma, tl, tn
		        JPanel modelPanel = new JPanel(new GridLayout(0,1));
		        modelPanel.setBorder(BorderFactory.createTitledBorder("States/Unit"));
		        
		       phaseUnit = new JTextField();
		       sigmaUnit = new JTextField();
		       tlUnit = new JTextField();
		       tnUnit = new JTextField();
		       
		       for(Object g:graphs)
		       {
		    	   Graph graph = (Graph)g;
		    	   if(graph.getName().equals("tL"))
		    			tlUnit.setText(graph.getUnit());   
		    	   if(graph.getName().equals("tN"))
		    			tnUnit.setText(graph.getUnit()); 
		    	   if(graph.getName().equals("Phase"))
		    			phaseUnit.setText(graph.getUnit()); 
		    	   if(graph.getName().equals("Sigma"))
		    			sigmaUnit.setText(graph.getUnit()); 
		       }
		        
		        JPanel unitPane = new JPanel(new GridLayout(0,2));
		        
		       phase = new JCheckBox("Phase",tracker.getTrackPhase());
		       sigma = new JCheckBox("Sigma",tracker.getTrackSigma());
		       tl = new JCheckBox("TL",tracker.getTrackTL());
		       tn = new JCheckBox("TN",tracker.getTrackTN());
		        
		        if (model instanceof FAtomicModel)
		        {
		        unitPane.add(phase); 
	        	unitPane.add(phaseUnit);
	        	modelPanel.add(unitPane);
	        	
	        	unitPane = new JPanel(new GridLayout(0,2));
	        	unitPane.add(sigma); 
	        	unitPane.add(sigmaUnit);
	        	modelPanel.add(unitPane);
		        }
		        
	        	unitPane = new JPanel(new GridLayout(0,2));
	         	unitPane.add(tl); 
	         	unitPane.add(tlUnit);
	         	modelPanel.add(unitPane);
	             
	         	unitPane = new JPanel(new GridLayout(0,2));
	         	unitPane.add(tn); 
	         	unitPane.add(tnUnit);
	         	modelPanel.add(unitPane);
	         	
	             //modelPanel.add(Box.createHorizontalStrut(100));
	             selection.add(modelPanel);
	            
		       
	             //X-axis
	             
	             xUnit = new JTextField(tracker.getxUnit());
	             xUnit.setHorizontalAlignment(JTextField.RIGHT);
	             JPanel axisPanel = new JPanel(new GridLayout(0,1));                
	             JLabel xaxis = new JLabel("X-Axis");
	             unitPane = new JPanel(new GridLayout(0,2));
	         	 unitPane.add(xaxis); 
	         	 unitPane.add(xUnit);
	             axisPanel.add(unitPane);
	           
	             //Time Increment
	             timeIncre = new JTextField(tracker.gettimeIncrement());
	             timeIncre.setHorizontalAlignment(JTextField.RIGHT);
	             JLabel time = new JLabel("Increment");
	             unitPane = new JPanel(new GridLayout(0,2));
	         	 unitPane.add(time); 
	         	 unitPane.add(timeIncre);        
	         	 axisPanel.add(unitPane);
	         	 
	         	 //zerotime advance
	         	 showZeroTimeAdvance = new JCheckBox("ZeroTimeAdvance plots",false);
	         	unitPane = new JPanel(new GridLayout(0,1));
	         	 unitPane.add(showZeroTimeAdvance);         
	         	 axisPanel.add(unitPane);
	         	 
	         	showZeroTimeAdvance.addItemListener(
    	        		new ItemListener() {
    	        			public void itemStateChanged(ItemEvent e) {
    	        	            if (e.getStateChange() == ItemEvent.SELECTED)
    	        	            {
    	        	            	 for(Object g:graphs)
    	        	  		       {
    	        	  		    	   Graph graph = (Graph)g;
    	        	  		    	  graph.setZeroTimeAdvance(true);
    	        	  		       }
    	        	            }
    	        	            else
    	        	            {

   	        	            	 for(Object g:graphs)
   	        	  		       {
   	        	  		    	   Graph graph = (Graph)g;
   	        	  		    	  graph.setZeroTimeAdvance(false);
   	        	  		       }
    	        	            }
    	        	        }
    	        		});
	             
	            // axisPanel.add(Box.createHorizontalStrut(100));
	             JPanel XaxisPanel = new JPanel();
	             XaxisPanel.add(axisPanel);
	             JScrollPane timeViewScrollPane = new JScrollPane(XaxisPanel);
	             timeViewScrollPane.setBorder(BorderFactory.createTitledBorder("X-Axis/Unit"));
	             selection.add(timeViewScrollPane);
	             
	             east.add(selection);
	             
	             east.add(Box.createHorizontalStrut(10));
	             
	             //input ports
	            selection = new JPanel();
	            selection.setLayout(new BoxLayout(selection, BoxLayout.X_AXIS));
	            
	            inputPortNames = model.getInputPortNames();
	            outputPortNames = model.getOutputPortNames();
	            
	            
	            Object col[] = {"Input Ports","Units","Selected"};
	            Object[][] data = new Object[inputPortNames.size()][3];
	            
	            
	         	 inputUnits= tracker.getInputPortUnits();   
	            
	            inputPorts = tracker.gettrackInputPorts();
	            
	             int row=0;
	             for(int i =0;i<inputPortNames.size();i++)
	             {
	          	  
	          	   data[row][0]=String.valueOf(inputPortNames.get(i));
	          	   data[row][1]=inputUnits[i];
	          	   data[row][2]=inputPorts[i];
	          	   row++;
	             }
	              
	             DefaultTableModel ipmodel = new DefaultTableModel(data,col); 
	             JTable table=new JTable(ipmodel){
	            
	             public boolean isCellEditable(int arg0, int arg1) {
	              
	                 return (arg1 == 1 || arg1 == 2);
	             }
	             
	             public void setValueAt(Object aValue, int rowIndex, int columnIndex) {  
	                 if(columnIndex == 2){  
	                    
	                    inputPorts[rowIndex]=(boolean)aValue; 
	                    
	                 } 
	                 
	                 if(columnIndex == 1){  
		                    if(aValue!=null)
		                    inputUnits[rowIndex]=(String)aValue; 
		                    
		                 }  
	                 
	                 super.setValueAt(aValue, rowIndex, columnIndex);  
	             }  
	             
	             public Class getColumnClass(int column) {
	                 switch (column) {
	                     case 0:
	                         return String.class;
	                     case 1:
	                         return String.class;
	                     case 2:
	                         return Boolean.class;
	                     
	                    
	                 }
					return null;}
	             };
	             
	             
	         JScrollPane spane = new JScrollPane(table);
	          
	         JPanel inset1 = new JPanel();
	         inset1.add(spane);
	         JScrollPane inputScrollPane = new JScrollPane(inset1);
	         inputScrollPane.setBorder(BorderFactory.createTitledBorder("Input Ports/Unit"));
	         selection.add(inputScrollPane);
	         east.add(selection);
	         east.add(Box.createHorizontalStrut(10));
	         
	         //o/p ports
	         selection = new JPanel();
	         selection.setLayout(new BoxLayout(selection, BoxLayout.Y_AXIS));
	         
	         outputPorts = tracker.gettrackOutputPorts();
	            
	         DefaultTableModel opmodel;
	         JTable table1;
	         Object col1[] = {"Output Ports","Units","Selected"};
	          Object[][] data1 = new Object[outputPortNames.size()][3];
	          outputUnits= tracker.getOutputPortUnits();    
	            
	          int row1=0;
	          for(int i =0;i<outputPortNames.size();i++)
	          {
	       	  
	       	   data1[row1][0]=String.valueOf(outputPortNames.get(i).toString());
	       	   
	       	   data1[row1][1]=outputUnits[i];
	       	   data1[row1][2]=outputPorts[i];
	       	   row1++;
	          }
	           
	          opmodel = new DefaultTableModel(data1,col1); 
	          table1=new JTable(opmodel)
	          {
	          public boolean isCellEditable(int arg0, int arg1) {
	           
	        	  return (arg1 == 1 || arg1 == 2);
	             }
	             
	             public void setValueAt(Object aValue, int rowIndex, int columnIndex) {  
	                 if(columnIndex == 2){  
	                    
	                    outputPorts[rowIndex]=(boolean)aValue; 
	                     
	                 } 
	                 
	                 if(columnIndex == 1){  
		                    
	                	 if(aValue!=null)
		                    outputUnits[rowIndex]=(String)aValue; 
	                	
		                     
		                 } 
	                 super.setValueAt(aValue, rowIndex, columnIndex);  
	             }  
	             
	             public Class getColumnClass(int column) {
	                 switch (column) {
	                     case 0:
	                         return String.class;
	                     case 1:
	                         return String.class;
	                     case 2:
	                         return Boolean.class;
	                     
	                    
	                 }
					return null;}
	             };
	             
	      JScrollPane spane1 = new JScrollPane(table1);
	       
	      JPanel inset2 = new JPanel();
	      inset2.add(spane1);
	      JScrollPane inputScrollPane1 = new JScrollPane(inset2);
	      inputScrollPane1.setBorder(BorderFactory.createTitledBorder("Output Ports/Unit"));
	      selection.add(inputScrollPane1);
	      east.add(selection);
	       
	     
	      selection = new JPanel(new FlowLayout(FlowLayout.LEFT));
	      selection.add(Box.createRigidArea(new Dimension(20,1)));
	       
	      
	      trackButton.setFont(new Font("SansSerif", Font.BOLD, 12));
	      trackButton.setHorizontalAlignment(SwingConstants.LEFT);
	      selection.add(trackButton);
	      //trackButton.setEnabled(false);
	      east.add(selection);
	      
	        
	     trackButton.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
               
        	  trackButton.setEnabled(false);
        	   DefaultMutableTreeNode node = (DefaultMutableTreeNode)tree.getLastSelectedPathComponent();
        	   graphs = new ArrayList();
        	   //add node in arrayList
        	   if(!trackedNodes.contains(node))
        	   {
        		  trackedNodes.add(node); 
        	   }
        	   
        	   trackers.add(tracker);
        	   tree.setCellRenderer(new MyTreeCellRenderer(trackedNodes));
          	   tracker.setTrackPhase(phase.isSelected());
               tracker.setTrackSigma (sigma.isSelected());
               tracker.setTrackTL(tl.isSelected());
               tracker.setTrackTN(tn.isSelected());
               tracker.settimeIncrement(timeIncre.getText());
               tracker.setxUnit(xUnit.getText());
               tracker.setInputPortUnits(inputUnits);
               tracker.setOutputPortUnits(outputUnits);
               
               if (!tracker.getTrackingLogSelected())
               {
               	tracker.setTrackingLogSelected(htmltracking.isSelected());            	
               	
               }  
               
               GraphFactory graphFactory= new GraphFactory();
           	  
               if(tl.isSelected())
               {
            	  Graph tl =graphFactory.createChart("STATEVARIABLE");
            	  tl.setCategory("STATEVARIABLE");
            	  tl.setUnit(tlUnit.getText());
            	  tl.setName("tl");
            	  tl.setZeroTimeAdvance(showZeroTimeAdvance.isSelected());
            	  graphs.add(tl);
               }
               if(tn.isSelected())
               {
            	  Graph tn =graphFactory.createChart("STATEVARIABLE");
            	  tn.setName("tN");
             	  tn.setUnit(tnUnit.getText());
             	  tn.setCategory("STATEVARIABLE");
             	 tn.setZeroTimeAdvance(showZeroTimeAdvance.isSelected());
             	  graphs.add(tn);
               	
               }
               if(phase.isSelected())
               {
            	  Graph phase =graphFactory.createChart("STATE");
            	  phase.setName("Phase");
             	  phase.setUnit(phaseUnit.getText());
             	  phase.setCategory("STATE");
             	 phase.setZeroTimeAdvance(showZeroTimeAdvance.isSelected());
             	  graphs.add(phase);
               }
               if(sigma.isSelected())
               {
            	  Graph sigma =graphFactory.createChart("SIGMA");
             	  sigma.setName("Sigma");
             	  sigma.setUnit(sigmaUnit.getText());
             	  sigma.setCategory("SIGMA");
             	 sigma.setZeroTimeAdvance(showZeroTimeAdvance.isSelected());
             	  graphs.add(sigma);   
               }
               tracker.setatLeastOneInputTracked(false);
               for (int i = 0; i < inputPorts.length; i++)
                {
                   if(inputPorts[i])
                   {   
                	   tracker.setatLeastOneInputTracked(true);
                	   Graph in =graphFactory.createChart("INPUT");
                 	   in.setName(inputPortNames.get(i).toString());
                 	   in.setCategory("INPUT");
                 	  in.setZeroTimeAdvance(showZeroTimeAdvance.isSelected());
                 	   graphs.add(in);
                 	  if(!inputUnits[i].equalsIgnoreCase(""))
                 		  in.setUnit(inputUnits[i]);
                   
                 	  else
                 		  in.setUnit("");
                    
                  
                }
                }
               tracker.settrackInputPorts(inputPorts); 
               tracker.setatLeastOneOutputTracked(false);
               for (int i = 0; i < outputPorts.length; i++)
               {
                  if(outputPorts[i])
                  {   
                	  tracker.setatLeastOneOutputTracked(true);
                	  Graph out =graphFactory.createChart("OUTPUT");
                	  out.setName(outputPortNames.get(i).toString());
                	  out.setCategory("OUTPUT");
                	  out.setZeroTimeAdvance(showZeroTimeAdvance.isSelected());
                	  graphs.add(out);
                	  if(!outputUnits[i].equalsIgnoreCase(""))
                		  out.setUnit(outputUnits[i]);
                        
                	  else
                		  out.setUnit("");
	  
                  }
                   
                 
               }
               
              tracker.settrackOutputPorts(outputPorts); 
              tracker.setGraphs(graphs);
              
               if (!tracker.getTimeViewSelected())
               {
            	 if(timeView.isSelected()||timeViewSep.isSelected())
            	 
               	tracker.setTimeViewSelected(true); 
               	    
               }
               
              
          }
      });
  	
  	trackPanel.revalidate();
    trackPanel.repaint();
	       }
	    }
	
	}
	  
	  private class MyTreeCellRenderer extends DefaultTreeCellRenderer {
		      ArrayList<DefaultMutableTreeNode> selectedNodes;
		  
		  MyTreeCellRenderer(ArrayList<DefaultMutableTreeNode> nodes) {
			  selectedNodes = nodes;
		  }
		  
		 
		 
		 
		 public Component getTreeCellRendererComponent(JTree tree,
				 Object value,
				 boolean sel,
				 boolean expanded,
				 boolean leaf,
				 int row,
				 boolean hasFocus)
		 {
	  super.getTreeCellRendererComponent(tree, value, sel,expanded, leaf, row,hasFocus);
	  for(DefaultMutableTreeNode node:selectedNodes)
	  {	 
	  if (isTrackedNode(value,node)) {
		  setBackgroundNonSelectionColor(Color.GREEN);	
		  break;
	  }
	  else
	  {
		  setBackgroundNonSelectionColor(null);
	  }
	  } 
		 return this;
	  }
	  protected boolean isTrackedNode(Object value,DefaultMutableTreeNode trackednode)
	  {   
		  DefaultMutableTreeNode node =
                  (DefaultMutableTreeNode)value;
          if (node != null)
          {
           FModel model= (FModel)node.getUserObject();
           FModel selectedModel=(FModel)trackednode.getUserObject();
           if(model.getName().equals(selectedModel.getName()))
		      return true;
	  }
          return false;
	  }
	}
	}
    private void writeString(String path, String stringToWrite)
    {
            try
            {
                FileWriter fw = new FileWriter(path);
                fw.write(stringToWrite);
                fw.close();
            }
            catch (Exception e)
            {
                System.err.println("An Error Occured While Writing: " + path);
                System.err.println(e);
            }
     }
    
    public void removeExternalWindows()
    {
    	tracking.clearWindows();
    }
    
    
    
    
}
