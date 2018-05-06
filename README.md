# QA Automation Engine

> Automated test suites for multiple CUAHSI software systems, along with associated tools and infrastructure

This repository contains:

1. Selenium-based automated test suites for the CUAHSI [HydroClient](http://data.cuahsi.org) and [HydroShare](http://hydroshare.org) systems.
2. An automated testing framework to support the rapid development of high readability and high maintainability test cases.
3. Scripts to support execution of the automated test suites on Jenkins and Selenium Grid installations.
4. A simulation to characterize and communicate the parallel test execution process.
5. Additional documentation to explain the theory and purpose of the testing system.

The test suites are designed to run within a [Jenkins](https://jenkins.io/) plus [Selenium Grid](http://www.seleniumhq.org/) environment on CUAHSI-managed hardware.  Test initiation and results interpretation are handled by Jenkins.  Meanwhile, the test case execution is handled by Selenium Grid.  

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Creating Test Cases](#creating-test-cases)
- [Maintainers](#maintainers)
- [Contribute](#contribute)
- [License](#license)

## Background

### Jenkins
The test suite execution process begins with a trigger of the "core" Jenkins job.  After setting up environment variables and pulling the GitHub repository, the core Jenkins job runs the jenkins.sh file.  This script uses API calls to create (for any new test cases) and run Jenkins jobs.  Each test case is given a separate job in Jenkins, which makes it easy to analyze historical test execution data for a specific test.  

### Selenium Grid
The Selenium Grid system uses VMs which run on CUAHSI hardware.  The number and types of Selenium Grid nodes does not need to be established a priori.  Rather, the Selenium Grid hub allocates test cases based on what nodes are available at the time.

## Install

### Infrastructure
On the infrastructure side, this project uses Jenkins and Selenium Grid. Please refer to the [Jenkins installation guide](https://wiki.jenkins.io/display/JENKINS/Installing+Jenkins+on+Ubuntu) and [Selenium Grid installation guide](https://github.com/SeleniumHQ/selenium/wiki/Grid2) for instructions on how to install these tools.

### Python Packages
Installation of necessary Python packages can be accomplished with with:
```
$ pip3 install -r requirements.txt
```

### Browser Driver
A browser driver must be downloaded into a system directory.  Further, this system directory must be included in the PATH environment variable.  For the Firefox browser, the [Gecko driver](https://github.com/mozilla/geckodriver/releases) should be downloaded.


## Usage

### Test Execution
The test suite can run without the Jenkins and Selenium Grid infrastructure for test script development and test suite debugging purposes.  To run all test cases (not just those defined in the configuration file):
```
$ python3 hydroclient.py
```
Specific tests can be executed by including the class and method names, for example:
```
$ python3 hydroclient.py HydroclientTestSuite.test_A_000002
```
When initiating a Selenium Grid execution, provide the IP of the Selenium Grid hub as an argument.  The port is assumed to be the Selenium Grid default of 4444.
```
$ python3 hydroclient.py --grid 127.0.0.1
$ python3 hydroclient.py HydroclientTestSuite.test_A_000002 --grid 127.0.0.1
```
To select a browser for test execution, provide a browser name as an argument. Current choices are 'firefox', 'chrome' and 'safari' (w/o quotes). Default is 'firefox'.
```
$ python3 hydroclient.py --browser chrome
$ python3 hydroclient.py --browser safari HydroclientTestSuite.test_A_000002
```

### Jenkins Deployments
In a Jenkins deployment, the core job should run the jenkins.sh script:
```
$ bash jenkins.sh
```
The Jenkins template project runs a parameterized version of the previously mentioned python3 commands.
```
$ python3 hydroclient.py HydroclientTestSuite.test_A_000002 --grid 127.0.0.1
```
To specify which tests to run, edit the software system config file:
1) hydroclient.conf
2) hydroshare.conf

### Flake8 Compliance
To confirm Flake8 compliance, use:
```
$ make check
```

### Combinatorial Design of Experiments
Calls to the [combinatorial design of experiments utility](doe/combinatorial-doe/combinatorial.py) requires a specification of the number of experiments to generate (--experiments), the number of factors for the combinatorial design (--factors), and the number of possible values for each independent variable (--specification).  For example, consider the following design of experiments problem:
1) Pairwise (2-way) combinatorial approach
2) One independent variable has three possible values, while three independent variables have two possible values
3) Desired number of experiments is eight (six is the feasible minimum, but specifying the minimum may result in a long solution convergence time)
This problem could be solved with the following call:
```
$ python3 combinatorial.py --experiments 8 --factors 2 --specification 3 2 2 2
```
Note: This utility is for very simple DOE-based test case generation only.  Further, the number of experiments should be well above the feasible minimum in order to generate a solution quickly.  The brute force approach quickly becomes impractical for large and close-to-optimal DOE problems.

### Test Assets Generation
CUAHSI software systems sometimes require test files in order verify and validate the system.  The utilities to automatically generate these files are deliberately independent from the automated testing system.  This enables not only the automated test system to use these utilities, but also the greater team at large.  The [assets](assets) folder contains the test file generation utilities.

For HydroServer test files generation, a few environment variables must be defined:
1) GENSERVER is the Azure SQL database server name
2) GENDB is the database name
3) GENUSER is the username for SQL server access - the account must have the authorization to run ad hoc SELECT queries
4) GENPASSWD is the password for SQL server access

