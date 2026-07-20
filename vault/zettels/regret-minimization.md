---
title: Regret minimization
tags: [ml, theory]
---

Online learning drops the assumption that data is drawn i.i.d. from a fixed distribution. Examples arrive in sequence, possibly chosen adversarially, and you predict on each before seeing the answer. Without a distribution, true risk is not even definable, so the usual goal is gone.

Regret replaces it: your cumulative loss minus the cumulative loss of the best fixed strategy in hindsight. It is a relative measure, which is what makes it work against an adversary. You are not promising to do well in absolute terms, only to not do much worse than the best single strategy you could have committed to from the start.

The target is sublinear regret, $o(T)$. Then average regret per round tends to zero and you are asymptotically as good as the best fixed strategy, whatever the sequence was. Bounds of this shape are why guarantees survive without any distributional assumption at all.

## Related posts

- [[online-learning]] — Online Learning in ML - A Beginner’s Guide to Adaptive Learning
- [[wma]] — Understanding the Weighted Majority Algorithm in Online Learning
- [[online-to-batch]] — On-line to Batch Conversion
