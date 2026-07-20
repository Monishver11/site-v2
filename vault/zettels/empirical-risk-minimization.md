---
title: Empirical risk minimization
tags: [ml, theory]
---

The thing we actually care about is the true risk: expected loss over the real data distribution. We cannot compute it, because we do not have the distribution, only a finite sample. So we minimize the empirical risk instead, the average loss on the sample, and hope the two are close.

That hope is the whole subject. Nothing guarantees it. Take a lookup table that memorizes every training point and returns garbage elsewhere: empirical risk zero, true risk terrible. ERM handed an unrestricted function space will find exactly that.

The fix is to not minimize over all functions. Restrict the hypothesis space, and the gap between empirical and true risk becomes controllable. That restriction is what [[bias-variance-tradeoff]] is about, and [[regularization-as-constraint]] is how it gets imposed in practice.

## Related posts

- [[erm]] — Empirical Risk Minimization (ERM)
- [[supervised-learning]] — Understanding the Supervised Learning Setup
- [[loss-functions]] — Loss Functions - Regression and Classification
