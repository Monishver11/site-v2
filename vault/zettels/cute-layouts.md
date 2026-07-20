---
title: CuTe layouts
tags: [gpu, cute]
---

A CuTe layout is a pair — shape and stride — defining a pure function from coordinate to memory offset. No data, no pointer; just a description of how to walk an indexed grid. Everything else in CUTLASS 3.x (tensors, partitioning, MMA atoms) composes on top of this one object.

The power is algebraic: layouts compose, divide, and product, so "give each thread its slice of this SMEM tile" becomes a layout expression the compiler can fold into constant arithmetic at JIT time.

Layouts are how tiling decisions from [[gpu-memory-hierarchy]] get expressed in code.

## Related posts

- [[cute]] — CuTe DSL - Notes
- [[fa3-cute]] — CuTe DSL fundamentals and primitives [FA3]
- [[fa3-k1]] — K1 in CuTe [FA3]
