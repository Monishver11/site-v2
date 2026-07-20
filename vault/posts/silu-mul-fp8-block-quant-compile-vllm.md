---
title: "SiLU+Mul+FP8 Block Quant Pattern Matching Pipeline - vLLM Notes"
date: 2026-03-25
tags: [GPU, post]
---

Detailed walkthrough of vLLM's torch.compile pattern matching pipeline that fuses SiLU+Mul and FP8 block quantization into a single kernel launch, covering FX graphs, matchers, and the dispatch machinery

Full post: [SiLU+Mul+FP8 Block Quant Pattern Matching Pipeline - vLLM Notes](https://monishver11.github.io/site-v2/blog/silu-mul-fp8-block-quant-compile-vllm/) · GPU & Performance

## Related

- [[silu-mul-fp8-block-quant-kernel-vllm]] — previous in vLLM work
- [[eagle-test-dp]] — next in vLLM work

<!-- links below this line are kept when regenerating -->
