
package view.jwizard;

import java.util.List;



public interface WizardListener {

   /**
    * Invoked when the wizard changes to display a new page.
    * 
    * @param newPage  The new page displayed.
    * @param path The list of WizardPages shown so far.
    */
   public void onPageChanged(WizardPage newPage, List<WizardPage> path);
   
   /**
    * Invoked when the user clicks the Finish button.
    * 
    * @param path The list of WizardPages shown so far.
    * @param settings The collection of settings gleaned during the wizard.
    */
   public void onFinished(List<WizardPage> path, WizardSettings settings);
   
   /**
    * Invoked when the user clicks the Cancel button.
    * 
    * @param path The list of WizardPages shown so far.
    * @param settings The collection of settings gleaned during the wizard.
    */
   public void onCanceled(List<WizardPage> path, WizardSettings settings);
}
