/* 
 * 
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
/**
 * FModelView: Display the tree structure of the model and the information
 * @modified Sungung Kim 
 */

package view;

import facade.modeling.*;

//Collections Connections

//Standard API Imports
import java.awt.*;
import java.awt.event.*;

import javax.swing.*;
import javax.swing.event.*;
import javax.swing.tree.*;
import javax.swing.text.*;

import GenCol.entity;




import controller.ControllerInterface;

import view.simView.SimView;


import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;

public class FModelView extends JPanel
{
    private DefaultMutableTreeNode root;
    private JTree tree;
    private JTextPane modelDetailArea;
    private Document  modelDetailDoc;
    private TrackingControl tracking;
    private ControllerInterface controller;
    private MutableAttributeSet headerAttr;
    private MutableAttributeSet textAttr;    
    
    //Needed global variables for Injecting Input Dialog
    private String selectedPort;
    private boolean[] selectedInput;
    private JPanel Options;
    
    
    public FModelView(ControllerInterface controller, TrackingControl tracking) 
    {
        super(new BorderLayout());
        setBorder(BorderFactory.createTitledBorder("Model Viewer"));
        this.tracking = tracking;
        this.controller = controller;
    }
    
    public void loadModel(FModel rootModel)
    {
        removeAll();
        UniversalListener listener = new UniversalListener();
        setupAttributeSets();
        
        if (rootModel instanceof FAtomicModel)
            root = new DefaultMutableTreeNode(rootModel,false);
        else if (rootModel instanceof FCoupledModel)
            root = createCoupledNode((FCoupledModel)rootModel);
        //else error        
        
        tree = new JTree(root);
        
        tree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);
        tree.addTreeSelectionListener(listener);
       
        modelDetailArea = new JTextPane();
        modelDetailArea.setBackground(new Color(204,204,204));
        modelDetailArea.setEditable(false);
        modelDetailDoc  = modelDetailArea.getDocument();
        
        JButton testInput = new JButton("Inject Input");
        testInput.addActionListener(listener);
        testInput.setActionCommand("INJECT");
	
        
        
       
       
        
        Options = new JPanel(new GridLayout(2,1));      
        
        JPanel inset = new JPanel(new GridLayout(1,2));
        inset.add(testInput);
             
       
        //Setup some initial stuff
        writeModelInfo("TL:\nTN:\nPhase:\nSigma:\nInput Ports:\nOutputPorts:\n",headerAttr);        
        
