package view;

import java.awt.BorderLayout;
import javax.swing.*;

public class ExternalTimeView implements Runnable
{
	private JFrame frame;
	private String name;
	private JScrollPane TG;
	public ExternalTimeView(String _name, JScrollPane _TG)
	{
		name=_name;
		TG=_TG;
	}
	public void run()
	{
    	frame=new JFrame(name);
    	frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
    	JComponent newContentPane = new JPanel(new BorderLayout());
    	newContentPane.add(TG, BorderLayout.CENTER);
    	newContentPane.setOpaque(true); //content panes must be opaque
    	frame.setContentPane(newContentPane);
    	frame.pack();
    	frame.setVisible(true);
	}
	public void dispose()
	{
		frame.dispose();
	}
}
