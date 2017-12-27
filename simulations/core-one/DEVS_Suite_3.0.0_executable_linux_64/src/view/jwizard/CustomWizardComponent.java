
package view.jwizard;

/**
 * An interface to allow the WizardPage to extract values from
 * custom (and other non-swing) components.
 * 
 * 
 *
 */
public interface CustomWizardComponent {

   /**
    * Gets the current value of the component.
    * 
    * @return The value.
    */
   public Object getValue();
}
