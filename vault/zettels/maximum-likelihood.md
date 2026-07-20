---
title: Maximum likelihood
tags: [ml, theory]
---

Given a parametric family of densities and a dataset, MLE picks the parameter under which the observed data is most probable. Not the most probable parameter, which is a different question, and the one [[bayesian-vs-frequentist]] turns on.

In practice you maximize the log-likelihood, because independence turns a product over data points into a sum, and sums are what optimizers and floating point both prefer.

The useful thing to notice is that MLE is often ERM in disguise. Maximizing log-likelihood under a Gaussian noise model is exactly minimizing squared error; under a Bernoulli model it is exactly minimizing log loss. Loss functions people write down by intuition usually turn out to be negative log-likelihoods of some noise assumption, which is worth knowing when choosing one. See [[empirical-risk-minimization]].

## Related posts

- [[mle]] — Generalized Linear Models Explained - Leveraging MLE for Regression and Classification
- [[probabilistic-modeling]] — Unveiling Probabilistic Modeling
