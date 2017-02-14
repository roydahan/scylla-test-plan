\page scylla-full Scylla MASTER Test Plan

Master Test Plan Document {#scylla_test_plan}
==============================

[TOC]

**THIS IS STILL WIP**

This is Scylla Master Test Plan document.\n
This document includes both already covered areas and missing areas that should be tested.\n
To ensure the quality of the product and associated tools, testing should cover:
* Platform Support
* Functionality
* Stability & Longevity
* Performance
* 3rd Party Support & Integrations
* Scale
* Load

Each release should have a **Release Test Plan** as child page of this page.

- - -
Platforms Support - Scylla Artifacts Tests {#label_Platforms_support}
---------------------------------------------------
- - -

### &nbsp;&nbsp; Installation {#label_Installation} ###

|Platform|Supported Versions     |Test Coverage|
|:------:|:---------------------:|:------------|
| Ubuntu | 14.04\n 16.04\n       |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|
| Centos | 7.2\n 7.3\n           |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|
| RHEL   | 7                     |    None     |
| Debian | 8.6, 8.7              |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|

&nbsp;

### &nbsp;&nbsp; Auto Deployment {#label_Deployment} ###

|Platform     |Test Coverage|
|:-----------:|:------------|
| AWS         |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|
| GCE         |    None     |
| OpenStack   |    None     |

&nbsp;

### &nbsp;&nbsp; Upgrade & Rollback {#label_1_upgrade} ###

|Platform     |Test Coverage|
|:-----------:|:------------|
| Ubuntu      | Manually - https://github.com/scylladb/scylla-docs/blob/master/upgrade/upgrade-guide-from-1.5-to-1.6-ubuntu.rst |
| Centos      | Manually - https://github.com/scylladb/scylla-docs/blob/master/upgrade/upgrade-guide-from-1.5-to-1.6-rpm.rst    |
| RHEL        | Manually - https://github.com/scylladb/scylla-docs/blob/master/upgrade/upgrade-guide-from-1.5-to-1.6-rpm.rst    |    
| Debian      | None        |

&nbsp;

- - -
Functional - Scylla dtest {#label_functional}
-------------------------------------
- - -
### &nbsp;&nbsp; All Functional Tests in "master" {#label_Mater} ###

\htmlinclude all_master_tests.html

\n

&nbsp;&nbsp;&nbsp;&nbsp; **Tests Documentation**
\subpage dtest-table

\n

### &nbsp;&nbsp; Jepsen {#label_Jepsen} ###

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TBD

&nbsp;&nbsp;

- - -
Stability - Scylla Cluster Tests {#label_Stability}
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

#### Covered Tests Scenarios  ####

| Test Name               |Test Duration | Scylla Cluster Configuration                            | Test Workload Parameters                                                                                                  | Nemesis                                              |  Test Configuration File  |
| ----------------------- | ------------ | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |----------------------------------------------------- | ------------------------- |
| Sanity (fka "Longevity")| 3 hours      | n_db_nodes: 6 - i2.4xlarge\n  n_loaders: 1 - c3.large\n | write\n 1 keyspace\n cl=QUORUM\n replication_factor=3\n mode cql3 native\n rate threads=1000\n pop seq=1..10000000\n |Type: ChaosMonkey\n Monkeys: All\n Interval: 5 mins\n | aws-sanity.yaml           |
| Longevity               | 7 days       | n_db_nodes: 6 - i2.4xlarge\n  n_loaders: 1 - c3.large\n | write\n 1 keyspace\n cl=QUORUM\n replication_factor=3\n mode cql3 native\n rate threads=1000\n pop seq=1..10000000\n |Type: ChaosMonkey\n Monkeys: All\n Interval: 5 mins\n | aws-longevity.yaml        |
| Longevity-1TB           | 7 days       | n_db_nodes: 4 - i2.4xlarge\n  n_loaders: 1 - c3.large\n | write\n 1 keyspace\n cl=QUORUM\n replication_factor=3\n mode cql3 native\n rate threads=20\n col 'size=FIXED(1000) n=FIXED(1)'\n -pop seq=1..1250000000\n |Type: ChaosMonkey\n Monkeys: All\n Interval: 15 mins\n | aws-longevity-1TB.yaml   |

&nbsp;
&nbsp;
  
#### Uncovered Tests Scenarios - to be added:  ####
- Two or more nemesis at the same time.
- Multi DC scenarios
- More nemesis

&nbsp;&nbsp;

- - -
Performance {#label_Performance}
---------------------------------
- - -

#### &nbsp;&nbsp; Throughput ####
* Single Schema
    - Write-only workload <span style="color:green">(COVERED)</span>
    - Read-only workload <span style="color:green">(COVERED)</span>
    - Mixed workload <span style="color:green">(COVERED)</span>

\n

* Multiple Schemas
    - Write-only workload
    - Read-only workload
    - Mixed workload

\n

#### &nbsp;&nbsp; Latency ####
* Latency (c-s) under certain loads (25% CPU, 50% …, )
* Performance of ops (latency) and their affect on the system under certain loads

\n

#### &nbsp;&nbsp;**Customers Workloads** ####
* OutBrain
    - features
    - Users
* mParticle
    - Need to collect more data
    - Need to collect more data
* Arista
    - Need to collect more data
    - Need to collect more data

\n

- - -
3rd Party Support & Integrations {#label_3rd_party_support}
--------------------------------------------------------------
- - -
Integration testing with:
* Thrift
* Python Driver
* Other Drivers
* Titan DB
* Spark
* Others?

\n

- - -
Scale {#label_Scale}
------------------------------
- - -
Testing functionality (e.g. Repair, compaction, compression, etc), stability and performance on:
* Large size data sets (1TB, 2TB, 5TB, 10TB)
* Scaling to **LARGE** size Clusters (>10)
* Scaling to **Extra-Large** size Clusters (>30)
* Large Scale decommission

\n

- - -
Load {#label_Load}
------------------------------
- - -
Common server functionality during high load in terms of:
* CPU Bound
* Network Bound
* Disk Bound
* Memory Bound

\n

- - -
Management and Monitoring {#label_1_Management}
------------------------------
- - -
* Grafana monitoring dashboard


