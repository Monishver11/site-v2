---
title: Notes
description: My zettelkasten — atomic notes and every blog post, connected.
---

Two kinds of note live here.

**Zettels** are atomic: one idea each, written to be linked rather than read in
order. There are only a few so far. This is the part that grows slowly.

**Post stubs** are a short entry for every post on the
[blog](https://monishver11.github.io/site-v2/blog/), pulled into the same graph.
The full text stays on the blog; the stub exists so the idea has a place here
and can be linked to.

To see how it all connects, open the graph panel and click the expand icon in
its corner. The sidebar view only shows what is near the note you are reading.

## Zettels

**Learning theory**

- [[empirical-risk-minimization]] — the proxy at the heart of supervised learning
- [[bias-variance-tradeoff]] — approximation error against estimation error
- [[regularization-as-constraint]] — why lasso is sparse and ridge is not
- [[convex-duality]] — the shadow problem, and where kernels become possible
- [[kernels-as-inner-products]] — a huge feature space you never build
- [[margin-maximization]] — L2 regularization wearing a different hat
- [[maximum-likelihood]] — and why your loss function was a likelihood all along
- [[bayesian-vs-frequentist]] — the same family of densities, two readings of it
- [[regret-minimization]] — what to optimize when there is no distribution
- [[boosting-as-additive-modeling]] — the idea underneath AdaBoost and gradient boosting
- [[variance-reduction-by-averaging]] — what bagging actually buys

**GPU and performance**

- [[gpu-memory-hierarchy]] — where every kernel optimization story begins
- [[arithmetic-intensity]] — whether a kernel can be compute-bound at all
- [[tiling]] — the reuse strategy under every fast kernel
- [[memory-coalescing]] — access pattern matters as much as access count
- [[cute-layouts]] — shape + stride as a first-class object
- [[wgmma]] — Hopper's asynchronous warpgroup MMA
- [[warp-specialization]] — a producer-consumer pipeline inside a block
- [[online-softmax]] — the trick that makes FlashAttention possible

**Systems**

- [[mapreduce-model]] — a restriction that buys distribution
- [[exactly-once-semantics]] — about effects, not deliveries

## Where to start reading

The posts are grouped into ordered threads. Each links to the next, so you can
follow a thread end to end:

- [[preface-ml]] — the ML foundations series, prerequisites through boosting
- [[gpu-intro]] — GPU fundamentals
- [[simons-gemm-notes]] — GEMM optimization
- [[cute]] — the CuTe DSL
- [[fa3-worklog]] — FlashAttention 3, kernel by kernel
- [[big-data-1-intro]] — big data systems
- [[silu-mul-fp8-block-quant-kernel-vllm]] — kernel work in vLLM
