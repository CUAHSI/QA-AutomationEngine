/**
 * Utility methods involving (or used by) viewable devs components.
 *
 * @author  Jeff Mather
 */

package view.modeling;

import java.awt.*;
import java.util.*;
import java.util.List;

import GenCol.*;


import model.modeling.*;


public class ViewableComponentUtil
{
    /**
     * Given a set of ports, returns a list of their names.
     *
     * @param   ports   The ports whose names are desired.
     */
    static public List getPortNames(Set ports)
    {
        // for each of the ports in the given set
        List names = new ArrayList();
        Iterator i = ports.iterator();
        while (i.hasNext()) {
            // add this port's name to the list we are building
            port port = (port)i.next();
            names.add(port.getName());
        }

        return names;
    }

    /**
     * Creates a test input structure from the given information,
     * and adds that input structure to the list of test inputs for
     * the given port.
     *
     * @param   portName    The name of the port on which to inject the value.
     * @param   value       The value to inject.
     * @param   e           The amount of simulation time to wait before
     *                      injecting the value.
     * @param   testInputs  The list of all test-inputs for a component
     *                      to which to add the test input created here.
     * @param   testInputsByPortName
     *                      The map of test-inputs to port-names to 
     *                      which to add the test input created here.
     */
    static public void addTestInput(String portName, entity value, double e,
        List testInputs, Map testInputsByPortName)
    {
        // make a new test-input object
        TestInput input = new TestInput(portName, value, e);

        // add the test-input to the given list of all test-inputs
        testInputs.add(input);

        // if there isn't already a list in the test-inputs-by-port-name
        // map for the given port
        List inputs = (List)testInputsByPortName.get(portName);
        if (inputs == null) {
            // create one
            inputs = new ArrayList();
            testInputsByPortName.put(portName, inputs);
        }

        // add the input to the list for the particular port
        inputs.add(input);
    }

    /**
     * Forms a name to use for a component in layout situations, using
     * the given component-name.
     *
     * @param   componentName       The component name to decorate to
     *                              form a name for layout purposes.
     */
    static public String buildLayoutName(String componentName)
    {
        return "\"" + componentName + "\"";
    }

    /**
     * Lays out the subcomponent cells within the given parent digraph in
     * a gridlike fashion.
     *
     * @param   numCells    The total number of cells to lay out.
     * @param   cellPrefix  The prefix that each cell's name starts with
     *                      (the cells are assumed to be named from
     *                      [cellPrefix]0 to [cellPrefix][numCells - 1].
     * @param   cellsPerRow How many cells should occupy each row of the grid.
     * @param   parent      The parent digraph containing the cells.
     * @param   columnWidth The width (in pixels) of each column in the grid.
     * @param   rowHeight   The height (in pixels) of each row in the grid.
     */
    static public void layoutCellsInGrid(int numCells, String cellPrefix,
        int cellsPerRow, digraph parent, int columnWidth, int rowHeight)
    {
        // for each cell
        for (int i = 0; i < numCells; i++) {
            // get this cell from the given parent
            ViewableComponent cell = (ViewableComponent)parent.withName(
                cellPrefix + i);

            // detm the cell's grid location (in pixels)
            final int column = i % cellsPerRow, row = i / cellsPerRow;
            Point location = new Point(10 + column * columnWidth,
                30 + row * rowHeight + column * 10);

            cell.setPreferredLocation(location);
        }
    }
}