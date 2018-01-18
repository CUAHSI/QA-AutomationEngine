/* 
 * Author     : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
 *  Version    : DEVSJAVA 2.7 
 *  Date       : 08-15-02 
 */ 
package view;

//Standard API Imports
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.text.*;
import java.io.*;

interface ConsoleInterface
{
   public void println(String line, AttributeSet attr);
   public void print(String line, AttributeSet attr);
}

public class ConsoleComponent extends JPanel implements ConsoleInterface
{
    public JTextPane htmlTextPane;
    private Document htmlDocument;
    
    private ConsolePrintStream out;
    private ConsolePrintStream err;
    
    private PrintStream stdOut;
    private PrintStream stdErr;
    
    public ConsoleComponent() 
    {
    	super(new BorderLayout());
    	this.setSize(200, 200);
        //super("Console",true,false,true,true);
        htmlTextPane = new JTextPane();
        htmlTextPane.setBackground(Color.black);
        htmlTextPane.setForeground(Color.white);
        htmlTextPane.setEditable(false);
        htmlDocument = htmlTextPane.getDocument();
        htmlTextPane.setVisible(true);
        
        stdOut = System.out;
        stdErr = System.err;
        
        out = new ConsolePrintStream(this);
        err = new ConsolePrintStream(this);
       // getContentPane().setLayout(new BorderLayout());
        this.add(new JScrollPane(htmlTextPane));
        //new PopupTextPaneListener(htmlTextPane);
        //restoreDefaultCustomization();
    }
    
    public void clearConsole()
    {
        try
        {
            htmlDocument.remove(0,htmlDocument.getLength());
        }
        catch(Exception e){}
    }
    
    public String getTextString()
    {
        return htmlTextPane.getText();
    }
    
    public void redirectOutAndErrStreams()
    {
        System.setOut(out);
        System.setErr(err);
    }
    
    public void restoreOutAndErrStreams()
    {
        System.setOut(stdOut);
        System.setErr(stdErr);
    }
    
    public synchronized void println(String line, AttributeSet attr)
    {
        try
        {
            htmlDocument.insertString(htmlDocument.getLength(),line+'\n',attr);
            htmlTextPane.setCaretPosition(htmlDocument.getLength());
        }
        catch (Exception e){}
    }
    
    public synchronized void print(String line, AttributeSet attr)
    {
        try
        {
            htmlDocument.insertString(htmlDocument.getLength(),line,attr);
            htmlTextPane.setCaretPosition(htmlDocument.getLength());
        }
        catch (Exception e){}
    }
    
    private class ConsolePrintStream extends PrintStream
    {
        private ConsoleInterface console;
        private MutableAttributeSet attr;
        
        public ConsolePrintStream(ConsoleInterface console, MutableAttributeSet attr)
        {
           super(new PipedOutputStream());//Just to give it something
           this.console = console;
           this.attr    = attr;
        }
        
        public ConsolePrintStream(ConsoleInterface console)
        {
           super(new PipedOutputStream());//Just to give it something
           this.console = console;
           this.attr    = new SimpleAttributeSet();
        }
         
        public MutableAttributeSet getAttributeSet()
        {
            return attr;
        }
        
        public void setAttributeSet(MutableAttributeSet attr)
        {
            this.attr = attr;
        }
        
         public boolean checkError() 
         {
            return false;
         }
         
         public void close() 
         {
         }
         
         public void flush()
         {
         }
         
         public void print(boolean x) 
         {
             console.print(""+x,attr);
         }
         
         public void print(char x) 
         {
              console.print(""+x,attr);
         }
 
         public void print(char[] x) 
         {
              console.print(""+x,attr);
         }
         public void print(double x)
         {
              console.print(""+x,attr);
         }
         
         public void print(float x)
         {
              console.print(""+x,attr);
         }
         
         public void print(int x) 
         {   
              console.print(""+x,attr);
         }
 
         public void print(long x)
         {
              console.print(""+x,attr);
         }
 
         public void print(Object x) 
         {
              console.print(""+x,attr);
         }

         public void print(String x) 
         {
              console.print(""+x,attr);
         }
         
         public void println() 
         {
              console.println("",attr);
         }
         
         public void println(boolean x) 
         {
              console.println(""+x,attr);
         }
         
