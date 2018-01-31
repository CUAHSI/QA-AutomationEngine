# CUAHSI QA Automation Engine

> Automated test suites for multiple CUAHSI software systems, along with associated tools and infrastructure

This repository contains:

1. Selenium-based automated test suites for the CUAHSI [HydroClient](http://data.cuahsi.org) and [HydroShare](http://hydroshare.org) systems.
2. An automated testing framework to support the rapid development of high readability and high maintainability test cases.
3. Scripts to support the execution of the automated test suites on Jenkins and Selenium Grid installations.
4. A simulation to characterize and communicate the parallel test execution process.
5. Additional documentation to explain the theory and purpose of the testing system.

The test suites are designed to run within a [Jenkins](https://jenkins.io/) plus [Selenium Grid](http://www.seleniumhq.org/) environment on CUAHSI-managed hardware.  Test initiation and results interpretation are handled by Jenkins.  Meanwhile, the test case execution is handled by Selenium Grid.  

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contribute](#contribute)
- [License](#license)

## Background

### Jenkins
The test suite execution process begins with a trigger of the "core" Jenkins job.  After setting up environment variables and pulling the GitHub repository, the core Jenkins job runs the jenkins.sh file.  This script uses API calls to create Jenkins jobs (for any new test cases) and to run Jenkins jobs.  Each test case is given a separate job in Jenkins, which enables the easy analysis of historical test execution data for a specific test.  

### Selenium Grid
The Selenium Grid system uses VMs which run on CUAHSI hardware.  The number and types of Selenium Grid nodes does not need to be established a priori.  Rather, the Selenium Grid hub allocates test cases based on what nodes are available at the time.

## Install

On the infrastructure side, this project uses Jenkins and Selenium Grid. Please refer to the [Jenkins installation guide](https://wiki.jenkins.io/display/JENKINS/Installing+Jenkins+on+Ubuntu) and [Selenium Grid installation guide](https://github.com/SeleniumHQ/selenium/wiki/Grid2) for the installation of these tools.

The test suites and associated framework are dependent on the unittest, argparse, sys, time, and selenium Python packages.  Further, the python3 version of these packages are required.  As needed, install the Python packages with:
```sh
$ pip3 install unittest
$ pip3 install argparse
$ pip3 install sys
$ pip3 install time
$ pip3 install selenium
```

## Usage

The test suite can ran without the Jenkins and Selenium Grid infrastructure for test script development and test suite debugging purposes.  To run all test cases (not just those defined in the configuration file):
```sh
$ python3 hydroclient.py
```
Specific tests can be ran by including the class and method names, for example:
```sh
$ python3 hydroclient.py HydroclientTestCase.test_A_000002
```
When initiating a Selenium Grid execution, provide the IP of the Selenium Grid hub as an argument.  The port is assumed to be the Selenium Grid default of 4444.
```sh
$ python3 hydroclient.py --grid 127.0.0.1
$ python3 hydroclient.py HydroclientTestCase.test_A_000002 --grid 127.0.0.1
```

In a Jenkins deployment, the core job runs the jenkins.sh script:
```sh
$ bash jenkins.sh
```
The Jenkins template project runs a parameterized version of the python3 commands previously stated.
```sh
$ python3 hydroclient.py HydroclientTestCase.test_A_000002 --grid 127.0.0.1
```
For specifying which tests to run, edit the software system config file:
1) hydroclient.conf
2) hydroshare.conf

## Maintainers

[@hydroshare](https://github.com/hydroshare).
[@cuahsi](https://github.com/cuahsi).
[@ndebuhr](https://github.com/ndebuhr).

## Contribute

Please feel free to contribute.  [Open an issue](https://github.com/ndebuhr/cuahsi-qa-automation-engine/issues/new) or submit PRs.

## License

The CUAHSI QA Automation Engine is released under the BSD 3-Clause License. This means that [you can do what you want, so long as you don't mess with the trademark, and as long as you keep the license with the source code](https://tldrlegal.com/license/bsd-3-clause-license-(revised)).

©2018 CUAHSI. This material is based upon work supported by the National Science Foundation (NSF) under awards 1148453 and 1148090. Any opinions, findings, conclusions, or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the NSF.