Then, the user must specify the number of data value sets, methods, sites, sources, and variables.  An example script call is provided below.
```
$ python3 gen_all.py --sets 3 --methods 4 --sites 5 --sources 6 --variables 7
```
As one would expect, this generates a methods.csv file with 4 records, a sites.csv file with 5 records, a sources.csv file with 6 records, and a variables.csv file with 7 records.  The number of data value records will typically far exceed the number of records for the metadata csv files previously described.  As a result of this size, the data value records must sometimes be uploaded in chunks (multiple files).  The "sets" argument dictates how many data value files are generated, with each file having 250k records.  This number of records per file strikes a good balance between upload speed and upload size.

## Creating Test Cases

The [PDF documentation](documentation/beta-release/CUAHSIAutomatedTestingEngineBeta.pdf) contained in this repository provides a deeper explanation of the test suite framework.  However, the general idea is to write test cases at the most abstract level, then support that with new classes, attributes, and methods in the lower abstraction levels as needed.

In the case of the HydroClient software system, test cases should be created in hydroclient.py.  Consider a test case which involves running a map search, filtering by data service, then exporting to the workspace.  The top level test case script in [hydroclient.py](hydroclient.py) would likely only need four lines - one for each of the three steps above and one assert statement to confirm expected test results.  This test case is supported at the lower levels by (in decreasing levels of abstraction):

1) [HydroClient macros](hc_macros.py), which captures common series of actions while working with HydroClient.  In our example, the map search step would be defined here and would include clicking the location search box, clearing the box of any existing text, injecting the desired text, then clicking the location search button.
2) [HydroClient elements](hc_elements.py), which contains attributes and methods for specific element identification on the page.  In our example, the location search field and the location search button would both be defined at this level.
3) [Site elements](site_elements.py) handles all the low level interactions with off-the-shelf Selenium.  In our example, the click, clear_all_text, and inject_text methods would be defined at this level.  These methods may involve a large number of Selenium commands and should use best practices in simulating real user behavior.  For instance, non-CUAHSI test scripts commonly inject large strings of text into fields instantaneously - the inject_text method within [site_elements.py](site_elements.py) has a small pause between simulated key presses to better mimic real user behavior.  The site elements module is common to all CUAHSI automated testing suites.

The [utilities](utils.py) are also common to all CUAHSI test suites.  These utilities support those rare actions which do not involve page element interaction, and therefore cannot be handled through the framework above.

## Maintainers

[@cuahsi](https://github.com/cuahsi).
[@hydroshare](https://github.com/hydroshare).
[@ndebuhr](https://github.com/ndebuhr).

## Contribute

Please feel free to contribute.  [Open an issue](https://github.com/ndebuhr/cuahsi-qa-automation-engine/issues/new) or submit PRs.

## License

The CUAHSI QA Automation Engine is released under the BSD 2-Clause License.

©2018 CUAHSI. This material is based upon work supported by the National Science Foundation (NSF) under awards 1148453 and 1148090. Any opinions, findings, conclusions, or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the NSF.
