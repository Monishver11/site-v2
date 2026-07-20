---
title: Exactly-once semantics
tags: [bigdata, systems]
---

In a stream processor that can crash, each event should affect the result exactly once: not lost, not double-counted. Since a crashed machine cannot be asked what it had already done, this is harder than it sounds.

It is not achieved by delivering each message once. It is achieved by making replay safe. Two pieces: a durable, ordered, replayable log of input events, and periodic checkpoints of operator state paired with the log position they correspond to. On failure, restore the last checkpoint and replay the log from exactly that offset. Events after it are reprocessed, but from a state that had not yet seen them, so the result is as if each were processed once.

The phrase is therefore about effects, not deliveries. Messages may well be delivered more than once.

The same durable log gives you reprocessing for free: rewind to the beginning and recompute the whole stream after a logic change.

## Related posts

- [[big-data-10-kafka]] — Apache Kafka
- [[big-data-11-flink]] — Apache Flink
