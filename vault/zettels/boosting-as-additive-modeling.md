---
title: Boosting as additive modeling
tags: [ml, theory]
---

Fit a model as a sum of basis functions, $f(x) = \sum_m v_m h_m(x)$. Fitting all terms jointly is intractable for most bases, so forward stagewise additive modeling goes greedy: add one term at a time, choosing $(v_m, h_m)$ to best reduce the current loss, and never revisit the terms already placed.

That last clause is the whole method. Earlier terms are frozen, so each step is a small fit against the current residual rather than a global optimization.

Seeing this once collapses a lot of boosting into one idea. AdaBoost is FSAM with exponential loss, and its reweighting scheme falls out of the algebra rather than being a separate trick. Gradient boosting is FSAM where each new term fits the negative gradient of whatever differentiable loss you chose, which is what frees you from exponential loss and lets boosting do regression and ranking. Contrast [[variance-reduction-by-averaging]]: boosting reduces bias by adding terms sequentially, bagging reduces variance by averaging independent ones.

## Related posts

- [[fsam]] — Forward Stagewise Additive Modeling
- [[adaboost]] — Boosting and AdaBoost
- [[intro-gradient-boosting]] — Introduction to Gradient Boosting
- [[gradient-boosting]] — Gradient Boosting / "Anyboost"
