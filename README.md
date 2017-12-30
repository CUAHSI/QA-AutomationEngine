# cuahsi-qa-automation-engine

### Scope
Suite of automated tests for:
1. data.cuahsi.org (HydroClient)
2. hydroshare.org (HydroShare)

### Infrastructure
Test suite is designed to run within Jenkins+SeleniumGrid environment on CUAHSI-managed hardware

### Configuration
Test suite configuration is managed by Jenkins.  The HydroClient and HydroShare test suites are ran as separate jobs, and test cases can be brought in or out of the suite as desired.
