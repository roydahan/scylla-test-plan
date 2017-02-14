\page scylla-1-6 Release 1.6 - Test Plan Document  

Release Test Plan - 1.6 {#scylla_1-6_test_plan}
===============================================

[TOC]

- - -
Platforms Support - Scylla Artifacts Tests{#label_1_Platforms_support}
-----------------------------------------------------------------------
- - -

###  Installation {#label_1_Installation} ###

|Platform|Tested on Versions     |Test Coverage|
|:------:|:---------------------:|:------------|
| Ubuntu | 14.04\n 16.04\n       |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|
| Centos | 7.2\n 7.3\n           |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|



###  New Support - Experimental {#label_1_New_Support} ###

|Platform|Tested on Versions     |Test Coverage|
|:------:|:---------------------:|:------------|
| Debian | 8.6\n 8.7\n          |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|



###  Upgrade & Rollback {#label_1_upgrade} ###

|Platform     |Test Coverage|
|:-----------:|:------------|
| Ubuntu      | Manually - https://github.com/scylladb/scylla-docs/blob/master/upgrade/upgrade-guide-from-1.5-to-1.6-ubuntu.rst |
| Centos      | Manually - https://github.com/scylladb/scylla-docs/blob/master/upgrade/upgrade-guide-from-1.5-to-1.6-rpm.rst    | 



###  Auto Deployment {#label_1_Deployment} ###

|Platform     |Test Coverage|
|:-----------:|:------------|
| AWS         |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|



- - -
Functional - Scylla dtest {#label_1_functional}
-------------------------------------
- - -

###  Progression {#label_1_Progression} ###
**New Functionality and Tests in @release:**

\htmlonly
<details>
  <summary>thrift_tests.TestMutations</summary>
  &nbsptest_multiget_slice_with_count
</details>

\endhtmlonly



###  Regression {#label_1_Regression} ###
**List of supported functionality that are part of previously released versions:** 

\htmlinclude 1-6-all-tests.html


**Tests Documentation**
\subpage dtest-table



- - -
Stability - Scylla Cluster Tests {#label_1_Stability}
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




#### Tests Scenarios  ####

| Test Name               |Test Duration | Scylla Cluster Configuration                            | Test Workload Parameters                                                                                                  | Nemesis                                              |  Test Configuration File  |
| ----------------------- | ------------ | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |----------------------------------------------------- | ------------------------- |
| Sanity (fka "Longevity")| 3 hours      | n_db_nodes: 6 - i2.4xlarge\n  n_loaders: 1 - c3.large\n | write\n 1 keyspace\n cl=QUORUM\n replication_factor=3\n mode cql3 native\n rate threads=1000\n pop seq=1..10000000\n |Type: ChaosMonkey\n Monkeys: All\n Interval: 5 mins\n | aws-sanity.yaml           |
| Longevity               | 7 days       | n_db_nodes: 6 - i2.4xlarge\n  n_loaders: 1 - c3.large\n | write\n 1 keyspace\n cl=QUORUM\n replication_factor=3\n mode cql3 native\n rate threads=1000\n pop seq=1..10000000\n |Type: ChaosMonkey\n Monkeys: All\n Interval: 5 mins\n | aws-longevity.yaml        |
| Longevity-1TB           | 7 days       | n_db_nodes: 4 - i2.4xlarge\n  n_loaders: 1 - c3.large\n | write\n 1 keyspace\n cl=QUORUM\n replication_factor=3\n mode cql3 native\n rate threads=20\n col 'size=FIXED(1000) n=FIXED(1)'\n -pop seq=1..1250000000\n |Type: ChaosMonkey\n Monkeys: All\n Interval: 15 mins\n | aws-longevity-1TB.yaml   |
  


- - -
Performance {#label_1_Performance}
---------------------------------
- - -

####  Throughput ####
**Single Schema Regression Tests**
    
| Test Name               |Test Duration | Scylla Cluster Configuration                            | Test Workload Parameters                                                                                            | Nemesis |  Test Configuration File       |
| ----------------------- | ------------ | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |-------- | ------------------------------ |
| Write-only workload     | 1 hour       | n_db_nodes: 3 - i2.2xlarge\n  n_loaders: 4 - c4.large\n | write\n 1 keyspace\n cl=QUORUM\n replication_factor=3\n mode cql3 native\n rate threads=100\n pop seq=1..10000000\n | None    | aws-perf-mixed-regression.yaml |
| Read-only workload      | 50 mins      | n_db_nodes: 3 - i2.2xlarge\n  n_loaders: 4 - c4.large\n | write\n pop seq=1..30000000\n \n **read**\n rate threads=100\n pop 'dist=gauss(1..30000000,15000000,1500000)'\n     | None    | aws-perf-mixed-regression.yaml |
| Mixed workload          | 7 days       | n_db_nodes: 3 - i2.2xlarge\n  n_loaders: 4 - c4.large\n | write\n pop seq=1..30000000\n \n **mixed**\n rate threads=100\n pop 'dist=gauss(1..30000000,15000000,1500000)'\n    | None    | aws-perf-mixed-regression.yaml |


    
- - -
3rd Party Support & Integrations {#label_1_3rd_party_support}
--------------------------------------------------------------
- - -

None.

- - -
Scale {#label_1_Scale}
------------------------------
- - -
Testing functionality (e.g. Repair, compaction, compression, etc), stability and performance on:
* Large size data sets - Longevity-1TB (see above).

- - -
Load {#label_1_Load}
------------------------------
- - -

None.

- - -
Management and Monitoring {#label_1_Management}
------------------------------
- - -
* Grafana monitoring dashboard


- - -
Exit Criteria {#label_1_Exit}
------------------------------
1. Scylla Artifacts Tests to pass on all supported platforms.
2. Upgrade and rollback tests to pass on all supported platforms and scylla-docs are updated accordingly.
3. Functional tests - No regressions.
4. Stability scenarios - Systems should survive and I/O should resume at all time without core dumps or critical errors.
5. Performance tests - No regressions.


