
package view.jwizard;

import java.util.List;

/**
 * A convenience class for implemeting parts of the WizardListener interface.
 * 
 * 
 */
public class WizardAdapter implements WizardListener {

   
   @Override
   public void onCanceled(List<WizardPage> path, WizardSettings settings) {
      // empty implementation.
   }

  
   @Override
   public void onFinished(List<WizardPage> path, WizardSettings settings) {
      // empty implementation.
   }

  
   @Override
   public void onPageChanged(WizardPage newPage, List<WizardPage> path) {
      // empty implementation.
   }

}
