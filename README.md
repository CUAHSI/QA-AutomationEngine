# cuahsi-qa-automation-engine

### Scope
This repository contains both general utilities for the execution of CUAHSI test suites on top of Jenkins and Selenium Grid infrastructure, as well as software system specific tools (eg. the HydroClient test suite).  Current CUAHSI software systems included in the scope of this repository are:
1. data.cuahsi.org (HydroClient)
2. hydroshare.org (HydroShare)

### Infrastructure
The test suites are designed to run within a Jenkins + Selenium Grid environment on CUAHSI-managed hardware.  Test initiation and results interpretation are handled by Jenkins.  Meanwhile, the test case execution is handled by Selenium Grid.  Both the Jenkins and Selenium Grid systems utilize parallel execution, and the parallel execution is handled independently in each system (how Jenkins jobs are allocated to executors is not related to how test cases are allocated to Selenium Grid nodes).

#### Jenkins
Each test case is given a separate job in Jenkins, which enables the easy analysis of historical test execution data for a specific test.  API calls are made to create Jenkins jobs (for any new test cases) and to run Jenkins jobs.  After setting up environment variables and pulling the GitHub repository, the "parent" Jenkins job runs the jenkins.sh file.  This shell script handles the Jenkins job creation (as needed) and the job build initiation.  For specifying which tests to run, use the software system config file (eg. hydroclient.conf)

#### Selenium Grid
The Selenium Grid system uses VMs which run on CUAHSI hardware.  The number and types of Selenium Grid nodes does not need to be established a priori.  Rather, the Selenium Grid hub allocates test cases based on what nodes are available at the time.  All Selenium Grid VMs (hub and nodes) are setup to automatically login and start the Selenium Grid Server in a JRE upon boot.  As such, turning a node VM on or off is sufficient for adding or removing it from the available node pool.  Whenever possible, test environments are setup to match real user scenarios.  With this principle in mind, the test system does not currently utilize docker environments, headless browsing, or other "more efficient" testing system approaches (the tradeoffs here can be evaluated down the road).
