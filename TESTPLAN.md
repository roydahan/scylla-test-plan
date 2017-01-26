Scylla Test Plan {#mainpage}
====================================

Master Test Plan Document  {#scylla_test_plan}
===============================================

[TOC]

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
Platforms Support {#label_Platforms_support}
---------------------------------------------------
- - -

### &nbsp;&nbsp; Installation {#label_Installation} ###

|Platform|Tested on Versions     |Test Coverage|
|:------:|:---------------------:|:------------|
| Ubuntu | 14.04\n 16.04\n       |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|
| Centos | 7.2.1511\n 7.3.1611\n |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|
| RHEL   | None                  |    None     |
| Debian | None                  |    None     |

&nbsp;
### &nbsp;&nbsp; Auto Deployment {#label_Deployment} ###

|Platform     |Test Coverage|
|:-----------:|:------------|
| AWS         |scylla-artifacts.py:ScyllaArtifactSanity.test_after_install\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_stop_start\n scylla-artifacts.py:ScyllaArtifactSanity.test_after_restart|
| GCE         |    None     |
| OpenStack   |    None     |

&nbsp;

- - -
Functional {#label_functional}
-------------------------------------
- - -
### &nbsp;&nbsp; Regression {#label_Regression} ###
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; List of supported functionality that are part of previously released versions: 


| Functionality | Implemented Tests |
| ------------- | :----------------  |
| **Authentication & Authorization** | auth_test.py\n  |
| **Backup & Restore** | backup_restore_tests.py\n  |
| **Batch** | batch_test.py\n  |
| **Bootstrap** | bootstrap_test::TestBootstrap.killed_wiped_node_cannot_join_test\n bootstrap_test::TestBootstrap.local_quorum_bootstrap_test\n bootstrap_test::TestBootstrap.manual_bootstrap_test\n bootstrap_test::TestBootstrap.read_from_bootstrapped_node_test\n bootstrap_test::TestBootstrap.shutdown_wiped_node_cannot_join_test\n bootstrap_test::TestBootstrap.simple_bootstrap_test\n  |
| **CFID** | cfid_test.py\n  |
| **clustering_key_filter** | clustering_key_filter_test.py\n  |
| **Commitlog** | commitlog_test::TestCommitLog.test_commitlog_replay_on_startup\n commitlog_test::TestCommitLog.test_commitlog_replay_with_alter_table\n  |
| **Compaction** | compaction_additional_test.py\n compaction_test::TestCompaction_with_DateTieredCompactionStrategy.compaction_delete_2_test\n compaction_test::TestCompaction_with_DateTieredCompactionStrategy.compaction_delete_test\n compaction_test::TestCompaction_with_DateTieredCompactionStrategy.compaction_strategy_switching_test\n compaction_test::TestCompaction_with_LeveledCompactionStrategy.compaction_delete_2_test\n compaction_test::TestCompaction_with_LeveledCompactionStrategy.compaction_delete_test\n compaction_test::TestCompaction_with_LeveledCompactionStrategy.compaction_strategy_switching_test\n compaction_test::TestCompaction_with_SizeTieredCompactionStrategy.compaction_delete_2_test\n compaction_test::TestCompaction_with_SizeTieredCompactionStrategy.compaction_delete_test\n compaction_test::TestCompaction_with_SizeTieredCompactionStrategy.compaction_strategy_switching_test\n  |
| **concurrent_schema_changes** | concurrent_schema_changes_test.py\n  |
| **Consistency** | consistency_test::TestAccuracy.test_network_topology_strategy_users\n consistency_test::TestAccuracy.test_simple_strategy_users\n consistency_test::TestAvailability.test_network_topology_strategy\n consistency_test::TestAvailability.test_simple_strategy\n consistency_test::TestConsistency.data_query_digest_test\n consistency_test::TestConsistency.quorum_available_during_failure_test\n consistency_test::TestConsistency.readrepair_test\n consistency_test::TestConsistency.short_read_delete_test\n consistency_test::TestConsistency.short_read_quorum_delete_test\n consistency_test::TestConsistency.short_read_reversed_test\n consistency_test::TestConsistency.short_read_test\n  |
| **Also bootstrap?** | consistent_bootstrap_test.py\n  |
| **CQL** | cql_additional_tests::TestCQL.alter_bug_test\n cql_additional_tests::TestCQL.alter_with_collections_test\n cql_additional_tests::TestCQL.batch_and_list_test\n cql_additional_tests::TestCQL.batch_test\n cql_additional_tests::TestCQL.blobAs_functions_test\n cql_additional_tests::TestCQL.boolean_test\n cql_additional_tests::TestCQL.bop_order_test\n cql_additional_tests::TestCQL.bug_4532_test\n cql_additional_tests::TestCQL.bug_4882_test\n cql_additional_tests::TestCQL.bug_6115_test\n cql_additional_tests::TestCQL.bug7105_test\n cql_additional_tests::TestCQL.clustering_order_and_functions_test\n cql_additional_tests::TestCQL.clustering_order_in_test\n cql_additional_tests::TestCQL.collection_and_regular_test\n cql_additional_tests::TestCQL.collection_compact_test\n cql_additional_tests::TestCQL.collection_function_test\n cql_additional_tests::TestCQL.collection_serialization_with_protocol_v2_test\n cql_additional_tests::TestCQL.column_name_validation_test\n cql_additional_tests::TestCQL.compact_metadata_test\n cql_additional_tests::TestCQL.composite_partition_key_validation_test\n cql_additional_tests::TestCQL.composite_row_key_test\n cql_additional_tests::TestCQL.compression_option_validation_test\n cql_additional_tests::TestCQL.conversion_functions_test\n cql_additional_tests::TestCQL.count_test\n cql_additional_tests::TestCQL.cql3_insert_thrift_test\n cql_additional_tests::TestCQL.create_invalid_test\n cql_additional_tests::TestCQL.date_test\n cql_additional_tests::TestCQL.delete_row_test\n cql_additional_tests::TestCQL.deletion_test\n cql_additional_tests::TestCQL.dense_cf_test\n cql_additional_tests::TestCQL.downgrade_to_compact_bug_test\n cql_additional_tests::TestCQL.drop_and_readd_collection_test\n cql_additional_tests::TestCQL.empty_blob_test\n cql_additional_tests::TestCQL.empty_in_test\n cql_additional_tests::TestCQL.exclusive_slice_test\n cql_additional_tests::TestCQL.float_with_exponent_test\n cql_additional_tests::TestCQL.function_and_reverse_type_test\n cql_additional_tests::TestCQL.function_with_null_test\n cql_additional_tests::TestCQL.identifier_test\n cql_additional_tests::TestCQL.in_clause_wide_rows_test\n cql_additional_tests::TestCQL.in_order_by_without_selecting_test\n cql_additional_tests::TestCQL.invalid_old_property_test\n cql_additional_tests::TestCQL.invalid_string_literals_test\n cql_additional_tests::TestCQL.in_with_desc_order_test\n cql_additional_tests::TestCQL.keyspace_creation_options_test\n cql_additional_tests::TestCQL.keyspace_test\n cql_additional_tests::TestCQL.large_clustering_in_test\n cql_additional_tests::TestCQL.large_count_test\n cql_additional_tests::TestCQL.limit_bugs_test\n cql_additional_tests::TestCQL.limit_multiget_test\n cql_additional_tests::TestCQL.limit_ranges_test\n cql_additional_tests::TestCQL.limit_sparse_test\n cql_additional_tests::TestCQL.list_prefetch_with_static_column_test\n cql_additional_tests::TestCQL.list_test\n cql_additional_tests::TestCQL.map_test\n cql_additional_tests::TestCQL.more_order_by_test\n cql_additional_tests::TestCQL.multi_collection_test\n cql_additional_tests::TestCQL.multi_list_set_test\n cql_additional_tests::TestCQL.multiordering_test\n cql_additional_tests::TestCQL.multiordering_validation_test\n cql_additional_tests::TestCQL.nan_infinity_test\n cql_additional_tests::TestCQL.negative_timestamp_test\n cql_additional_tests::TestCQL.noncomposite_static_cf_test\n cql_additional_tests::TestCQL.nonpure_function_collection_test\n cql_additional_tests::TestCQL.null_support_test\n cql_additional_tests::TestCQL.only_pk_test\n cql_additional_tests::TestCQL.order_by_multikey_test\n cql_additional_tests::TestCQL.order_by_test\n cql_additional_tests::TestCQL.order_by_validation_test\n cql_additional_tests::TestCQL.order_by_with_in_test\n cql_additional_tests::TestCQL.range_key_ordered_test\n cql_additional_tests::TestCQL.range_query_test\n cql_additional_tests::TestCQL.range_slice_test\n cql_additional_tests::TestCQL.range_with_deletes_test\n cql_additional_tests::TestCQL.remove_range_slice_test\n cql_additional_tests::TestCQL.rename_test\n cql_additional_tests::TestCQL.reversed_compact_multikey_test\n cql_additional_tests::TestCQL.reversed_compact_test\n cql_additional_tests::TestCQL.reversed_comparator_test\n cql_additional_tests::TestCQL.row_existence_test\n cql_additional_tests::TestCQL.select_distinct_test\n cql_additional_tests::TestCQL.select_distinct_with_deletions_test\n cql_additional_tests::TestCQL.select_key_in_test\n cql_additional_tests::TestCQL.select_with_alias_test\n cql_additional_tests::TestCQL.set_test\n cql_additional_tests::TestCQL.slicing_test\n cql_additional_tests::TestCQL.sparse_cf_test\n cql_additional_tests::TestCQL.static_cf_test\n cql_additional_tests::TestCQL.static_with_empty_clustering_test\n cql_additional_tests::TestCQL.static_with_limit_test\n cql_additional_tests::TestCQL.table_options_test\n cql_additional_tests::TestCQL.table_test\n cql_additional_tests::TestCQL.ticket_5230_test\n cql_additional_tests::TestCQL.timestamp_and_ttl_test\n cql_additional_tests::TestCQL.timeuuid_test\n cql_additional_tests::TestCQL.token_range_test\n cql_additional_tests::TestCQL.truncate_clean_cache_test\n cql_additional_tests::TestCQL.tuple_notation_test\n cql_additional_tests::TestCQL.undefined_column_handling_test\n cql_additional_tests::TestCQL.unescaped_string_test\n cql_additional_tests::TestCQL.update_type_test\n cql_tests.py\n cql_tracing_test.py\n  |
| **Inter-node SSL** | internode_ssl_test.py\n  |
| **json tools** | json_tools_test.py\n  |
| **Large columns** | largecolumn_test.py\n  |
| **Limits** | limits_test.py\n  |
| **Migration** | migration_test.py\n  |
| **Multi DC** | multidc_putget_test.py\n  |
| **native_transport_ssl** | native_transport_ssl_test.py\n  |
| **Nodetool** | nodetool_additional_test.py\n  |
| **Offline tools** | offline_tools_test.py\n  |
| **Paging** | paging_additional_test.py\n paging_test::TestPagingDatasetChanges.test_cell_TTL_expiry_during_paging\n paging_test::TestPagingDatasetChanges.test_data_change_impacting_earlier_page\n paging_test::TestPagingDatasetChanges.test_data_change_impacting_later_page\n paging_test::TestPagingDatasetChanges.test_node_unavailabe_during_paging\n paging_test::TestPagingDatasetChanges.test_row_TTL_expiry_during_paging\n paging_test::TestPagingData.static_columns_paging_test\n paging_test::TestPagingData.test_paging_across_multi_wide_rows\n paging_test::TestPagingData.test_paging_a_single_wide_row\n paging_test::TestPagingQueryIsolation.test_query_isolation\n paging_test::TestPagingSize.test_undefined_page_size_default\n paging_test::TestPagingSize.test_with_equal_results_to_page_size\n paging_test::TestPagingSize.test_with_less_results_than_page_size\n paging_test::TestPagingSize.test_with_more_results_than_page_size\n paging_test::TestPagingSize.test_with_no_results\n paging_test::TestPagingWithDeletions.test_multiple_cell_deletions\n paging_test::TestPagingWithDeletions.test_multiple_partition_deletions\n paging_test::TestPagingWithDeletions.test_single_cell_deletions\n paging_test::TestPagingWithDeletions.test_single_partition_deletions\n paging_test::TestPagingWithDeletions.test_single_row_deletions\n paging_test::TestPagingWithDeletions.test_ttl_deletions\n paging_test::TestPagingWithModifiers.test_with_allow_filtering\n paging_test::TestPagingWithModifiers.test_with_limit\n paging_test::TestPagingWithModifiers.test_with_order_by\n paging_test::TestPagingWithModifiers.test_with_order_by_reversed\n  |
| **Partitioner** | partitioner_tests.py\n  |
| **Persistence** | persistence_test.py\n  |
| **pushed_notifications** | pushed_notifications_test::TestPushedNotifications.move_single_node_test\n pushed_notifications_test::TestPushedNotifications.restart_node_test\n  |
| **range_ghost** | range_ghost_test.py\n  |
| **Repair** | repair_additional_test.py\n repair_test.py\n  |
| **replace_address** | replace_address_test.py\n  |
| **Schema** | schema_management_test.py\n schema_test.py\n  |
| **Boot/Shutdown** | simple_boot_shutdown.py\n  |
| **Cluster Driver** | simple_cluster_driver_test.py\n simple_driver_test.py\n  |
| **Snapshot** | snapshot_test::TestSnapshot.test_basic_snapshot_and_restore_with_refresh\n  |
| **SSTables** | sstable_generation_loading_test::TestSSTableGenerationAndLoading.promoted_index_generation_with_small_partition_followed_by_a_large_partition_test\n sstableloader_test.py\n sstablesplit_test.py\n  |
| **Thrift** | thrift_tests.py\n  |
| **Topology** | topology_test::TestTopology.crash_during_decommission_test\n topology_test::TestTopology.decommissioned_node_cant_rejoin_test\n topology_test::TestTopology.decommission_test\n topology_test::TestTopology.movement_test\n topology_test::TestTopology.move_single_node_test\n  |
| **TTL** | ttl_test.py\n  |
| **update_cluster_layout** | update_cluster_layout_tests::TestUpdateClusterLayout.add_node_with_large_partition1_test\n update_cluster_layout_tests::TestUpdateClusterLayout.add_node_with_large_partition2_test\n update_cluster_layout_tests::TestUpdateClusterLayout.add_node_with_large_partition3_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_add_new_node_while_query_info_1_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_add_new_node_while_query_info_2_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_add_new_node_while_schema_changes_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_add_node_1_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_add_two_nodes_in_parallel_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_decommission_node_1_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_decommission_node_2_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_decommission_node_while_adding_info_1_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_decommission_node_while_adding_info_2_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_decommission_node_while_query_info_1_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_decommission_node_while_query_info_2_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_kill_new_node_while_bootstrapping_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_kill_new_node_while_bootstrapping_with_parallel_writes_in_multidc_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_kill_new_node_while_bootstrapping_with_parallel_writes_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_kill_node_while_decommissioning_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_removenode_1_test\n update_cluster_layout_tests::TestUpdateClusterLayout.simple_removenode_2_test\n  |
| **User Types** | user_types_test.py\n  |
| **Wide Rows** | wide_rows_test.py\n  |
| **Materialized Views** | materialized_views_test.py |
| **Other** | \n \n  | 

&nbsp;&nbsp;

- - -
Stability {#label_Stability}
------------------------------
- - -
* Sanity
* Short Term Longevity
* Long Term Longevity
* Crash Recovery?

- - -
Performance {#label_Performance}
---------------------------------
- - -

#### &nbsp;&nbsp; Throughput ####
* Single Schema
    - Write-only workload
    - Read-only workload
    - Mixed workload

* Multiple Schemas
    - Write-only workload
    - Read-only workload
    - Mixed workload

#### &nbsp;&nbsp; Latency ####
* Latency (c-s) under certain loads (25% CPU, 50% …, )
* Performance of ops (latency) and their affect on the system under certain loads


#### &nbsp;&nbsp;**Customers Workloads** ####
* OutBrain
    - features
    - Users
* mParticle
    - a
    - b
* Arista
    - a
    - b

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
* ???

- - -
Scale {#label_Scale}
------------------------------
- - -
Testing functionality (e.g. Repair, compaction, compression, etc), stability and performance on:
* Large size SStables (1TB, 2TB, 5TB, 10TB)
* Scaling to **LARGE** size Clusters (>10)
* Scaling to **Extra-Large** size Clusters (>30)
* Large Scale decommission

- - -
Load {#label_Load}
------------------------------
- - -
Common server functionality during high load in terms of:
* CPU Bound
* Network Bound
* Disk Bound
* Memory Bound


