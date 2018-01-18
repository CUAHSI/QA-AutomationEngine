/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
/**
 * Facade Connections
 * This class display the Tracking Log
 * @modified Sungung Kim
 */

package view;


import facade.modeling.*;

//Standard API Imports
import java.awt.*;
import javax.swing.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;
import java.util.Hashtable;

public class ModelTrackingComponent
{
    public static final short HORIZONTAL_TABLE_STYLE = 0;
    public static final short VERTICAL_TABLE_STYLE   = 1;
    
    private Tracker[] modelColumn;
    private List headerRow;
    private List dataColumns;
    private JEditorPane htmlViewer;
    private StringBuffer htmlString;
    private short tableType;
    private boolean autoRefresh;
    
    public ModelTrackingComponent()
    {    
        tableType = HORIZONTAL_TABLE_STYLE;
        autoRefresh = true;        
    }
   
    public String getHTMLString()
    {
        if (tableType == HORIZONTAL_TABLE_STYLE)
            setupHorizontalTable();
        else
            setupVerticalTable();
       
        return htmlString.toString();
    }
     
    //Returns Comma deliminated String for given model
    public String getCSVString(FModel model)
    {    
        Tracker tracker  = findTrackerFor(model);
        return createCSVString(tracker.getDataHeaders(),tracker.getDataStorage());
    }
    
    public String[] getEncodedCSVString(FModel model)
    {
        int seed = 0;
        StringBuffer legend = new StringBuffer();
        
        legend.append("<HTML><BODY><B>Legend - " + model.getName() + "</B>");
        Hashtable hashtable = new Hashtable();
        Tracker tracker  = findTrackerFor(model);
        String[] headers = tracker.getDataHeaders();
        List[] dataStore = tracker.getDataStorage();
        List[] encodedDataStore = new List[dataStore.length];
        
        
        {
            encodedDataStore[0] = ViewUtils.integerEncode(dataStore[0],hashtable,seed);
            seed += 100;
            legend.append("<P><B>"+headers[0]+"</B>");
            legend.append("<TABLE BORDER=\"1\" CELLPADDING=\"5\" CELLSPACING=\"1\" ");
            legend.append("bordercolorlight=\"#C0C0C0\" bordercolordark=\"#C0C0C0\" bordercolor=\"#C0C0C0\" >");
            legend.append("<TR><TD width=\"100\"><B>Key</B></TD>");
            legend.append("<TD width=\"100\"><B>Value</B></TD></TR>");
        
            Iterator it = hashtable.keySet().iterator();
            while(it.hasNext())
            {
                 Object key = it.next();
                 legend.append("<TR><TD nowrap>" + key + "</TD>");
                 legend.append("<TD nowrap>" + hashtable.get(key) + "</TD></TR>");
            }
            hashtable.clear();
            legend.append("</TABLE>");
        }
        encodedDataStore[1] = dataStore[1];
        encodedDataStore[2] = dataStore[2];
        encodedDataStore[3] = dataStore[3];
                  
        for (int i = 4; i < dataStore.length; i++)
        {
            encodedDataStore[i] = ViewUtils.integerEncode(dataStore[i],hashtable,seed);
            seed += 100;
            legend.append("<P><B>"+headers[i]+"</B>");
            legend.append("<TABLE BORDER=\"1\" CELLPADDING=\"5\" CELLSPACING=\"1\" ");
            legend.append("bordercolorlight=\"#C0C0C0\" bordercolordark=\"#C0C0C0\" bordercolor=\"#C0C0C0\" >");
            legend.append("<TR><TD width=\"100\"><B>Key</B></TD>");
            legend.append("<TD width=\"100\"><B>Value</B></TD></TR>");

            Iterator it = hashtable.keySet().iterator();
            while(it.hasNext())
            {
                Object key = it.next();
                legend.append("<TR><TD nowrap>" + key + "</TD>");
                legend.append("<TD nowrap>" + hashtable.get(key) + "</TD></TR>");
            }
            hashtable.clear();
            legend.append("</TABLE>");
        }
        
        legend.append("</BODY></HTML>");
        
        String[] val = new String[2];
        val[0] = legend.toString();
        val[1] = createCSVString(headers,encodedDataStore);
        return val;
    }
    
    private String createCSVString(String[] headers,List[] storage)
    {    
        String delim = ",";
        String newLine = "\n";
        StringBuffer buffer = new StringBuffer();
        
        buffer.append(delim);
        for (int i = 0; i < headers.length; i++)
        {
            buffer.append(headers[i]);
            buffer.append(delim);
        }
        buffer.append(newLine);
        
        int length = headerRow.size()-1;
        for (int i = 0; i < length; i++)
        {
            buffer.append(headerRow.get(i+1));
            buffer.append(delim);
            for (int j = 0; j < storage.length; j++)
            {  
                Object obj = storage[j].get(i);
                buffer.append((obj == null) ? "" : obj.toString());
                buffer.append(delim);
            }
            buffer.append(newLine);
        }
        return buffer.toString();
    }
    
    public void loadModel(String name, Tracker [] t)
    {        
   
        modelColumn = t;
        
        dataColumns = new ArrayList();
        headerRow = new ArrayList();
        headerRow.add(" ");
        htmlViewer = new JEditorPane();
        htmlViewer.setEditable(false);
        htmlViewer.setContentType("text/html");
        
        //**********
        htmlString = new StringBuffer();
        htmlString.append("<HTML><BODY>");
        htmlString.append("<B><p align=\"center\"><font color=\"#000080\" size=\"4\">DEVS ");
        htmlString.append("Modeling &amp; Simulation <br>Tracking Environment</font></B>");
        htmlString.append("<br>Model: <B>" + name + "</B> Loaded</p>");
        htmlString.append("</BODY></HTML>");
        htmlViewer.setText(htmlString.toString());
        //**********
    }
    
