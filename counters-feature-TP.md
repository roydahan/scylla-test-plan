\page counters-feature Counters Feature Test Plan


### Existing dtest test-cases (P0) ###

\htmlonly
<body>
<style>
    div1 {
        margin: 0px 0px 0px 80px;
        background-color: transparent;
    }

    summary {
        text-indent: 45px;
    }
</style>

<details>
    <summary>batch_test.TestBatch</summary>
    <div1>counter_batch_accepts_counter_mutations_test<br></div1>
    <div1>counter_batch_rejects_regular_mutations_test<br></div1>
    <div1>logged_batch_rejects_counter_mutations_test<br></div1>
    <div1>unlogged_batch_rejects_counter_mutations_test<br></div1>
</details>

<details>
    <summary>counter_tests.TestCounters</summary>
<div1>counter_consistency_test<br></div1>
<div1>multi_counter_update_test<br></div1>
<div1>simple_increment_test<br></div1>
<div1>upgrade_test<br></div1>
<div1>validate_empty_column_name_test<br></div1>
</details>

<details>
    <summary>cql_additional_tests.TestCQL</summary>
<div1>collection_counter_test<br></div1>
<div1>counters_test<br></div1>
<div1>reserved_keyword_test<br></div1>
<div1>validate_counter_regular_test<br></div1>
</details>

<details>
    <summary>thrift_tests.TestMutations</summary>
<div1>test_counter_get_slice_range<br></div1>
<div1>test_incr_decr_standard_add<br></div1>
<div1>test_incr_decr_standard_batch_add<br></div1>
<div1>test_incr_decr_standard_batch_remove<br></div1>
<div1>test_incr_decr_standard_muliget_slice<br></div1>
<div1>test_incr_decr_standard_remove<br></div1>
<div1>test_incr_decr_standard_slice<br></div1>
<div1>test_incr_standard_remove<br></div1>
</details>
</body>

\endhtmlonly

* need to verify all relevant test cases were enabled.

\n

### Java unittests (P0) ###
* Enable all java unitests for counters.

\n

### Parallel update (P1) ###
* Update the same counter in parallel by multiple threads - as counters a read-modify-write - end result should be correct.

\n

### Commitlog replay (P1) ###
* Test a commitlog replay for counters is not causing issues (it shouldn't, as we save the end result and not the delta in commitlog).

\n

### Related Functionality support (P2) ###
* Repair
* Add Node
* Decommission Node
* Rebuild

\n

### Related Tools support (P2) ###
* sstable2json / sstabledump 
* cassandra-stress / cassandra-stress user profile ?
* sstableloader 
    - load/migrate sstables with cassandra counters
    - load/migrate sstables in old counter format (we will not support them - need to make sure we do not crash)

\n

### miscellaneous (P2) ###
* digest -read repair (e.g. when a node is down and counter was updated, the node is up read via the down node with CL=QUORUM - is the correct data read ?)
* Node replace (counter information is associated with node ... need to verify that if we replace a node it works ok / need to verify that if we remove a node it works ok)
* Authorization
* Prepared statements
* Prepared unset values
* nipticks ("Cassandra rejects USING TIMESTAMP or USING TTL in the command to update a counter column.")

\n

### Jepsen (P3) ###
* Run Jepsen for counters.

\n

