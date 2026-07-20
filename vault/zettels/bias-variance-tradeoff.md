---
title: Bias-variance tradeoff
tags: [ml, theory]
---

Two errors pull in opposite directions as the hypothesis space grows or shrinks.

**Approximation error** is what you lose by restricting the space at all: the best function in your space is still worse than the true one. Shrink the space and this gets worse.

**Estimation error** is what you lose by picking from that space using finite data rather than the distribution: you overfit the sample. Grow the space and this gets worse.

A larger space approximates better but overfits more easily, especially on small data. A smaller space is safer but may not be able to express the relationship at all. There is no setting that zeroes both, which is why this is a tradeoff and not a bug to be fixed.

This is the same tension as bias and variance in the classical framing: approximation error is bias, estimation error is variance. [[regularization-as-constraint]] is the usual dial. [[variance-reduction-by-averaging]] attacks the estimation side specifically, without shrinking the space.

## Related posts

- [[regularization]] — Regularization - Balancing Model Complexity and Overfitting
- [[intro-to-ensemble-methods]] — Introduction to Ensemble Methods
