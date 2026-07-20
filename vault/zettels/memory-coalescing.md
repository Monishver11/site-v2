---
title: Memory coalescing
tags: [gpu, performance]
---

Threads in a warp issue loads together, and the memory system services them in fixed-size transactions. If the 32 threads touch 32 consecutive addresses, the hardware merges them into the minimum number of transactions. If they touch scattered addresses, you get one transaction per thread and waste most of every line you paid for.

Think of 32 people each ordering one item from the same store. Consecutive addresses are one bulk delivery. Scattered addresses are 32 separate trips for one item each, same distance travelled, a fraction of the goods.

The practical consequence is that access pattern matters as much as access count. The classic case is a row-major matrix read down a column: stride equal to the row length, every thread in its own line, effective bandwidth collapsing to a fraction of peak. The fix is usually to change which thread handles which element, not to move less data.

This is why [[cute-layouts]] treats stride as a first-class object. See [[gpu-memory-hierarchy]].

## Related posts

- [[gpu-intro]] — GPU Essentials - A Concise Technical Guide
- [[simons-gemm-notes]] — GEMM Kernel Optimization Notes
