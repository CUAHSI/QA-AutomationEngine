
/**
 * A label that displays what's contained in a content object.
 *
 * @author      Jeff Mather
 */ 

package view.modeling;

import java.awt.*;
import javax.swing.*;

import model.modeling.*;

import java.text.DecimalFormat;
import util.*;

public class ContentView extends JLabel
{
    /**
     * The content this view is displaying.
     */
    protected content content;

    /**
     * The foreground color of this view's label.
     */
    static protected Color foreground = new Color(102, 102, 153);

    /**
     * The font of this view's label.
     */
    static protected Font font =   new Font("SansSerif", Font.PLAIN, 10);

    /**
     * Constructs a view on the given content.
     *
     * @param   content        The content to be viewed.
     */
    public ContentView(content content_)
    {
        content = content_;

        // define this view's look
        setOpaque(true);
        setForeground(foreground);
        setBackground(Color.white);
        setFont(font);
        setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(Color.black, 1),
            BorderFactory.createEmptyBorder(0, 2, 0, 2)));

        // try to convert the content's value to a double; if it can
        // be converted, format the double nicely;
        // otherwise the value will be displayed as is
        final String header = "<html><body bgcolor=#FFFFFF style=\"font-size:12pt; font-family:'sans-serif'\">";
        String value = content.getValue().toString();
        try {
            double numericValue = Double.parseDouble(value);
            value = (new DecimalFormat("0.000")).format(numericValue);
        } catch (NumberFormatException e) {}

        // have this view display the content's value
        setText(header + value);
    }

    /**
     * Return's the content this view is displaying.
     */
    public content getContent() {return content;}
}