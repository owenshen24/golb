title: NHST notes

Things which are important:

1. This has been going on a for a long time?
   1. Were the original critiques 50 years ago the same as now?
2. Common pitfalls and why they seem intuitively correct.

Questions to ask:

1. What are some common examples of $P(H_0 | D)$ or <others> given typical settings? EX: legal, medical, business, industrial settings?
2. Have you had any experience with non NHST-methods? What was that experience like? (Was it intuitive? What were you able to infer? Was it still quantitative?)
3. What can we learn with from qualitative assessments? Dooes quantification still play an integral role in scientific analysis, given its pitfalls? How else can we do comparisons? Are comparisons even useful?

Activities:

1. Goodhart's Law leads to gaming metrics?
   1. Your favorite metric of choice likely won't make it
   2. What, then, to do?

---

Notes:

The **correct** definition of a p-value is $p(D|H_0)$. In other words, p-values tell us about the probabilties of seeing different data points (assuming an underlying state of the world). What we usually want is $P(H_0|D)$ or $P(H_A|D)$. We want something that tells us about the probabilities of different states of the world, given the data we see.

I think the confusing ones are where the two sides of the conditioning get swapped:

Incorrect interpretations focus on making the probabilities into something that we want:

* Probability that the null hypothesis is true (given the data we see) $P(H_0|D)$
  * mistaken p-value
* Probability that null hypothesis is true (given our decision to reject) $P(H_0 | \text{reject } H_0)$
  * mistaken $\alpha$

Other ones which seem pernicious:

* p-value is the magnitude of the effect size
  * small differences and large sample sizes can yield very small p-values
* if p-value is not significant, then effect size is zero
  * underpowered tests might not detect effect sizes
* keeping $H_0$ means the study failed
  * important to publish null results!
  * e.g. ESP, homeopathy, other scams

Null hypothesis is typically already false:

* If you assume this, then low p-value doesn't even tell you anything new.
* Often unrealistic assumptions being made

Publication bias:

* Overestimating effect sizes
  * If only studies past an acceptance threshold are published, averaging published data will be more misleading than averaging all data
* Assumes people are being honest. Faking data / selective reporting opens up another can of worms.

p-values are lossy compression:

* confidence intervals can help alleviate part of the issue
* but also, very different studies could yield similar p-values
  * small sample big effect
  * smal effect big sample

Go over extended example of P(H0|D) vs P(D|H0)

