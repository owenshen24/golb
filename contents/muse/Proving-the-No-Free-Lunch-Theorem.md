title: Proving the No-Free-Lunch Theorem

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.css" integrity="sha384-zB1R0rpPzHqg7Kpt0Aljp8JPLqbXI3bhnPWROx27a9N0Ll6ZP/+DiW/UqRcLbRjq" crossorigin="anonymous">

  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.js" integrity="sha384-y23I5Q6l+B6vatafAwxRu/0oK/79VlbSz7Q9aiSZUvyWYIYsd+qj+o24G5ZU2zJz" crossorigin="anonymous"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/contrib/auto-render.min.js" integrity="sha384-kWPLUVMOks5AQFrykwIup5lo0m3iMkkHrD0uJ4H5cjeGihAutqP0yW0J6dpFiVkI" crossorigin="anonymous"
      onload="renderMathInElement(document.body);"></script>

The No-Free-Lunch Theorem is an important part of statistical learning theory. I'm going to trace the proof found in *Understanding Machine Learning* for my own benefit.

The theorem is this:

Say there is a learning algorithm A which outputs a binary classifier and has the 0-1 loss function over a domain $X$. Then, there exists a distribution $D$ over $X \times \{0,1\}$ such that:

1. There exists a function $f: X \to \{0,1\}​$ with $L_D(f) = 0​$. That is, there is some binary function over $X​$ such that the expected loss of $f​$ over $D​$ is 0, meaning there is some function which will correctly classify all the points.

2. With probability of at least $\frac{1}{7}$ over the choice of $S \sim D^m$ $L_D(A(S)) \ge \frac{1}{8}$. In other words, for at least $\frac{1}{7}$ of all possible training sets of size $m$ from $D$, the expected loss of output of the training algorithm on the training set is at least  $\frac{1}{8}$.

### Proof:

Let $C \subseteq X$ such that $|C| = 2m$. We note that there are $T = 2^{2m}$ possible functions from $C$ to $\{0,1\}$.  Let $D_i$ be the distribution over $D$ that only assigns probability to the $(x,f_i(x))$ pairs for the corresponding function.

We're going to show that:

$\underset{i \in [T]}{\text{max }} \underset{S \sim D_i^m}{\mathbb{E}} [L_{D_i}(A(S))] \ge 1/4$

That is, the largest expected loss of running our learning algorithm on a training set of size $m$ among all functions from $C$ to $\{0,1\}$ (or rather, the distribution that is defined only on the function's $(x, f(x))$ pairs) is 1/4.

When a random variable is between 0 and 1, we can use Markov's inequality to show that:

$P(X \ge a) \ge \frac{\mathbb{E}[X]-a}{1-a}$

Applying that to our inequality above, we see that:

$P(L_D(A'(S)) \ge \frac{1}{8}) \ge \frac{\frac{1}{4}-\frac{1}{8}}{\frac{7}{8}} \ge \frac{1}{7}$ as desired.

So now we just have to prove the inequality itself.

Well, what do we know about the expected loss for a given distribution and a learning algorithm? It's just the averaged loss, over all possible choices of a training set:

$\underset{S \sim D_i^m}{\mathbb{E}}[L_{D_i}(A(S))] = \frac{1}{k}\sum_{j=1}^kL_{D_i}(A(S^i_j))$

And we care about taking the maximum among all possible distributions, which is greater than the average loss among all distributions, which is greater than the minimum value:

$\underset{i \in [T]}{\text{max }} \frac{1}{k}\sum_{j=1}^kL_{D_i}(A(S^i_j))$ 

$\ge \frac{1}{T}\sum^T_{i=1}\frac{1}{k}\sum^k_{j=1}L_{D_i}(A(S^i_j))​$

$=\frac{1}{k}\sum^k_{j=1}\frac{1}{T}\sum^T_{i=1}L_{D_i}(A(S^i_j))​$

$\ge \underset{j \in [k]}{\text{min }} \frac{1}{T}\sum_{i=1}^TL_{D_i}(A(S^i_j))$

(To be clear, the last inequality refers to the lowest cost possible among all possible training sets, averaged across all possible distributions.)

Next, let's fix some $j \in [k]$. $S_j = (x_1,..,x_m)$. Let $(v_1, ...,v_p)$ be the examples in $C$ that aren't in $S_j$. We can see that $p \ge m$.

Thus:

$L_{D_i}(h) = \frac{1}{2m}\sum_{x\in C}\mathbf{1}[h(x) \not= f_i(x)]$

$\ge \frac{1}{2p}\sum_{j=1}^p\mathbf{1}[h(v_j) \not= f_i(v_j)]$

Combining our two inequalities, we get:

$ \frac{1}{T}\sum_{i=1}^TL_{D_i}(A(S^i_j)) \ge \frac{1}{T}\sum_{i=1}^T \frac{1}{2p}\sum_{j=1}^p\mathbf{1}[h(v_j) \not= f_i(v_j)]$

$ = \frac{1}{2p}\sum_{j=1}^p\frac{1}{T}\sum_{i=1}^T \mathbf{1}[h(v_j) \not= f_i(v_j)]$

$\ge \frac{1}{2}\underset{r \in [p]}{\text{min}}\frac{1}{T}\sum_{i=1}^T \mathbf{1}[h(v_j) \not= f_i(v_j)]$

Now, fix a point $v_r \in [p]$. Notice that we can partition $[T]$ into $(f_a, f_b)$ pairs such that $f_a$ and $f_b$ agree on every value except for $v_r$. We can do this because $[T]$ is the set of all functions, so we can imagine fixing $f(v_r) = 0$ and letting all the other values vary, as well as fixing $f(v_r) = 1$ and doing the same thing. It's clear this will give us two sets of equal size, as well as enable the above pairing.

This means that:

$\mathbf{1}[h(v_j) \not = f_a(j)] + \mathbf{1}[h(v_j) \not = f_b(j)] = 1$, which means that the average loss for the pair of functions is $\frac{1}{2}$.

Thus, $\frac{1}{2}\underset{r \in [p]}{\text{min}}\frac{1}{T}\sum_{i=1}^T \mathbf{1}[h(v_j) \not= f_i(v_j)] = \frac{1}{4}$

Thus, $\underset{i \in [T]}{\text{max }} \frac{1}{k}\sum_{j=1}^kL_{D_i}(A(S^i_j)) \ge \frac{1}{4}$ as desired.

