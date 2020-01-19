title: Perceptron Musings

Thinking about why the Voted Perceptron works well. It works because if you have data that's generally linearly separable, then the weights which have survived the longest are a good proxy for the true value. Similarly, if you instead run each updated set of weights against the entire dataset, you can probably get a good indication for how well a set of weights is doing.

But this seems sort of artificial, mainly because I just flipped a few points. It seems like a better version of this is to try it ona dataset with some actual inherent nonlinearity, e.g. some Gaussians or something like that.

Otherwise, maybe some sort of ensemble method that uses a decision tree to decide which perceptron to apply...? That's a little extreme...

Anyway, the other thing with the delta trick seems too complex, in that it could easily blow up your dimensionality...and I'm still confused about what the curse of dimensionality is about...

But anyhow, I think the next thing to do is to run the delta trick perceptron and see if it can classify all of the points correctly. That's of course good for reducing empirical risk, but it feels pretty brittle, especially if it's really just noise...but maybe it'd be good for actually nonlinear datasets.

Anyway, this is what I want to do:

1. Implement the delta trick. See what it looks like.
   1. See if it can classify everything correctly.
2. Add Voted Perceptron visualization to the website.