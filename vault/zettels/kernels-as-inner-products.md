---
title: Kernels as inner products
tags: [ml, theory]
---

Map your data into a richer feature space and a linear model there is nonlinear back here. The problem is that useful feature spaces are enormous, and writing down $\phi(x)$ explicitly is hopeless.

The escape is that some algorithms never need $\phi(x)$ itself, only $\langle \phi(x), \phi(x') \rangle$. A kernel computes that inner product directly from $x$ and $x'$, at the cost of the original dimension, with the feature space never materialized.

The degree-2 polynomial kernel $(x^\top x' + 1)^2$ is the clean example: expand it and you get every pairwise product of coordinates, a quadratically large feature space, computed in the time of one dot product plus a square.

This only works for algorithms already written in terms of inner products, which is why [[convex-duality]] comes first. The dual SVM qualifies; the primal does not.

## Related posts

- [[kernel-trick]] — Understanding the Kernel Trick
- [[feature-maps]] — Unleashing the Power of Linear Models - Tackling Nonlinearity with Feature Maps
- [[svm-solution-span-of-data]] — SVM Solution in the Span of the Data
