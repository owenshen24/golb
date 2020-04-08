title: Why P-values Are Problematic
summary: As advertised.

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.11.0/dist/katex.min.css" integrity="sha384-BdGj8xC2eZkQaxoQ8nSLefg4AV4/AwB3Fj+8SUSo7pnKP6Eoy18liIKTPn9oBYNG" crossorigin="anonymous">

<script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.0/dist/katex.min.js" integrity="sha384-JiKN5O8x9Hhs/UE5cT5AAJqieYlOZbGT3CHws/y97o3ty4R7/O5poG9F3JoiOYw1" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.0/dist/contrib/auto-render.min.js" integrity="sha384-kWPLUVMOks5AQFrykwIup5lo0m3iMkkHrD0uJ4H5cjeGihAutqP0yW0J6dpFiVkI" crossorigin="anonymous"
    onload="renderMathInElement(document.body);"></script>
*(Notes: This content is adapted from [What's Wrong With Statistical Tests– And Where We Go From Here](/docs/whats-wrong-kline.pdf) by Rex B Kline and [The Earth Is Round (p < .05)](/docs/earth-round-cohen.pdf) by Jacob Cohen, from MSED 296C taught by [David Quarfoot](http://www.math.ucsd.edu/~dquarfoot/) at UCSD.)*

<hr>

Everyone knows that social scientists literally only want one thing, and it's disgusting:

$$p < 0.05$$

Jokes aside, many words have already been spilled about how evil stasticians can p-hack their way to a statistically significant result. (See, for example, the [interactive demo on 538](https://projects.fivethirtyeight.com/p-hacking/), or this [lengthy takedown](https://putanumonit.com/2016/04/17/022-power_skeptic/) of power posing by Jacob Falkovich). What I want to focus on in this essay is how the p-value can be misleading, even when everything is being honest. There are several tempting misconceptions about p-values, as well as several issues with null hypothesis significance testing as a whole, which I think are less noticeable, but just as problematic.

### p-values are about data, not hypotheses

Whenever we run a study, ideally, we'd like to use the data we get to inform our decision about which hypotheses could explain the data. One way to think about p-values is that they can represent the probability we can assign to some hypothesis (given some data).

Except this is wrong.

In significance testing, the p-value represents $P(D|H_0)$. This tells us how likely it is to for certain types of *data* (given some hypothesis is true). Even though what we usually want is $P(H_0|D)$, i.e. how likely it is for certain *hypotheses* (given that we've seen some data).

Now, with Bayes Theorem, we can see that $P(D|H_0)$ is related to $P(H_0|D)$, but they certainly aren't equal:

$$P(D|H_0) = \frac{P(H_0|D)P(D)}{P(H_0)}$$

Given, the p-value, we could try to derive an estimate for $P(H_0|D)$, if we had estimates for $P(H_0)$ and $P(D)$. But most papers don't get that far, and frequentist statistics doesn't emphasize priors anyway.

One reason it can be easy to mistake the two is due to a misapplication of the contrapositive rule from logical inference. 

Consider the following:

1. If you live in the USA, then you do not live in Russia.
2. You live in Russia.
3. Thus, you do not live in the USA.

Simple logical deduction, nothing wrong here. But, once the conditional in 1. becomes probabilistic, rather than certain, this type of reasoning breaks down.

Consider the following:

1. If you live in the USA, then you are unlikely to be the President.
2. You are the President.
3. Thus, you are unlikely to live in the USA.

This is wrong. If A makes B more probable, then the lack of B does not necessarily mean A is now *improbable*.

### p-values don't represent the magnitude of the effect size

Imagine three different interventions to improve student test scores, which are given by $N(\mu = 50, \sigma = 10)$.

For each of the three interventions, you run a study. Here are your results:

1. Intervention A: Sample size = 16, sample mean = 70
2. Intervention B: Sample size = 64, sample mean = 60
3. Intervention C: Sample size 256, sample mean = 55

Does the each intervention feel different?

The first intervention seems like it needs more information. Our initial results are quite promising with an effect size of 2, but we'll definitely need some larger samples to make a conclusion. 

The second intervention seems more credible, with a sizable sample size and some good results with an effect size of 1.

The last intervention seems quite convincing, with a large sample size and a reasonable effect size of 0.5.

Yet, all three of these studies would yield the exact same p-value of $6.2 \times 10^{-16}$.

Because the p-value is dependent on your sample size and your sample mean, it's a lossy representation. If it's very low, this is good evidence that your two groups are likely different, but you need more information that just the p-value in order to quantify just how different.

When low p-values are described as "significant", this comes with a lot of baggage associated with the way the word is used in everyday life. We usually use significant to mean something like influential, which sneaks in the asusmption of a large delta. But all a significant p-value tells us is that there is evidence of *an* effect, not necessarily a large one.

### p-value thresholds for publication lead to overestimation

In null hypothesis significance testing, scientists have to control for $\alpha$, the false positive rate or Type 1 error rate. In the social sciences, $\alpha$ is often set to be 0.05. Hence, $p < 0.05$. We might expect, then, that around 5% of published studies are false. Mildly worrying.

But it's actually much worse than that:

Imagine 100 honest scientists investigating whether or not homeopathy actually works (spoiler alert: it doesn't):

With $\alpha = 0.05$, we expect around 95 scientists to get null results and 5 scientists to get misleading positive results. Now, say these 5 scientists all publish their results and get accepted because they all honestly got $p < 0.05$, and all the journals care about are p-values and good research methodology (e.g. preregistering hypotheses).

Now, imagine doing a literature review of these published homeopathy studies. Now, it's not just 5% of published studies which are false, but 100% of them!

Having thresholds for publication means that we don't get to see the other 95 results–and, in this case, it's made painfully clear that we *need* to see those null results in order to get an accurate estimation of a field. 

In particular, assuming the typical $\alpha$ used in a field as the default false positive rate fails to take into account is the prior probability that any given study investigates a true relationship. In fields where real relationships are rare or data is vast, this does not bode well for published results, no matter how careful scientists are to avoid bias and measurement error. False positives can still vastly overshadow real results.

And of course it's not just the false positive rate. You can demonstrate similar overestimation results for effect size, confidence intervals, and other parameteres of interest.

### The null hypothesis is never true anyway

(Also see Gwern's [Everything is Correlated](https://www.gwern.net/Everything) for an in-depth literature review on this topic.)

Okay, so we just get everyone to publish their null results as well, so can stop skewing the literature, and we encourage good research methodology. Is that enough?

As you have likely guessed, no, no it's not enough.

The issue is that, for many studies, we *already know* the null hypothesis is false. Why? Because the real world never gives us perfect similarity between two groups. Look enough decimal points, and there will be a difference. 

In other words, if the z-score is given by $z = \frac{\bar{X}-\mu}{\frac{\sigma}{\sqrt{n}}}$, and $\bar{X}-\mu \ge \epsilon \ge 0$, we can get any z-score we want by making the sample size big enough.

This means that, for a large enough sample size, our significance tests will always output very small p-values (assuming null hypotheses which state two values are equal).

This raises two big issues.

The first is that, if we already know the result of running such a test with a massive sample, why even bother running the test in the first place with a smaller (read: feasible) sample? 

The second is that, if we admit that there is always *some* difference between our groups, then our false positive error rate becomes 0%. We'll never mistakenly conclude an exists when it doesn't because there's always *some* effect (though potentially small).

So we're locked into this weird limbo where we want our sample sizes to be large enough to rule out noise in our measurements–but not too large, such that the p-values are only small if the difference between the two groups is meaningful, i.e. a non-trivial effect.

### p-values should not be the main gatekeeper for journals

Despite decades of pushback, including a very recent [rebuke](https://amstat.tandfonline.com/doi/full/10.1080/00031305.2019.1583913) from the American Statistical Association, the $p < 0.05$ paradigm refuses to die. It's not just the journals. Other students in my course, who are in  education studies graduate courses have spoken about focusing on p-values. My first statistics class focused on p-values. Heck, even a recent [science-focused anime](https://www.crunchyroll.com/science-fell-in-love-so-i-tried-to-prove-it/episode-6-science-types-fell-in-love-so-they-tried-kissing-792895) showed it too.

To be clear, p-values *do*, at the very least, address sampling error, which is probably the only thing they have going for them. They can quantify the variation we might see in our samples and help identify when certain results are extreme. 

So that's useful at least.

(Except confidence intervals can do that too, and they're arguably more informative.)

(Please let the $p < 0.05$ paradigm die.)

