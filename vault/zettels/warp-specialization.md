---
title: Warp specialization
tags: [gpu, performance]
---

Instead of every warp running the same code, give different warps different jobs. Some warps only move data, others only compute, and they hand off through shared memory with barriers between them.

This is a producer-consumer pipeline inside one thread block. The producer warps run ahead issuing async copies for tile $i+1$ while the consumer warps do math on tile $i$. The copy latency disappears behind compute instead of stalling it.

It became worth doing on Hopper specifically because the hardware acquired the asynchrony to exploit: TMA for bulk copies and async [[wgmma]] for the math, both issued without blocking. Uniform warps cannot keep both pipes busy, since the same instruction stream has to alternate.

The cost is complexity. Two roles mean two code paths, explicit barriers, and a shared memory budget split into multiple buffers so the producer has somewhere to write while the consumer reads. Getting the barrier discipline wrong deadlocks rather than merely running slowly.

## Related posts

- [[fa3-worklog]] — FlashAttention 3 - A Worklog[WIP]
- [[fa3-k4]] — K4 in CuTe [FA3]