    public void setTableStyle(short tableStyle)
    {
        if (tableType != tableStyle)
        {
            tableType = tableStyle;
            if (tableType == HORIZONTAL_TABLE_STYLE)
                setupHorizontalTable();
            else
                setupVerticalTable();
        }
    }    

    public void refresh()
    {
        if (tableType == HORIZONTAL_TABLE_STYLE)
            setupHorizontalTable();
         else
             setupVerticalTable();
        htmlViewer.setText(htmlString.toString());
    }
    
    public void addTrackingSet(double currentTime)
    {
        headerRow.add(Double.toString(currentTime));
        String[] nextColumn = new String[modelColumn.length];
        for (int i =0; i < modelColumn.length; i++)
        {
            nextColumn[i] = modelColumn[i].getCurrentTrackingHTMLString();            
            modelColumn[i].saveCurrentTrackingState(currentTime);
        }
        dataColumns.add(nextColumn);
       
        if (autoRefresh)
        {
            if (tableType == HORIZONTAL_TABLE_STYLE)
                setupHorizontalTable();
            else
                setupVerticalTable();
            htmlViewer.setText(htmlString.toString());
        }
    }
    
    private void setupHorizontalTable()
    {
        htmlString = new StringBuffer();
        htmlString.append("<HTML><BODY><p><TABLE BORDER=\"1\" CELLPADDING=\"5\" CELLSPACING=\"1\" ");
        htmlString.append("bordercolorlight=\"#C0C0C0\" bordercolordark=\"#C0C0C0\" bordercolor=\"#C0C0C0\" >");
        htmlString.append("<TR>");
        for (int j = 0; j < headerRow.size(); j++)
            htmlString.append("<TD nowrap><B>"+headerRow.get(j)+"</B></TD>");
        htmlString.append("</TR>");
        for (int row = 0; row < modelColumn.length; row++)
        {
            htmlString.append("<TR>");
            htmlString.append("<TD nowrap><B>"+modelColumn[row]+"</B></TD>");
            for (int column = 0; column < dataColumns.size(); column++)
                htmlString.append("<TD nowrap>"+((String[])dataColumns.get(column))[row]+"&nbsp;</TD>");
            htmlString.append("</TR>");
            
        }
        htmlString.append("</TABLE></BODY></HTML>");
    }
    
    
    private void setupVerticalTable()
    {
        htmlString = new StringBuffer();
        htmlString.append("<HTML><BODY><TABLE BORDER=\"1\" CELLPADDING=\"5\" CELLSPACING=\"0\" ");
        htmlString.append("bordercolorlight=\"#C0C0C0\" bordercolordark=\"#C0C0C0\" bordercolor=\"#C0C0C0\" >");
        htmlString.append("<TR><TD></TD>");
        for (int header = 0; header < modelColumn.length; header++)
            htmlString.append("<TD nowrap width=\"100\"><p align=\"center\"><B>"+modelColumn[header]+"</P></B></TD>");
        htmlString.append("</TR>");
        
        for (int row = 0; row < dataColumns.size(); row++)
        {
            htmlString.append("<TR>");
            htmlString.append("<TD nowrap><B>"+headerRow.get(row+1)+"</B></TD>");
            String[] currentRow = (String[])dataColumns.get(row);
            for (int column = 0; column < currentRow.length; column++)
                htmlString.append("<TD nowrap>"+currentRow[column]+"&nbsp;</TD>");
            htmlString.append("</TR>");
            
        }
        htmlString.append("</TABLE></BODY></HTML>");
    }
    
    
    
    public void customizeComponent(Component owner)
    {
        JPanel panel = new JPanel();
        panel.setBorder(BorderFactory.createTitledBorder("Table Style"));
        JRadioButton horizontal = new JRadioButton("Horizontal",tableType==HORIZONTAL_TABLE_STYLE);
        JRadioButton vertical = new JRadioButton("Vertical",tableType==VERTICAL_TABLE_STYLE);
        ButtonGroup bg = new ButtonGroup();
        bg.add(horizontal);
        bg.add(vertical);
        panel.add(horizontal);
        panel.add(vertical);
        JCheckBox autoRefreshBox = new JCheckBox("Auto-Refresh",autoRefresh);
        JPanel outer = new JPanel(new BorderLayout());
        outer.add(autoRefreshBox,BorderLayout.NORTH);
        outer.add(panel,BorderLayout.CENTER);
        
        int option = JOptionPane.showConfirmDialog(owner,outer,"Data Tracking Log Settings...", 
                                                   JOptionPane.PLAIN_MESSAGE);   
        if (option == JOptionPane.OK_OPTION)
        {
            if (horizontal.isSelected())
                setTableStyle(HORIZONTAL_TABLE_STYLE);
            else
                setTableStyle(VERTICAL_TABLE_STYLE);
            
            autoRefresh = autoRefreshBox.isSelected();
            if (autoRefresh)
                htmlViewer.setText(htmlString.toString());
        }
    }
    
    private Tracker findTrackerFor(FModel model)
    {
        Tracker t = null;
        boolean found = false;
        for (int i = 0; i < modelColumn.length && !found; i++)
        {
            if (modelColumn[i].getAttachedModel() == model)
            {
                t = modelColumn[i];
                found = true;
            } 
        }
        return t;
    }
    
    public JScrollPane retTL(){
    	return new JScrollPane(htmlViewer);
    }
    
    
    
}