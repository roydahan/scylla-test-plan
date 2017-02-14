\page scylla-1-7 Release 1.7 - Test Plan Document  

Release Test Plan - 1.7 {#scylla_1-7_test_plan}
===============================================

[TOC]

- - -
Platforms Support - Scylla Artifacts Tests{#label_2_Platforms_support}
-----------------------------------------------------------------------
- - -

### &nbsp;&nbsp; Installation {#label_2_Installation} ###

|Platform|Tested on Versions     |Test Coverage|
|:------:|:---------------------:|:------------|
| Ubuntu | 14.04\n 16.04\n       |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|
| Centos | 7.2\n 7.3\n           |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|

&nbsp;

### &nbsp;&nbsp; New Support {#label_2_New_Support} ###

|Platform|Tested on Versions     |Test Coverage|
|:------:|:---------------------:|:------------|
| Debian | 8.6\n 8.7\n          |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|

&nbsp;

### &nbsp;&nbsp; Upgrade & Rollback {#label_2_upgrade} ###

|Platform     |Test Coverage|
|:-----------:|:------------|
| Ubuntu      | Manually -  |
| Centos      | Manually -  | 

&nbsp;

### &nbsp;&nbsp; Auto Deployment {#label_2_Deployment} ###

|Platform     |Test Coverage|
|:-----------:|:------------|
| AWS         |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|

&nbsp;

- - -
Functional - Scylla dtest {#label_2_functional}
-------------------------------------
- - -

### &nbsp;&nbsp; Progression {#label_2_Progression} ###
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **New Functionality in v1.7:**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \subpage counters-feature 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Other Tests Added in v1.7:**

\htmlinclude 1-7-diff-tests.html


### &nbsp;&nbsp; Regression {#label_2_Regression} ###
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **List of supported functionality that are part of previously released versions:** 

\htmlinclude 1-7-all-tests.html


**Tests Documentation**
\subpage dtest-table

&nbsp;&nbsp;

- - -
Stability - Scylla Cluster Tests {#label_2_Stability}
------------------------------------
- - -
These tests uses SCT as test infrastructure and avocado as test framework.
ChaosMonkey framework is being used for cluster disruptions.

#### Supported disruptor ####

| Nemesis Class| Nemesis Name             | Disruption Method |
| :----------: | :--------------------:   | :--------------------------------------------------------- |
| ChaosMonkey  | StopStartMonkey          | sdcm.nemesis.Nemesis.disrupt_stop_start_scylla_server      |
| ChaosMonkey  | StopWaitStartMonkey      | sdcm.nemesis.Nemesis.disrupt_stop_wait_start_scylla_server |
| ChaosMonkey  | DrainerMonkey            | sdcm.nemesis.Nemesis.disrupt_nodetool_drain                |
| ChaosMonkey  | CorruptThenRepairMonkey  | sdcm.nemesis.Nemesis.disrupt_destroy_data_then_repair      |
| ChaosMonkey  | CorruptThenRebuildMonkey | sdcm.nemesis.Nemesis.disrupt_destroy_data_then_rebuild     |
| ChaosMonkey  | DecommissionMonkey       | sdcm.nemesis.Nemesis.disrupt_nodetool_decommission         |

&nbsp;
&nbsp;

#### Tests Scenarios  ####

| Test Name               |Test Duration | Scylla Cluster Configuration                            | Test Workload Parameters                                                                                                  | Nemesis                                              |  Test Configuration File  |
| ----------------------- | ------------ | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |----------------------------------------------------- | ------------------------- |
| Sanity (fka "Longevity")| 3 hours      | n_db_nodes: 6 - i2.4xlarge\n  n_loaders: 1 - c3.large\n | write\n 1 keyspace\n cl=QUORUM\n replication_factor=3\n mode cql3 native\n rate threads=1000\n pop seq=1..10000000\n |Type: ChaosMonkey\n Monkeys: All\n Interval: 5 mins\n | aws-sanity.yaml           |
| Longevity               | 7 days       | n_db_nodes: 6 - i2.4xlarge\n  n_loaders: 1 - c3.large\n | write\n 1 keyspace\n cl=QUORUM\n replication_factor=3\n mode cql3 native\n rate threads=1000\n pop seq=1..10000000\n |Type: ChaosMonkey\n Monkeys: All\n Interval: 5 mins\n | aws-longevity.yaml        |
| Longevity-1TB           | 7 days       | n_db_nodes: 4 - i2.4xlarge\n  n_loaders: 1 - c3.large\n | write\n 1 keyspace\n cl=QUORUM\n replication_factor=3\n mode cql3 native\n rate threads=20\n col 'size=FIXED(1000) n=FIXED(1)'\n -pop seq=1..1250000000\n |Type: ChaosMonkey\n Monkeys: All\n Interval: 15 mins\n | aws-longevity-1TB.yaml   |
  
&nbsp;&nbsp;

- - -
Performance {#label_2_Performance}
---------------------------------
- - -

#### &nbsp;&nbsp; Throughput ####
**Single Schema Regression Tests**
    
| Test Name               |Test Duration | Scylla Cluster Configuration                            | Test Workload Parameters                                                                                            | Nemesis |  Test Configuration File       |
| ----------------------- | ------------ | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |-------- | ------------------------------ |
| Write-only workload     | 1 hour       | n_db_nodes: 3 - i2.2xlarge\n  n_loaders: 4 - c4.large\n | write\n 1 keyspace\n cl=QUORUM\n replication_factor=3\n mode cql3 native\n rate threads=100\n pop seq=1..10000000\n | None    | aws-perf-mixed-regression.yaml |
| Read-only workload      | 50 mins      | n_db_nodes: 3 - i2.2xlarge\n  n_loaders: 4 - c4.large\n | write\n pop seq=1..30000000\n \n **read**\n rate threads=100\n pop 'dist=gauss(1..30000000,15000000,1500000)'\n     | None    | aws-perf-mixed-regression.yaml |
| Mixed workload          | 7 days       | n_db_nodes: 3 - i2.2xlarge\n  n_loaders: 4 - c4.large\n | write\n pop seq=1..30000000\n \n **mixed**\n rate threads=100\n pop 'dist=gauss(1..30000000,15000000,1500000)'\n    | None    | aws-perf-mixed-regression.yaml |

&nbsp;&nbsp;
    
- - -
3rd Party Support & Integrations {#label_2_3rd_party_support}
--------------------------------------------------------------
- - -

None.

- - -
Scale {#label_2_Scale}
------------------------------
- - -
Testing functionality (e.g. Repair, compaction, compression, etc), stability and performance on:
* Large size data sets - Longevity-1TB (see above).

- - -
Load {#label_2_Load}
------------------------------
- - -

None.

- - -
Management and Monitoring {#label_2_Management}
------------------------------
- - -
* Grafana monitoring dashboard


- - -
Exit Criteria {#label_2_Exit}
------------------------------
1. Scylla Artifacts Tests to pass on all supported platforms.
2. Upgrade and rollback tests to pass on all supported platforms and scylla-docs are updated accordingly.
3. Functional tests - No regressions.
4. Stability scenarios - Systems should survive and I/O should resume at all time without core dumps or critical errors.
5. Performance tests - No regressions.


