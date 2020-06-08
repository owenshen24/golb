title: An Illustrated Proof of the No Free Lunch Theorem

 <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.11.0/dist/katex.min.css" integrity="sha384-BdGj8xC2eZkQaxoQ8nSLefg4AV4/AwB3Fj+8SUSo7pnKP6Eoy18liIKTPn9oBYNG" crossorigin="anonymous">

<script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.0/dist/katex.min.js" integrity="sha384-JiKN5O8x9Hhs/UE5cT5AAJqieYlOZbGT3CHws/y97o3ty4R7/O5poG9F3JoiOYw1" crossorigin="anonymous"></script>

<script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.0/dist/contrib/auto-render.min.js" integrity="sha384-kWPLUVMOks5AQFrykwIup5lo0m3iMkkHrD0uJ4H5cjeGihAutqP0yW0J6dpFiVkI" crossorigin="anonymous"
onload="renderMathInElement(document.body);"></script>


### Introduction

This essay is an illustrated proof of the No Free Lunch (NFL) theorem; the NFL theorem has many variants, which all say slightly different things. The [most famous one](https://en.wikipedia.org/wiki/No_free_lunch_theorem) says, roughly, that every learning algorithm has the same performance, when averaged across all possible target functions. In other words, there is no universal learning algorithm that outperforms every other algorithm on every learning task.



Throughout this essay, I'm going to be refering to a "learning algorithm". If you're unfamiliar, in the machine learning context, a learning algorithm is an algorithm that takes in $S$, a series of (x,y) pairs, i.e. our training data or training set, from some target function and outputs a hypothesis, which is a function that tries to be close to the original target function. Note that the inputs and outputs aren't necessarily  binary, but it's easier to illustrate them as such, and the proof is not affected. Learning algorithms are often evaluated by looking at the error rate, which in the case of classification, is the proportion of $(x,y)$ pairs it predicts incorrectly.



<img src="/images/hypothesis.svg">



In this essay, I will focus on an easier NFL theorem (from [Understanding Machine Learning by Shai Shalev-Shwartz and Shai Ben-David](https://www.cse.huji.ac.il/~shais/UnderstandingMachineLearning/index.html)) which says, roughly, for any learning algorithm that outputs a binary function, there exists a distribution that will cause it to output a hypothesis with a high error rate, even when there exists another function that can achieve 0 error on the distribution. In other words, for every learning algorithm, we can find a distribution that can trip up the learning algorithm.



How do we formalize this? 



The NFL theorem we're going to prove states that:



Say we have a learning algorithm A which outputs a binary classifier (this is our hypothesis) over a domain $X$. 



Next, let's define an error or loss function, which will tell us how well our output hypothesis does on the actual distribution. We'll use the **1** loss function $L$ which, when given two inputs, outputs 0 if the two values match, otherwise it outputs 1. Then, there exists a distribution $D$ over $X \times \{0,1\}$ (i.e. a distribution over possible $(x,\{0,1\})$ values) such that:



1. There exists a function $f: X \to \{0,1\}$ with $L_D(f) = 0$. That is, there is some binary function over $X$ such that the expected loss of $f$ over $D$ is 0. In other words, there is some function which will correctly classify all the points in our distribution correctly.
   

2. With probability of at least $\frac{1}{7}$ over the choice of $S \sim D^m$ $L_D(A(S)) \ge \frac{1}{8}$. In other words, for at least $\frac{1}{7}$ of all possible training sets of size $m$ from $D$, the expected loss of output of the training algorithm on the training set is at least  $\frac{1}{8}$. (Note that our loss function is defined here as the average **1** loss across all points in the distribution).
   

3. The distribution $D$ is defined over $2m$ points, so our training set will consist of at most $m$ unique values, i.e. half of the distribution's points. 



<img src="/images/nfl-base.svg">



To prove this, we are actually going to prove something different, but equivalent. Instead, we are going to prove that:



 $\underset{i \in [T]}{\text{max }} \underset{S \sim D_i^m}{\mathbb{E}} [L_{D_i}(A(S))] \ge 1/4$



That is, if we run our learning algorithm on training sets of size $m$, across a family of distributions $D_1-D_T$, the largest such expected loss will be at least $\frac{1}{4}$. In other words, we will show that at least one distribution $D_i$ from this group will trip up our algorithm.



<img src="/images/dist-one-fourth-error.svg">



To see how these two statements are equivalent, we just apply a modified version of [Markvov's inequality](https://en.wikipedia.org/wiki/Markov%27s_inequality). This lower bounds how likely a random variable is to be greater than some value:



$P(X \ge a) \ge \frac{\mathbb{E}[X]-a}{1-a}$



Applying that to our inequality above, we see that:



$P(L_{D_i}(A(S)) \ge \frac{1}{8}) \ge \frac{\frac{1}{4}-\frac{1}{8}}{\frac{7}{8}} \ge \frac{1}{7}$ as desired. So now we just need prove this new inequality.



Before that, here's the intuition for why this inequality is true:



First, our learning algorithm only gets half of all possible points as its training set. This means our algorithm knows nothing about the labels of the other half of the points. Now, if we assume that every function over these unknown points is equally likely, then each point is either 1 or a 0. This means that our algorithm can only guess for these unknown points, which makes its expected error rate 0.5. So in the best case, it'll still get an error rate of 0 on the half it sees and 0.5 on the half it doesn't see, which makes its overall error 0.25.



<img src="/images/seen-unseen-data.svg">



### The Proof

Now, let's begin the proof.



Let $C \subseteq X$ such that $|C| = 2m$. So it's a subset of our input space that's of size $2m$. 



Notice that there are $T = 2^{2m}$ possible functions from $C$ to $\{0,1\}$.  Let $D_i$ be the distribution over $D$ that only assigns probability to the $(x,f_i(x))$ pairs for the corresponding function. This captures the idea that our input space $C$ is twice the size of our training set, and that each function is equally likely. 



Each function is now turned into a probability distribution that places $\frac{1}{|C|}$ probability if the given $(x,y)$ point is one of the function's input/output pairs, and 0 probability otherwise. So each unique function has a unique distribution associated with it.



<img src="/images/function-dist.svg">



Recall that we're trying to calculate $\underset{i \in [T]}{\text{max }} \underset{S \sim D_i^m}{\mathbb{E}} [L_{D_i}(A(S))]$, i.e. the expected loss over all possible training examples, with regards to the distribution that maximizes this loss. 



For any given distribution,  $\underset{S \sim D_i^m}{\mathbb{E}} [L_{D_i}(A(S))]$ is the loss for a given training set, averaged over all possible choices of training data. 



If our input space consists of $2m$ points and our training data consists of a sequence of $m$ points, then there are $k = (2m)^m$ possible sequences. 



Below, we'll let $S_i^j$ be the $i^{th}$ possible sequence of training data, labeled with the $j^{th}$ possible function. 



<img src="/images/sij.svg"> 



Thus, we know that $\underset{S \sim D_i^m}{\mathbb{E}}[L_{D_i}(A(S))] = \frac{1}{k}\sum_{j=1}^kL_{D_i}(A(S^i_j))$. In other words, for any one given distribution of data, the expected loss of our learning algorithm (across all training data sets) is equal to the expected loss if we take $m$ training points, averaged across all possible functions that could label the data.



<img src="/images/one-distr-error.svg"> Recall that, from above, we care about taking the **maximum** error across all possible distributions; by definition, this will be at least as big as the average loss across all distributions. Thus, we know that:



$\underset{i \in [T]}{\text{max }} \frac{1}{k}\sum_{j=1}^kL_{D_i}(A(S^i_j)) \ge \frac{1}{T}\sum^T_{i=1}\frac{1}{k}\sum^k_{j=1}L_{D_i}(A(S^i_j))$



<img src="/images/sum-distr-training.svg"> 



Next, it doesn't really matter if we take the average over all distributions first or the average over all training sets first. Thus, we can switch the order of the summations to get the same value:



$\frac{1}{T}\sum^T_{i=1}\frac{1}{k}\sum^k_{j=1}L_{D_i}(A(S^i_j)) =\frac{1}{k}\sum^k_{j=1}\frac{1}{T}\sum^T_{i=1}L_{D_i}(A(S^i_j))$



<img src="/images/sum-training-distr.svg">



Now, if we're taking the loss averaged over all training data, notice that this will necessarily have to be at least as big as the loss given by the training data which leads to the **smallest** average loss. 



Thus, we can replace our inequality with a smaller, simpler one. Our inequality has to be at least as large as the average loss (across all functions) when applied to that specific training set.



$\frac{1}{k}\sum^k_{j=1}\frac{1}{T}\sum^T_{i=1}L_{D_i}(A(S^i_j)) \ge \underset{j \in [k]}{\text{min }} \frac{1}{T}\sum_{i=1}^TL_{D_i}(A(S^i_j))$



<img src="/images/one-training-error.svg"> 



So we've been abstractly talking about the loss function for a while now. What does $L_{D_i}(h)$ actually represent? We want it to be how well our hypothesis does on a specific distribution $D_i$. One straightforward way to formalize this is to just go through all $(x,y)$ pairs in $D_i$ and take the average **1** loss between $y$ and $h(x)$:



$L_{D_i}(h) = \frac{1}{2m}\sum_{x\in C}\mathbf{1}[h(x) \not= f_i(x)]$



<img src="/images/loss.svg">



Next, let's fix some $j \in [k]$, which has $m$ training examples given by $S_j = (x_1,..,x_m)$. Let $(v_1, ...,v_p)$ be the examples in $C$ (all data points) that **aren't** in $S_j$. We can see that $p \ge m$ because at most we have half the data from the distribution, which is when we have no duplicates.



<img src="/images/p-data.svg"> 



Thus:



$L_{D_i}(h) =\frac{1}{2m}\sum_{x\in C}\mathbf{1}[h(x) \not= f_i(x)] \ge \frac{1}{2p}\sum_{j=1}^p\mathbf{1}[h(v_j) \not= f_i(v_j)]$



<img src="/images/loss-p.svg"> 



In other words, the average loss over all points in the distribution is at least half of the average loss over all points **not** in the training set. 



Now, we can substitutue this in for $L_{D_i}$ from our inequality earlier to get:



$ \frac{1}{T}\sum_{i=1}^TL_{D_i}(A(S^i_j)) \ge \frac{1}{T}\sum_{i=1}^T \frac{1}{2p}\sum_{j=1}^p\mathbf{1}[h(v_j) \not= f_i(v_j)]$



So now we're taking the loss across all functions, across all points in $(v_1,...,v_p)$. Like before, we can swap the order of the summations:



$ \frac{1}{T}\sum_{i=1}^T \frac{1}{2p}\sum_{j=1}^p\mathbf{1}[h(v_j) \not= f_i(v_j)] =\frac{1}{2p}\sum_{j=1}^p\frac{1}{T}\sum_{i=1}^T \mathbf{1}[h(v_j) \not= f_i(v_j)]$



<img src="/images/sum-p-dist.svg">



Once again, we can upper bound this inequality by noticing that the average loss across all points in $(v_1,...,v_p)$ and across all functions has to be at least the loss of the point $v_r$ which we assume to be the point which gives the minimal loss:



$\frac{1}{2p}\sum_{j=1}^p\frac{1}{T}\sum_{i=1}^T \mathbf{1}[h(v_j) \not= f_i(v_j)] \ge \frac{1}{2}\underset{r \in [p]}{\text{min}}\frac{1}{T}\sum_{i=1}^T \mathbf{1}[h(v_r) \not= f_i(v_r)]$



<img src="/images/one-p-error.svg">



Now, notice that we can partition $[T]$ into $(f_a, f_b)$ pairs such that $f_a$ and $f_b$ agree on every value except for $v_r$. We can do this because $[T]$ is the set of all functions, so we can imagine fixing $f_a(v_r) = 0$ and letting all the other values vary, as well as fixing $_bf(v_r) = 1$ and doing the same thing. It's clear this will give us two sets of equal size, as well as enable the above pairing.



<img src="/images/t-split.svg">



This means that:



$\mathbf{1}[h(v_j) \not = f_a(j)] + \mathbf{1}[h(v_j) \not = f_b(j)] = 1$, which means that the average loss for the pair of functions is $\frac{1}{2}$. After all, for each pair, our hypothesis can only get one of them right, making the overall error half.



<img src="/images/t-split-error.svg"> 



Thus, we can substitutue $\frac{1}{2}$ for $\sum _{i=1}^T\mathbf{1}[h(v_j) \not = f_i(v_j)]$ into our above inequality and get:



 $\frac{1}{2}\underset{r \in [p]}{\text{min}}\frac{1}{T}\sum_{i=1}^T \mathbf{1}[h(v_j) \not= f_i(v_j)] = \frac{1}{2} ( \frac{1}{2}) = \frac{1}{4}$



And because we've been only taking upper bounds this whole time, our final value of $\frac{1}{4}$ applies to our initial inequality.



Thus, $\underset{i \in [T]}{\text{max }} \frac{1}{k}\sum_{j=1}^kL_{D_i}(A(S^i_j)) \ge \frac{1}{4}$ as desired.



<img src="/images/dist-one-fourth-error.svg">



### Conclusion

So, to summarize, for **any** learning algorithm, we wanted to show that there exists a distribution where it performs poorly in terms of a high expected loss. We started by considering a set of distributions that mapped onto the set of all binary functions from our input space. We upper-bounded this by considering the average across all distributions (and training sets). We then showed that the loss was then upper bounded by considering the training set with minimal loss and averaged across all possible distributions, which had to be at least one half due to our partition argument. Plugging this back in gave us $\frac{1}{4}$ like we wanted. Finally, we can reverse our initial steps and use Markov's Inequality, which gets us the theorem in its original form.

All in all, this isn't very complicated, despite the mess of inequalities, and the proof basically all hinges on the combinatorial properties of looking at the set of all possible binary functions. 

If every learning algorithm has its Kryptonite in the form of some distribution (i.e. function), then what explains the major differences in performance that we see in practice? Why do certain algorithms appear to do better than others? 

One lesson from the disconnect between empirical results and the No Free Lunch Theorem is that our search space is often more constrained than we think. We're basically never actually searching over the set of all possible functions. Real life often doesn't give us such adversarial distributions, and because of this, we often have informative priors about what the end result should look like. This often looks like a bias towards simplicity, which regularization can help enforce. 