        JSplitPane splitPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
	 				     new JScrollPane(tree),new JScrollPane(modelDetailArea));
        splitPane.setDividerLocation(150);
        splitPane.setOneTouchExpandable(true);
        add(splitPane,BorderLayout.CENTER);
        Options.add(inset);
        
        //Option to show coupling or not
        JCheckBox checkBox = new JCheckBox("always show couplings", SimView.alwaysShowCouplings);
        checkBox.setFont(new Font("SansSerif", Font.BOLD, 12));        
        // when the always-show-couplings checkbox is clicked
        checkBox.addItemListener(new ItemListener() {
        	public void itemStateChanged(ItemEvent e) {
        		SimView.alwaysShowCouplings =
        			(e.getStateChange() == ItemEvent.SELECTED);
        			SimView.modelView.repaint();
        	}
        });
        checkBox.setHorizontalAlignment(SwingConstants.CENTER);
        
        if(!View.isSimView)
        	checkBox.setEnabled(false);
        
        Options.add(checkBox);        
        add(Options,BorderLayout.SOUTH);
        
        this.revalidate();
        this.repaint();
    }
    
    public void synchronizeView()
    {
        if (tree != null)
        {
            DefaultMutableTreeNode node = (DefaultMutableTreeNode)tree.getLastSelectedPathComponent();
            if (node != null)
                setDetails((FModel)node.getUserObject());
        }
    }
   
    private void setupAttributeSets()
    {
        headerAttr = new SimpleAttributeSet();
        textAttr   = new SimpleAttributeSet();
        
        StyleConstants.setFontFamily(headerAttr,"Monospaced");
        StyleConstants.setForeground(headerAttr, Color.black);
        StyleConstants.setFontSize(headerAttr,12);
        StyleConstants.setBold(headerAttr,true);
        
        StyleConstants.setFontFamily(textAttr,"Monospaced");
        StyleConstants.setForeground(textAttr, new Color(0,0,128));
        StyleConstants.setFontSize(textAttr,12);
    }
    
    private void writeModelInfo(String line, AttributeSet attr)
    {
        try
        {
            modelDetailDoc.insertString(modelDetailDoc.getLength(),line,attr);
        }
        catch (Exception e){}
    }
    
    private void setDetails(FModel model)
    {
        Iterator it;
        
        try
        {
            modelDetailDoc.remove(0,modelDetailDoc.getLength());
        }
        catch (Exception e){}
        
        writeModelInfo("TL: ",headerAttr);
        writeModelInfo(model.getTimeOfLastEvent()+"\n",textAttr);
        writeModelInfo("TN: ",headerAttr);
        writeModelInfo(model.getTimeOfNextEvent()+"\n",textAttr);
        
        if (model instanceof FAtomicModel)
        {
            FAtomicModel atomic = (FAtomicModel)model;
            writeModelInfo("Phase: ",headerAttr);
            writeModelInfo(atomic.getPhase()+"\n",textAttr);
            writeModelInfo("Sigma: ",headerAttr);
            writeModelInfo(atomic.getSigma()+"\n",textAttr);
        }
        
        writeModelInfo("Input Ports:\n",headerAttr);
        
        it = sort(model.getInputPortNames()).iterator();
        while (it.hasNext())
            writeModelInfo("{"+it.next()+"} ",textAttr);
        writeModelInfo("\n",textAttr);
        
        writeModelInfo("Output Ports:\n",headerAttr);
        it = sort(model.getOutputPortNames()).iterator();
        while (it.hasNext())
            writeModelInfo("{"+it.next()+"} ",textAttr);
    }
    
    private List sort(List list)
    {
        List sortedList = new ArrayList(list.size());
        boolean finished = false;
        while (!finished)
        {
            if (list.isEmpty())
                finished = true;
            else
            {
                int loc = 0;
                Object next = list.get(0);
                for (int i = 1; i < list.size(); i++)
                    if (next.toString().compareTo((String)list.get(i)) > 0)
                    {
                        next = list.get(i);
                        loc = i;
                    }

                sortedList.add(next);
                list.remove(loc);
            }
        }
        
        return sortedList;
    }
    
    private void showInjectInput(FModel m)
    {
        final FModel model = m;
        selectedPort = null;
        
        JPanel portNamePanel = new JPanel();
        portNamePanel.setLayout(new BoxLayout(portNamePanel,BoxLayout.Y_AXIS));
        portNamePanel.setBorder(BorderFactory.createTitledBorder("Input Ports"));
        
        
        final JPanel injectPanel = new JPanel();
        injectPanel.setLayout(new BoxLayout(injectPanel,BoxLayout.Y_AXIS));
        injectPanel.setBorder(BorderFactory.createTitledBorder("Test Values"));
        injectPanel.setPreferredSize(new Dimension(200,200));
        Iterator it = model.getInputPortNames().iterator();
        ButtonGroup portNameGroup = new ButtonGroup();
        
        while (it.hasNext())
        {
            JRadioButton port = new JRadioButton((String)it.next());
            portNameGroup.add(port);
            portNamePanel.add(port);
            port.addActionListener(new ActionListener()
            {
                 public void actionPerformed(ActionEvent e) 
                 {
                     selectedPort = ((JRadioButton)e.getSource()).getText();
                     List testInputs = model.getInputPortTestValues(selectedPort);
                     selectedInput   = new boolean [testInputs.size()];
                     injectPanel.removeAll();
                     for (int i = 0; i < testInputs.size(); i++)
                     {
                         String inputName = testInputs.get(i).toString();
                         if (inputName.length() == 0)
                             inputName = "<unnamed entity "+(i+1)+">";
                         JCheckBox cBox = new JCheckBox(inputName);
                         cBox.setName(Double.toString(i));
                         injectPanel.add(cBox);
                         selectedInput[i] = false;
                         cBox.addActionListener(new ActionListener()
                         {
                             public void actionPerformed(ActionEvent e)
                             {
                                 JCheckBox source = (JCheckBox)e.getSource();
                                 int selected = (int)Double.parseDouble(source.getName());
                                 selectedInput[selected] = source.isSelected();
                             }
                            
                         });
                     }
                     injectPanel.revalidate();
                     injectPanel.repaint();
                 }
            });
        }
        
        
        portNamePanel.setPreferredSize(new Dimension(100,-1));
        JPanel panel = new JPanel(new BorderLayout());
        panel.add(portNamePanel,BorderLayout.WEST);
        panel.add(injectPanel,BorderLayout.CENTER);
        
        int ok = JOptionPane.showConfirmDialog(View.PARENT_FRAME,panel,"Inject Test Values...",
                                               JOptionPane.OK_CANCEL_OPTION);
        
        if (ok == JOptionPane.OK_OPTION && selectedPort != null)
        {
            List list = model.getInputPortTestValues(selectedPort);
            for (int i = 0; i < selectedInput.length; i++)
            {
                if (selectedInput[i])
                    controller.injectInputGesture(model, selectedPort,(entity)list.get(i));
            }
        }
    }
    
    private DefaultMutableTreeNode createCoupledNode(FCoupledModel model)
    {
        DefaultMutableTreeNode node = new DefaultMutableTreeNode(model,true);
        Iterator children = model.getChildren().iterator();
        while (children.hasNext())
        {
            FModel next = (FModel)children.next();
            if (next instanceof FAtomicModel)
                node.add(new DefaultMutableTreeNode(next,false));
            else if (next instanceof FCoupledModel)
                node.add(createCoupledNode((FCoupledModel) next));
            //else error
        }
        return node;
    }
    
    private class UniversalListener implements TreeSelectionListener, ActionListener
    {
        public void valueChanged(TreeSelectionEvent e) 
        {
            DefaultMutableTreeNode node = (DefaultMutableTreeNode)tree.getLastSelectedPathComponent();
             if (node != null)
                 setDetails((FModel)node.getUserObject());
        }
        
        public void actionPerformed(ActionEvent e) 
        {
            DefaultMutableTreeNode node = (DefaultMutableTreeNode)tree.getLastSelectedPathComponent();
            if (node != null)
            {
                String actionCmd = e.getActionCommand();
                if (actionCmd.equalsIgnoreCase("INJECT"))
                    showInjectInput((FModel)node.getUserObject());
                
            }
        }
    }
    
    public FModel getSelectedModel()
    {
        DefaultMutableTreeNode node = (DefaultMutableTreeNode)tree.getLastSelectedPathComponent();
        if (node == null)
            return null;
        else
            return (FModel)node.getUserObject();
    }
    
    public DefaultMutableTreeNode  getJTreeModel()
    {
    	return root;
    }
    
    public TrackingControl getTrackingControl()
    {
    	return tracking;
    }
}
