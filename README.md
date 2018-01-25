# cuahsi-qa-automation-engine

### Scope
This repository contains general utilities for the execution of CUAHSI test suites on top of Jenkins and Selenium Grid infrastructure, as well as software system specific tools (eg. the HydroClient test suite).  Current CUAHSI software systems included in the scope of this repository are:
1. data.cuahsi.org (HydroClient)
2. hydroshare.org (HydroShare)

### Infrastructure
The test suites are designed to run within a Jenkins + Selenium Grid environment on CUAHSI-managed hardware.  Test initiation and results interpretation are handled by Jenkins.  Meanwhile, the test case execution is handled by Selenium Grid.  

#### Jenkins
The test suite execution process begins with a trigger of the "core" Jenkins job.  After setting up environment variables and pulling the GitHub repository, the core Jenkins job runs the jenkins.sh file.  This script uses API calls to create Jenkins jobs (for any new test cases) and to run Jenkins jobs.  Each test case is given a separate job in Jenkins, which enables the easy analysis of historical test execution data for a specific test.  For specifying which tests to run, use the software system config file (eg. hydroclient.conf)

#### Selenium Grid
The Selenium Grid system uses VMs which run on CUAHSI hardware.  The number and types of Selenium Grid nodes does not need to be established a priori.  Rather, the Selenium Grid hub allocates test cases based on what nodes are available at the time.

### Usage
The test suite can ran without the Jenkins and Selenium Grid infrastructure for test script development and test suite debugging purposes.  To run all test cases (not just those defined in the configuration file):
```bash
python3 hydroclient.py
```
Specific tests can be ran by including the class and method names, for example:
```bash
python3 hydroclient.py HydroclientTestCase.test_A_000001
```
