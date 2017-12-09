# cuahsi-qa-automation-engine

### Scope
Suite of automated tests for:
1. data.cuahsi.org (HydroClient)
2. hydroshare.org (HydroShare)

### Configuration
Test cases can be either in-development/incomplete (tag TODO), ready/done (tag DONE), or ignored (no tag).  Only the test cases marked "DONE" will be ran during test suite execution.  To make an adjustment to the test suite configuration for execution:
1. Run the config-in.py script - this will update the configuration file (config.org) to the test cases scripted in the hydroclient.py and hydroshare.py files
2. Manipulate the config.org file as needed to specify the desired subset of the test suite to be ran.
3. Run the config-out.py script - this will update the hydroclient.py and hydroshare.py scripts based on the configuration detailed in config.org

### Running the Test Suite
After configuration, the test suites are ran by executing hydroshare.py and hydroclient.py.  A subset or the full test suite will be ran, based on the config.org file specification (don't forget to run config-out.py to commit the configuration changes).