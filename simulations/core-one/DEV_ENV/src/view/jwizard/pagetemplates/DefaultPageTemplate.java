/**
 * Copyright 2008  Eugene Creswick
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *    http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package view.jwizard.pagetemplates;

import java.awt.CardLayout;


import view.jwizard.WizardPage;


 
public class DefaultPageTemplate extends PageTemplate {
   
   /**
    * Commons logging log instance
    */
  
   
   private final CardLayout _layout = new CardLayout();
   
   public DefaultPageTemplate(){
      this.setLayout(_layout);
   }
   
  
   public void setPage(final WizardPage page){
     
      // remove the page, just in case it was added before:
      remove(page);
      validate();
      
      add(page, page.getId());
      _layout.show(this, page.getId());
   }
}
