---
title: WGMMA
tags: [gpu, cute]
---

Hopper's warpgroup matrix multiply-accumulate. The unit of issue is a warpgroup, four warps acting together, rather than a single warp as with earlier `mma` instructions. One instruction covers a much larger tile.

It is asynchronous. `wgmma.mma_async` is issued and the warpgroup continues; you commit and wait on the result later. That gap is the point, because it lets the next tile's copies overlap with the current tile's math instead of alternating stall and compute.

It also reads operands from shared memory through a matrix descriptor rather than requiring everything staged in registers first, which relieves register pressure and removes an explicit SMEM-to-register step. The accumulator still lives in registers.

The cost is rigidity: operand layouts and swizzling are dictated by the instruction, not chosen. Getting a descriptor wrong is the standard way to lose a day. [[cute-layouts]] exists partly to make those constraints expressible, and [[warp-specialization]] is the pattern that exploits the asynchrony.

## Related posts

- [[gemm-colfax-1]] — CUTLASS WGMMA on Hopper - Notes
- [[fa3-k4]] — K4 in CuTe [FA3]
