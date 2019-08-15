# Self-Service Hydroshare QA Training

## Getting started

### Running the test suite

In your SSH session:
```bash
export DISPLAY=:99.0
cd ~/QA-AutomationEngine
./hydrotest hydroshare
```

In your VNC session:
1. Watch the Hydroshare test suite execute
1. When you are satisfied with the concept, _Ctrl+C_ in the SSH session to terminate the test suite execution
   1. The suite takes a long time to execute when not ran in parallel (~30 min)

## Understanding the test case layers

The test cases use a layered architecture, to keep the test suite efficient and maintainable.  Further, this layered architecture is a "closed layers" architecture - each layer only directly interacts with the layer immediately below it.  The layers are structured in order of decreasing abstraction, such that the test case defined at the top layer is succinct and appears as an almost domain-specific-language-like description of the test case, using Hydroshare-user-friendly terminology.  Consider a Hydroshare test case to simply login and logout.  We'll assert that the My Resources page is visible when logged in, but not when the user is logged out.  This example is broken down in the following sections.

### The test case layer

At this top-layer, we would have succinct, high-abstraction steps for the test to execute, as well as any test assertions.  For our example, this would involve something like `Home.login()`, `Home.logout()`, and `MyResources.goto()` for the test execution/navigations.  Lastly, we need an assertion like `MyResources.is_visible()`.  To conceptually separate the test execution from the expected state information, use a test oracle function `def oracle(expectedMyResourceVisibility):` whenever running state assertions.  Putting this all together, the test case in _hydroshare/hydroshare.py_ would look something like:

```python
def mytest(self):
    def oracle(myResourcesExpectedVisible):
        if myResourcesExpectedVisible:
            self.assertTrue(MyResources.is_visible(self.driver))
        else:
            self.assertFalse(MyResources.is_visible(self.driver))

    MyResources.goto(self.driver)
    oracle(myResourcesExpectedVisible=False)
    Home.login(self.driver)
    MyResources.goto(self.driver)
    oracle(myResourcesExpectedVisible=True)
    Home.logout(self.driver)
    MyResources.goto(self.driver)
    oracle(myResourcesExpectedVisible=False)
```

Note that we pass the self.driver object into the macro at each step - this self.driver is the actual browser session that we want the test to execute against.

### The macro layer

At this middle layer, reusable chains of actions are defined.  In drafting out the test case layer, we have already defined the macros we need.  Here are our macros, defined in _hydroshare/hs_macros.py_, for this test:

1. Home.login()
1. Home.logout()
1. MyResources.goto()
1. MyResources.is_visible()

The definition for these macros is the specific steps (clicks and other actions) needed to complete the workflow. For our example, we would have something like:

```python
class Home:
    def login(self, driver):
        HomePage.to_login.click(driver)
        LoginPage.username.inject_text(driver, username)
        LoginPage.password.inject_text(driver, password)
        LoginPage.submit.click(driver)
    def logout(self, driver):
        HomePage.to_logout.click(driver)

class MyResources:
    def to_resources(self, driver):
        HomePage.to_my_resources.click(driver)
    def is_visible(self, driver):
        MyResourcesPage.table.is_visible(driver)
```

### The elements layer

At this lowest layer, we finally define the actual HTML elements being exercised in the test.  This is "where the rubber meets the road" for the test case.  What page elements are we actually interacting with?  Element definitions should use the most maintainable, robust approach for identifying an element.  For example, an element definition by "id" is relatively robust, if the element has an id which is not repeated elsewhere in the application.  An element definition by an AND match on the classes "btn btn-centered btn-big hs-nav" would not be robust - the element definition will no longer be valid if some small styling changes are made.  The element definitions in _hydroshare/hs_elements.py_ might look like:

```python
class LoginPage:
    def __init__(self):
        self.username = SiteElement(By.ID, "id_username")
        self.password = SiteElement(By.ID, "id_password")
        self.submit = SiteElement(
            By.CSS_SELECTOR, "input[type='submit']"
        )

class HomePage:
    def __init__(self):
        self.to_login = SiteElement(By.CSS_SELECTOR, "#signin-menu a")
        self.to_logout = SiteElement(By.ID, "signout")
        self.to_my_resources = SiteElement(By.ID, "main-menu-my-resources")

class MyResourcesPage:
    def __init__(self):
        self.table = SiteElement(By.ID, "my-resources-table")
```

### See an broken-down example

Look at the following commits to see an implemented example.
1. Elements defined `git diff 06e71c 2cacaa`
1. Macros defined `git diff 2cacaa 6524bf`
1. Test case defined `git diff 6524bf a267f7`

This test case can be ran with `./hsctl hydroshare HydroshareTestSuite.test_B_000035` and viewed through the browser using the VNC session.

### Notes on design

Test case creation is not a black-and-white process.  For example, there are some judgement calls in the following:
1. Organizing the macros and elements into classes
1. Scoping macros so that they are reusabile, but long enough to be meaningful
1. Choosing element identifiers
1. Deciding what tests to add to the suite
1. Designing assertions for the test cases
1. Avoiding overlap with the macros and elements are already defined

Please use a collaborative approach with colleagues, or at least request PR reviewers.

## CI systems

1. Cut test case branches from, and merge test case branches into, the develop branch.
1. Note the badges on https://github.com/CUAHSI/QA-AutomationEngine/tree/develop.  Try to avoid dropping the Code Quality, Vulnerability, or Requirements scores.
1. Please run `./hydrotest check` before commiting contributions to ensure the code conforms to the project standards.