---
title: Margin maximization
tags: [ml, theory]
---

If the data is linearly separable there are infinitely many separating hyperplanes. The perceptron returns whichever one it stumbles into. Most of them sit alarmingly close to some training point, and a hyperplane that barely clears the data it was trained on is unlikely to clear data it has not seen.

Margin maximization picks the one with the most clearance: maximize the distance from the boundary to the nearest point of either class. That turns an underdetermined problem into a unique solution, and it is a generalization argument, not an aesthetic one.

The scale of $w$ is arbitrary here (scaling $w$ and $b$ together leaves the boundary unchanged), so the usual move is to fix the functional margin at 1 and minimize $\|w\|^2$. Maximizing margin becomes minimizing weight norm, which is the same objective [[regularization-as-constraint]] describes. Max margin is L2 regularization wearing a different hat.

## Related posts

- [[max-margin-classifier]] — Understanding the Maximum Margin Classifier
- [[svm]] — Support Vector Machines(SVM) - From Hinge Loss to Optimization
