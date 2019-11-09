title: Mathematics for Machine Learning
summary: Working through mml-book and Deep Learning.

I need to brush up on my formal understanding as well as the intuitions behind the maths in machine learning. To that end, I'll be working through exercises in Mathematics for Machine Learning as well as summarizing chapters.

# Assorted Notes:

- Hessians and the 2nd degree Taylor expansion:
  - Taylor's theorem tells us how we can approximate a differentiable function.
  - More specifically, as the Hessian represents the matrix of second derivatives, we're typically talking about quadratic approximations.
  - Specifically: $f(a) + f'(a)(x-a) + \frac{f''(a)}{2}(x-a)^2$.
  - Ah, furthermore, as the Hessian can be used in the 2nd derivative test, we know that if the Hessian is positive definite, then we're at a local minima.



- Hessians, diagonalization, and eigenvectors: