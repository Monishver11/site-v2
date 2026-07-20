---
title: Tiling
tags: [gpu, performance]
---

Cut the problem into blocks that fit in fast memory, load each block once, and do all the work that touches it before moving on. That is the whole idea, and it is the main lever on [[arithmetic-intensity]] because it cuts bytes moved rather than flops done.

For GEMM: a naive kernel re-reads rows and columns from global memory for every output element. Tile it so a block of A and a block of B are staged in shared memory, and every thread in the block reuses them. A $T \times T$ tile reuses each loaded element $T$ times, so intensity scales with $T$ and the kernel walks up the roofline as tiles grow.

Tiles cannot grow forever: shared memory and registers are the ceiling, and larger tiles mean fewer resident blocks and less latency hiding. There is also tile quantization, where dimensions are not divisible by the tile size and boundary blocks launch with threads that have nothing to compute.

[[cute-layouts]] is the vocabulary for expressing these decisions precisely.

## Related posts

- [[simons-gemm-notes]] — GEMM Kernel Optimization Notes
- [[gemm-colfax-1]] — CUTLASS WGMMA on Hopper - Notes
- [[fa3-k2]] — K2 in CuTe [FA3]
