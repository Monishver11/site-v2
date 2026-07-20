---
title: MapReduce model
tags: [bigdata, systems]
---

A restricted programming model that buys distribution for free. You write two functions. Map takes a record and emits key-value pairs. Reduce takes a key with all its values and emits results.

Between them sits the part you do not write and the part that actually costs: shuffle and sort. Every mapper's output is partitioned by key, copied across the network to the right reducer, and sorted so that all values for a key arrive together. That guarantee, all records for a key reach the same reducer, is what makes the model work, and the network copy is usually where the time goes.

The restriction is the feature. Because map is per-record and reduce is per-key, the framework can shard data, run tasks in parallel, and re-run failed tasks on other machines without you writing any of it.

The cost is that every job materializes intermediate output to disk, which is brutal for iterative work. That limitation is what Spark was built to remove.

## Related posts

- [[big-data-4-mapreduce]] — Big Data Processing Concepts & MapReduce
- [[big-data-5-mr-dp]] — MapReduce Design Patterns
- [[spark-job]] — Anatomy of a Spark Job Run