         public void println(char x) 
         {
              console.println(""+x,attr);
         }
         
         public void println(char[] x) 
         {
              console.println(""+x,attr);
         }
         
         public void println(double x) 
         {
             console.println(""+x,attr);
         }
 
         public void println(float x) 
         {
             console.println(""+x,attr);
         }
         
         public void println(int x)
         {
             console.println(""+x,attr);
         }
         
         public void println(long x)
         {
             console.println(""+x,attr);
         }

         public void println(Object x)
         {
             console.println(""+x,attr);
         }
 
         public void println(String x)
         {
             console.println(""+x,attr);
         }
         
         protected void setError() 
         {
         } 
         
         public void write(byte[] buf, int off, int len)
         {
             console.println(new String(buf,off,len),attr);
         }
         
         public void write(int b)
         {
             char x = (char)b;
             console.println(""+x,attr);
         }
    }
    
    private class PopupTextPaneListener extends MouseAdapter implements ActionListener
    {
        private JTextPane textPane;
        
        public PopupTextPaneListener(JTextPane textPane)
        {
            this.textPane = textPane;
            textPane.addMouseListener(this);
        }
        
        public void mouseClicked(MouseEvent e)
        {
            if ((e.getModifiers() & e.BUTTON2_MASK) == e.BUTTON2_MASK ||
                (e.getModifiers() & e.BUTTON3_MASK) == e.BUTTON3_MASK)
            {
                JPopupMenu popup    = new JPopupMenu();
                JMenuItem copy      = new JMenuItem("Copy",'C');
                JMenuItem selectAll = new JMenuItem("Select All",'S');
                copy.setActionCommand("COPY");
                selectAll.setActionCommand("SELECT_ALL");
                copy.addActionListener(this);
                selectAll.addActionListener(this);
                copy.setEnabled(textPane.getSelectionStart() < textPane.getSelectionEnd());
                popup.add(copy);
                popup.add(selectAll);
                popup.show(textPane,e.getX(),e.getY());
            }
        }
        
        public void actionPerformed(ActionEvent e) 
        {
            if (e.getActionCommand().equalsIgnoreCase("COPY"))
                textPane.copy();
            else if (e.getActionCommand().equalsIgnoreCase("SELECT_ALL"))
                textPane.selectAll();
        }
        
    }
    private JButton createColorButton(Color initialColor, String setupTitle, Component parent)
    {
        final String sTitle   = setupTitle;
        final Component owner = parent;
        final JButton cButton = new JButton();
        cButton.setMaximumSize(new Dimension(60,16));
        cButton.setPreferredSize(new Dimension(60,16));
        cButton.setBackground(initialColor);
        cButton.setFocusPainted(false);
        cButton.addActionListener(new ActionListener()
        {
            public void actionPerformed(ActionEvent e)
            {
                Color newColor = JColorChooser.showDialog(owner,sTitle,cButton.getBackground());
                if (newColor != null)
                    cButton.setBackground(newColor);
            }
        });
        return cButton;
    }
    
    private JPanel createProxyPanel(Component c)
    {
        JPanel panel = new JPanel();
        panel.add(c);
        return panel;
    }
    
