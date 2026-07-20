---
title: Bayesian vs frequentist
tags: [ml, theory]
---

Both start in the same place: a parametric family of densities, one distribution per parameter value. They disagree about what the parameter is.

The frequentist treats $\theta$ as fixed and unknown, and the data as random. Estimators are random variables, so you talk about their bias and variance over hypothetical repeated samples. [[maximum-likelihood]] is the canonical move.

The Bayesian treats $\theta$ as a random variable with a prior, and the observed data as fixed once seen. Bayes' rule turns prior plus likelihood into a posterior, and the answer is that whole distribution, not a point.

The practical difference shows up with little data. A point estimate from three samples tells you nothing about how much to trust it; a posterior is visibly wide. It also gives you a principled place to put what you knew beforehand, which is either the main attraction or the main objection depending on who you ask.

## Related posts

- [[bayesian-ml]] — Bayesian Machine Learning - Mathematical Foundations
- [[bayes-point-estimate]] — Conjugate Priors and Bayes Point Estimates
- [[bayes-decision-theory]] — Bayesian Decision Theory - Concepts and Recap
