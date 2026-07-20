---
title: Variance reduction by averaging
tags: [ml, theory]
---

Average $n$ i.i.d. estimates and the variance drops by $n$ while the mean is unchanged. Less error, no added bias. The catch is i.i.d.: you have one dataset, not $n$.

Bagging fakes it. Resample the data with replacement, fit a model per bootstrap sample, average the predictions. The models are not independent, since the samples overlap, so the reduction falls short of the ideal $1/n$, but it is real.

This only pays off for high-variance, low-bias base learners. Averaging deep unpruned trees, which individually overfit badly, works well. Averaging linear models mostly wastes compute, since they were stable to begin with.

Random forests attack the leftover correlation directly: restrict each split to a random feature subset, so trees cannot all latch onto the same dominant predictor. More decorrelated, so the average is tighter. This is the [[bias-variance-tradeoff]] attacked from the variance side, and the mirror image of [[boosting-as-additive-modeling]].

## Related posts

- [[bagging]] — Bagging - Bootstrap Aggregation
- [[random-forest]] — Random Forests
- [[intro-to-ensemble-methods]] — Introduction to Ensemble Methods