    public void customizeComponent(Component owner)
    {
        JPanel panel;
        JPanel stdoutPanel;
        JComboBox stdoutFont;
        JPanel stderrPanel;
        JComboBox stderrFont;
        JComboBox stdoutSize;
        JComboBox stderrSize;
        Integer[] sizes = {new Integer(6),new Integer(8),new Integer(10),new Integer(12),
                           new Integer(14),new Integer(18),new Integer(24),new Integer(36),
                           new Integer(42),new Integer(56),new Integer(72),new Integer(144)};
        
        final JButton bgColor;
        final JButton stdoutForegroundColor;
        final JButton stderrForegroundColor;
        String[] FONTS = {"Monospaced","Serif","SansSerif"};
        
        panel = new JPanel();
        panel.setLayout(new BoxLayout(panel,BoxLayout.Y_AXIS));
        
        JPanel bgPanel = new JPanel(new GridLayout(1,2));
        bgPanel.add(new JLabel("Background Color: "));
        bgColor = createColorButton(htmlTextPane.getBackground(),"Console Background Color...",panel);
        bgPanel.add(createProxyPanel(bgColor));
        panel.add(bgPanel);
        
        panel.add(Box.createVerticalStrut(5));
        
        stdoutPanel = new JPanel(new GridLayout(0,2));
        stdoutPanel.setBorder(BorderFactory.createTitledBorder("{StdOut} Settings"));
        stdoutForegroundColor = createColorButton(StyleConstants.getForeground(out.getAttributeSet()),
                                                  "{StdOut} Foreground Color",owner);
        stdoutPanel.add(new JLabel("Font: "));
        stdoutFont = new JComboBox(FONTS);
        stdoutFont.setSelectedItem(StyleConstants.getFontFamily(out.getAttributeSet()));
        stdoutPanel.add(stdoutFont);
        stdoutSize = new JComboBox(sizes);
        stdoutSize.setSelectedItem(new Integer(StyleConstants.getFontSize(out.getAttributeSet())));
        stdoutPanel.add(new JLabel("Font Size:"));
        stdoutPanel.add(stdoutSize);
        stdoutPanel.add(new JLabel("Color: "));
        stdoutPanel.add(createProxyPanel(stdoutForegroundColor));
        panel.add(stdoutPanel);
        
        stderrPanel = new JPanel(new GridLayout(0,2));
        stderrPanel.setBorder(BorderFactory.createTitledBorder("{StdErr} Settings"));
        stderrForegroundColor = createColorButton(Color.red,
                                                  "{StdErr} Foreground Color",owner);
        stderrPanel.add(new JLabel("Font: "));
        stderrFont = new JComboBox(FONTS);
        stderrFont.setSelectedItem(StyleConstants.getFontFamily(err.getAttributeSet()));
        stderrPanel.add(stderrFont);
        stderrSize = new JComboBox(sizes);
        stderrSize.setSelectedItem(new Integer(StyleConstants.getFontSize(err.getAttributeSet())));
        stderrPanel.add(new JLabel("Font Size:"));
        stderrPanel.add(stderrSize);
        stderrPanel.add(new JLabel("Color: "));
        stderrPanel.add(createProxyPanel(stderrForegroundColor));
        panel.add(stderrPanel);   
        
        Object[] options = { "OK", "Cancel", "Reset" };
        int option = JOptionPane.showOptionDialog(owner, panel,"Console Settings...", 
                                     JOptionPane.DEFAULT_OPTION, JOptionPane.PLAIN_MESSAGE,
                                     null, options, options[0]);
        if (option == 2)
            restoreDefaultCustomization();
        else if (option == 0)
        {
            htmlTextPane.setBackground(bgColor.getBackground());
            StyleConstants.setForeground(out.getAttributeSet(),stdoutForegroundColor.getBackground());
            StyleConstants.setForeground(err.getAttributeSet(),stderrForegroundColor.getBackground());
            StyleConstants.setFontFamily(out.getAttributeSet(),stdoutFont.getSelectedItem().toString());
            StyleConstants.setFontFamily(err.getAttributeSet(),stderrFont.getSelectedItem().toString()); 
            StyleConstants.setFontSize(out.getAttributeSet(),((Integer)stdoutSize.getSelectedItem()).intValue());
            StyleConstants.setFontSize(err.getAttributeSet(),((Integer)stderrSize.getSelectedItem()).intValue());
        }
    }
    
    //Background of Text is set to Transparent {Color(0,0,0,0)}
    public void restoreDefaultCustomization()
    {
        htmlTextPane.setBackground(Color.black);
        
        StyleConstants.setFontFamily(out.getAttributeSet(),"Monospaced");
        StyleConstants.setForeground(out.getAttributeSet(), Color.lightGray);
        StyleConstants.setBackground(out.getAttributeSet(),new Color(0,0,0,0));
        StyleConstants.setFontSize(out.getAttributeSet(),12);
        StyleConstants.setBold(out.getAttributeSet(),true);
        
        StyleConstants.setFontFamily(err.getAttributeSet(),"Monospaced");
        StyleConstants.setForeground(err.getAttributeSet(), Color.red);
        StyleConstants.setBackground(err.getAttributeSet(), new Color(0,0,0,0));
        StyleConstants.setFontSize(err.getAttributeSet(),12);
        StyleConstants.setBold(err.getAttributeSet(),true);
    }
}
