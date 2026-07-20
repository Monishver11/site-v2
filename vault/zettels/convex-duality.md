---
title: Convex duality
tags: [ml, optimization]
---

Every constrained minimization has a shadow problem. Fold the constraints into the objective with multipliers to get the Lagrangian, minimize over the primal variables, and what remains is the dual, a maximization over the multipliers.

The dual is always a lower bound on the primal. For a well-behaved convex problem the bound is tight, so solving either one solves both. That is worth something computationally, since the dual can be much smaller: for an SVM the primal has one variable per feature, the dual has one per training point.

The bigger payoff is structural. The dual of the SVM depends on the data only through inner products between training points, never through the points themselves. That is precisely the opening [[kernels-as-inner-products]] needs. KKT conditions also drop out here, and they are what makes most dual variables zero, leaving only the support vectors.

## Related posts

- [[dual-problem]] — The Dual Problem of SVM
- [[svm-dual-problem]] — Demystifying SVMs - Understanding Complementary Slackness and Support Vectors
