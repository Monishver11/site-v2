---
title: Online softmax
tags: [gpu, attention]
---

Softmax normally needs two passes: one for the max (numerical stability), one for the normalizing sum. Online softmax fuses them — maintain a running max $m$ and running sum $\ell$, and when a new block raises the max, rescale the accumulated sum by $e^{m_{old} - m_{new}}$.

$$
\ell_{new} = \ell_{old} \cdot e^{m_{old} - m_{new}} + \sum_i e^{x_i - m_{new}}
$$

This is the enabling trick of FlashAttention: attention can be computed block by block in SMEM without ever materializing the full score matrix in GMEM — exactly the discipline [[gpu-memory-hierarchy]] demands.
