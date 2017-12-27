/*
 * Stephen Wilhelm
 * CSE 561 Homework 4
 */

package SimpArcMod;

import java.util.LinkedList;
import GenCol.Pair;
import GenCol.entity;
import model.modeling.message;
import view.modeling.ViewableAtomic;

/**
 * The HW4 model models a phone as per the specification given.
 *
 * Some assumptions have been made during development.  The first is that an
 * Interrupt phase needs to be added to account for the 0.1 time spent handling
 * an incoming call while in the Active phase.  The second is that the input
 * needs to provide the call duration, otherwise the model can't know when a
 * call should end.  I provide for that by making the input a Pair whose key is
 * the call identifier and whose value is the duration of the call.
 */
public class HW4 extends ViewableAtomic
{
    // Ports
    private static final String ON_OFF = "OnOff";
    private static final String INCOMING_VOICE = "incomingVoice";
    private static final String OUTGOING_VOICE = "outgoingVoice";

    // States
    private static final String ON = "On";
    private static final String OFF = "Off";
    private static final String SEARCHING = "SearchingForService";
    private static final String ACTIVE = "Active";
    private static final String READY = "Ready";
    private static final String INTERRUPT = "Interrupt";

    // Events
    private static final String START = "start";
    private static final String STOP = "stop";

    // A queue containing calls that interrupt the current call
    private final LinkedList<Pair> queue;

    // The current call.  The key is the caller in the range "a1".."z1".
    // The value is the call duration.
    private Pair currentCall = null;

    // Whether or not service is found.
    private boolean service = true;

    /**
     * Create the model.
     */
    public HW4()
    {
        this("HW4");
    }

    /**
     * Create the model.
     *
     * @param  name  The model name.
     */
    public HW4(String name)
    {
        super(name);

        queue = new LinkedList<Pair>();
        addInport(ON_OFF);
        addInport(INCOMING_VOICE);
        addOutport(OUTGOING_VOICE);

        addTestInput(ON_OFF, new entity(START));
        addTestInput(ON_OFF, new entity(STOP));
        addTestInput(INCOMING_VOICE, new Pair("a1", 10.0));
        addTestInput(INCOMING_VOICE, new Pair("d1", 13.7), 5.3);
    }

    /**
     * Initialize the model to the Off state.
     */
    @Override
    public void initialize()
    {
        holdIn(OFF, Double.POSITIVE_INFINITY);
        super.initialize();
    }

    /**
     * The external transition function.
     *
     * @param  msg  The input we need to handle.
     */
    @Override
    public void deltext(double e, message msg)
    {
        Continue(e);

        for (int i = 0; i < msg.getLength(); i++)
        {
            if (messageOnPort(msg, ON_OFF, i))
            {
                entity val = msg.getValOnPort(ON_OFF, i);

                if (val.eq(STOP))
                {
                    queue.clear();
                    currentCall = null;
                    holdIn(OFF, Double.POSITIVE_INFINITY);
                }
                else if (val.eq(START) && phaseIs(OFF))
                {
                    holdIn(ON, 0.0);
                }
            }
            else if (messageOnPort(msg, INCOMING_VOICE, i))
            {
                entity val = msg.getValOnPort(INCOMING_VOICE, i);

                if (val instanceof Pair && validCall((Pair) val))
                {
                    Pair call = (Pair) val;

                    if (phaseIs(READY))
                    {
                        currentCall = call;
                        holdIn(ACTIVE,(Double)( call.value));
                    }
                    else if (phaseIs(ACTIVE))
                    {
                        Double duration = (Double) currentCall.value;
                        queue.addFirst(call);
                        currentCall.value = duration - e;
                        holdIn(INTERRUPT, 0.1);
                    }
                }
                else
                {
                    System.err.println("Invalid value on " +
                                       INCOMING_VOICE +
                                       ": " + val);
                }
            }
        }
    }

    /**
     * The internal transition function.
     */
    @Override
    public void deltint()
    {
        if (phaseIs(ON))
        {
            holdIn(SEARCHING, 2.0);
        }
        else if (phaseIs(SEARCHING))
        {
            if (findService())
            {
                holdIn(READY, Double.POSITIVE_INFINITY);
            }
            else
            {
                holdIn(ON, Double.POSITIVE_INFINITY);
            }
        }
        else if (phaseIs(ACTIVE))
        {
            // If the queue isn't empty, then one or more calls interrupted
            // this one, so we need to answer them in order.

            if (queue.size() > 0)
            {
                currentCall = queue.removeLast();
                holdIn(ACTIVE, (Double) currentCall.value);
            }
            else
            {
                currentCall = null;
                holdIn(READY, Double.POSITIVE_INFINITY);
            }
        }
        else if (phaseIs(INTERRUPT))
        {
            // Use max() to ensure we never wait for a negative amount of time.
            double duration = (Double) currentCall.value;
            holdIn(ACTIVE, Math.max(duration,  0.0));
        }
    }

    /**
     * Generate output.
     *
     * @return  If the phase is active, then the outgoing voice response is
     *          returned; otherwise an empty message is returned.
     */
    @Override
    public message out()
    {
        message msg = new message();

        if (phaseIs(ACTIVE))
        {
            msg.add(makeContent(OUTGOING_VOICE, respond()));
        }

        return msg;
    }

    /**
     * Test to see if the pair describes a valid phone call.  A valid phone
     * call will have a key in the range "a1".."z1" and a positive double
     * value.
     *
     * @param  pair  The pair holding the caller and the duration.
     * @return  A true if the pair represents a valid phone call.
     */
    private boolean validCall(Pair pair)
    {
        if (pair.key instanceof String &&
            pair.value instanceof Double &&
            pair.key != null &&
            pair.value != null)
        {
            String caller = (String) pair.key;
            double duration = (Double) pair.value;

            return (caller.length() == 2 &&
                    caller.charAt(0) >= 'a' &&
                    caller.charAt(0) <= 'z' &&
                    caller.charAt(1) == '1' &&
                    duration > 0.0);
        }
        else
        {
            return false;
        }
    }

    /**
     * Get the output for responding to a phone call.  The response for the
     * call "a1" is "A2", "b1" is "B2", and so on.
     *
     * @return  The output entity for responding to a phone call.
     */
    private entity respond()
    {
        // Output is the caller value converted to upper case.
        String caller = currentCall.key.toString();
        char[] response = new char[2];
        response[0] = Character.toUpperCase(caller.charAt(0));
        response[1] = '2';
        return new entity(new String(response));
    }

    /**
     * Attempt to find service.  This is implemented as a toggle between
     * success and failure.
     *
     * @return  A true if service is found, otherwise a false.
     */
    private boolean findService()
    {
        boolean s = service;
        service = !service;
        return s;
    }
}
