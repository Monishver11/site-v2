---
title: Arithmetic intensity
tags: [gpu, performance]
---

FLOPs performed per byte moved from memory. It decides, before you write a line of code, whether a kernel can possibly be compute-bound.

Compare it against the hardware's ratio of peak FLOP/s to peak bandwidth. Below that ratio you are memory-bound and the compute units idle waiting on data; above it you are compute-bound and bandwidth has slack. This is the roofline model in one sentence.

The numbers are stark. An elementwise add reads two floats and writes one to do a single flop: intensity around 0.08, deeply memory-bound, and no amount of arithmetic cleverness helps. A GEMM does $O(n^3)$ work over $O(n^2)$ data, so intensity grows with tile size, which is the entire reason [[tiling]] exists.

The lever is almost always the denominator. You rarely reduce the flops; you cut the bytes by reusing data once it has been brought close. See [[gpu-memory-hierarchy]].

## Related posts

- [[gpu-intro]] — GPU Essentials - A Concise Technical Guide
- [[gpu-notes]] — GPU Notes
- [[simons-gemm-notes]] — GEMM Kernel Optimization Notes
