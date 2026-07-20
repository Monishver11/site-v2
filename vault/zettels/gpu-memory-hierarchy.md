---
title: GPU memory hierarchy
tags: [gpu]
---

Every GPU performance story is a story about the memory hierarchy: registers, shared memory (SMEM), L2, and global memory (GMEM), each roughly an order of magnitude apart in bandwidth and latency. Kernels are fast when data moves down the hierarchy once and gets reused many times before moving back up.

Arithmetic intensity — FLOPs per byte moved — decides whether a kernel is compute-bound or memory-bound. Elementwise ops sit deep in memory-bound territory; GEMM earns compute-bound status only with aggressive tiling and reuse.

Tiling is the act of choosing which slice of data lives at which level, and [[cute-layouts]] is the vocabulary for describing those choices precisely. [[online-softmax]] exists because materializing an attention matrix to GMEM violates everything this note says.

## Related posts

- [[gpu-intro]] — GPU Essentials - A Concise Technical Guide
- [[gpu-notes]] — GPU Notes
- [[aleksagordic-gpu-blog-notes]] — Reading Notes from Aleksa Gordic's GPU BlogPost
- [[simons-gemm-notes]] — GEMM Kernel Optimization Notes
