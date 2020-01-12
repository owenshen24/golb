title: Perceptron Convergence Proof

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.11.0/dist/katex.min.css" integrity="sha384-BdGj8xC2eZkQaxoQ8nSLefg4AV4/AwB3Fj+8SUSo7pnKP6Eoy18liIKTPn9oBYNG" crossorigin="anonymous">

<script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.0/dist/katex.min.js" integrity="sha384-JiKN5O8x9Hhs/UE5cT5AAJqieYlOZbGT3CHws/y97o3ty4R7/O5poG9F3JoiOYw1" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.0/dist/contrib/auto-render.min.js" integrity="sha384-kWPLUVMOks5AQFrykwIup5lo0m3iMkkHrD0uJ4H5cjeGihAutqP0yW0J6dpFiVkI" crossorigin="anonymous"
    onload="renderMathInElement(document.body);"></script>

Okay, so here's the setup for proving that the perceptron learning algorithm converges in the binary classification case. If this is new to you, the perceptron is a linear classifier as follows:

* $\hat{y} =  \text{sign}(w \cdot x)$
  * The perceptron is a linear combination of the input vector and outputs either $-1$ or $+1$.
* If $\hat{y}_t \not = y_t$ then we update $w_{k+1} = w_{k} + y_t(x_k)^T$
  * It's an iterative algorithm, where the first misclassified input is added to our weight vector on iteration $k+1$ and then we iterate again.
* $w_1 = 0$
  * We initialize the starting weight vector to the zero vector.

For this proof, we'll assume a few things:

* There exists an optimal $w = w^*$ such that for some $\epsilon > 0$, it's the case that $y_i(w^* \cdot x_i) > \epsilon$ for all inputs on the training set.
  * In other words, we assume that there is a margin of at least $\epsilon$ and that a solution exists.
* $||w^*|| = 1$
  * This gives us a unique weight vector.
* For all $x_1, x_2, ... \in X$, it's the case that $||x_i|| \le R$.
  * We're upper bounding the norm of the data points in our training set.



To start, we show that $w_{k+1} \cdot (w^*)^T \ge k \epsilon $ with a proof by induction.

Base case where $k = 0$:
$w_{0+1}\cdot (w^*)^T =  0 \ge 0 \cdot \epsilon $

Inductive step where $k \to k+1$:
$w_{k+1}\cdot (w^*)^T = (w^k + y_t(x_t)^T)\cdot (w^*)^T$ (WLOG, we assume that $x_t$ is the first misclassified input)
$= w^k \cdot (w^*)^T + y_t (w^* \cdot x_t)$
$ \ge (k-1)\cdot \epsilon + \epsilon$ (Using the inductive hypothesis, and the definition of $w^*$)
$ \ge k \epsilon$ 

Next, we show that $||w_{k+1}|| \ge k \epsilon​$
$w_{k+1} \cdot w^* = ||w_{k+1}|| \times ||w^*|| \times \text{cos}(\theta)​$ where $\theta​$ is the angle between $w_{k+1}​$ and $w^*​$
Because $cos(\theta) \le 1​$, $||w_{k+1}|| \times ||w^*|| \ge w_{k+1} \cdot (w^*)^T​$
​Thus $||w_{k+1}|| \times ||w^*|| \ge k \epsilon​$
Finally because $||w^*|| = 1​$ by definition, $||w_{k+1}|| \ge k \epsilon​$



Now we notice that $||w_{k+1}||^2 = ||w_{k} + y_t (x_t)^T||^2$
$= ||w_k||^2 + 2y_t (w_k \cdot x_t) + ||x_k||^2$
$\le ||w_k||^2 + ||x_k||^2$ because by definition $\text{sign}(y_t(w_k \cdot x_t)) = -1$ as it is the first misclassified input, so $2y_t(w_k \cdot x_t) < 0$.
$\le ||w_k||^2 + R^2$ because by definition $||x_i|| \le R$

Next we show that $||w_{k+1}||^2 \le kR^2$ with a proof by induction.

Base case where $k = 0$
$||w_{0+1}||^2 = 0 \le 0(R)$

Inductive step where $k \to k+1$

By the above part, we know that $||w_{k+1}||^2 \le ||w_k||^2 + R^2$.
Now, by the inductive hypothesis, we see that $||w_{k+1}|| \le (k-1)R^2 + R^2 = kR^2$.



Thus, we have the full inequality:
$k^2 \epsilon^2 \le ||w_{k+1}||^2 \le kR^2$

And thus we can see that $k \le \frac{R^2}{\epsilon^2}$, bounding the number of iterations we run our algorithm by the margin and the farthest point.

