---
title: Regularization as a constraint
tags: [ml, optimization]
---

Regularization has two equivalent readings. The penalty form adds $\lambda \Omega(w)$ to the objective. The constraint form minimizes the loss subject to $\Omega(w) \le r$. For each $\lambda$ there is an $r$ giving the same solution, and the constraint form is the one that makes the behaviour obvious.

Picture the constraint as a region the weights must stay inside. The loss contours push outward; the solution sits where they first touch the region. L2 gives a ball, which has no corners, so the touch point generically has every coordinate nonzero: everything shrinks, nothing vanishes. L1 gives a cross-polytope whose corners lie on the axes, and corners are exactly where coordinates are zero. That geometry, not the algebra, is why lasso is sparse and ridge is not.

So L1 does feature selection and L2 does shrinkage. Both are ways of limiting the hypothesis space from [[bias-variance-tradeoff]] without changing the model family.

## Related posts

- [[regularization]] — Regularization - Balancing Model Complexity and Overfitting
- [[l1-l2-reg-indepth]] — L1 and L2 Regularization - Nuanced Details
