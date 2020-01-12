title: Neural Networks 1
summary: Writing a neural net in Python, covers forward pass and backpropagation code and derivations.

# Introduction
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.11.0/dist/katex.min.css" integrity="sha384-BdGj8xC2eZkQaxoQ8nSLefg4AV4/AwB3Fj+8SUSo7pnKP6Eoy18liIKTPn9oBYNG" crossorigin="anonymous">

<script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.0/dist/katex.min.js" integrity="sha384-JiKN5O8x9Hhs/UE5cT5AAJqieYlOZbGT3CHws/y97o3ty4R7/O5poG9F3JoiOYw1" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.0/dist/contrib/auto-render.min.js" integrity="sha384-kWPLUVMOks5AQFrykwIup5lo0m3iMkkHrD0uJ4H5cjeGihAutqP0yW0J6dpFiVkI" crossorigin="anonymous"
    onload="renderMathInElement(document.body);"></script>

This post will explain how to write a neural network in Python. I am obviously not the first person to do this. Almost all of the code is here adapted from Michael Nielsen's fantastic online book [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/chap2.html). [Victor Zhou also has a great tutorial in Python](https://victorzhou.com/series/neural-networks-from-scratch/). Why am I trying to do the same? Partially, it's for my own benefit, cataloging my code so I can refer back to it later in a form more captivating than a mere docstring. Also partially, I think I can share a few intuitions which make the backpropagation equations a lot easier to derive. 

Okay, so here's a typical picture of a neural network:

![basic neural net image](/images/simple_nn.svg)

If you're new to all this: A neural network is a function that takes in an input vector (or matrix) and outputs another vector (or matrix). The input starts at the leftmost vertical layer of nodes and then gets transformed, via a series of operations, to the rightmost vertical layer of nodes. Each layer is a linear combination of the layer before it, followed by an activation function, which is applied to element-wise to each node in the layer. In other words, a neural net is parameterized by a series of weight matrices $W_1,W_2,..$, a series of bias vectors, $b_1,b_2,...$, and an activation function $a$ (typically a nonlinear function like $tanh(x)$).

The typical picture, while good for representing the general idea of a neural net, does not do a good job of showing the different operations being performed. I prefer representing a neural net as a computational graph, like below:

![a graph with nodes, one after another](/images/computational_graph.svg)

Here, it's clearer to see how each node is a function of the step before it. A normal three-layer neural network is given by the following composition of functions:

$f_0 = X = \text{input}$

$f_1 = W_1\cdot f_0 + b_1$

$f_2 = a(f_1)$

$f_3 = W_2 \cdot f_2 + b_2$

$f_4 = a(f_3) = \hat{Y} = \text{predicted output}$

This recursive definition will make it easy to derive the backpropagation algorithm, which we'll use to train our network. It also allows us to easily unroll the function, if we want to see what's going on in on line, by substituting until we get back to the input:

$f_4 = a(W_2 \cdot (a(W_1 \cdot f_0 + b_1) + b_2))$

And of course, if our neural network has more than three layers, we just add more recursively defined functions.

# Forward Pass

The process of taking an input and going through the process of matrix multiplications, vector additions, and activation functions to get the output is referred to as the **forward pass**. To get started, let's write a neural net class that can perform a forward pass, given the dimensions for each layer and an activation function:

```python
import numpy as np

class NN():
    def __init__(self, sizes, activation):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.x_dim = sizes[0]
        self.b = [np.random.randn(1, y) for y in sizes[1:]]
        self.w = [np.random.randn(x, y)
                  for x, y in zip(sizes[: -1], sizes[1:])]
        self.activ = activation
    
    def forward_pass(self, input, classify=False):
        if (input.ndim == 1):
            input = input.reshape(1, -1)
        for i in range(self.num_layers-1):
            input = self.activ.fn(np.dot(input, self.w[i]) + self.b[i])
        return input
```
A quick explanation: our class takes in an array of layer sizes and creates appropriate weight matrices with random values from 0 to 1. EX: `[20, 50, 10]` would result in weight matrices of dimensions $20 \times 50$ and $50 \times 10$. For the `forward_pass` function, we can see from the computational graph that each matrix multiplication (and vector addition) is followed by an application of the activation function, so we can simply recurse until we go through all of our weight matrices.

# Loss Function

So far, I haven't explained how the neural net is supposed to actually work. Say we have some data and their associated target values (EX: different measurements of divers and how long they can hold their breath). Using the above code, even if we get the dimensions of the input/output right, our forward pass is going to give us garbage results.

This is because we randomly initialized our weights and biases. We don't want a random set of weights and biases, but a "good" set of weights and biases. And in doing so, we now need to define what we mean by "good". At the very least, it seems that a good set of weights and biases should lead to predicted values which are close to the associated target values, for most of the data we have.

This is where loss functions come in. They take in as input our predicted value and the true value and output a measure of just how far apart the two values are. There are many functions we could choose to measure the distance between $Y$(true value) and $\hat{Y}$(predicted output). For ease of explanation, we'll go with the $L_2$ norm of their difference, i.e. the sum of the squares of their differences. 

Now, after performing a forward pass, we can use our loss function to tell us just how far away our predicted value is from the true value. It's easy to add this change to our class:

```python
class NN():
    
    def __init__(self, sizes, activation, loss):
        self.loss = loss
        '''
        The rest is unchanged
        '''
    '''
    predict is unchanged
    '''
    
    def eval_loss(self, input, output):
        return self.loss.fn(self.predict(input), output)
```

We can easily integrate this into our model by adding it to our computational graph:

![a graph with nodes, one after another](/images/computational_graph2.svg)

Now we've added one more step:

$f_0 = X = \text{input}$

$f_1 = W_1\cdot f_0 + b_1$

$f_2 = a(f_1)$

$f_3 = W_2 \cdot f_2 + b_2$

$f_4 = a(f_3) = \hat{Y} = \text{predicted output}$

$f_5 = \Vert f_4-Y \Vert_2$

Now that we have our loss function defined, we can begin the work of actually optimizing our network because we have an answer to the question, "Optimizing with respect to what?"

# Backpropagation

Recall that our network is parameterized by a set of weights and biases. (There's also the activation function, but we're going to assume that's fixed.) 

Backpropagation allows us to figure out how much each weight and bias is responsible for the loss function. We do this by taking partial derivatives of the loss function with respect to each weight matrix and bias vector. Given that a neural net is just a big composite function, we'll be using the Chain Rule a lot. This is where the recursive notation shines. It's much easier to have a placeholder like $f_3$ than a big clump of nested parentheses.

The reason we are taking partial derivatives at all is because they'll allow us to perform iterative optimization, e.g. gradient descent, on our network, which is how the "training" happens. 

We'll start with the biases $b_1, b_2, ...$ first:

First, let's find $\frac{\partial f_5}{\partial b_2}$

From above, we've already defined $f_6$ to be the loss function applied after a forward pass, so that's why we're taking the partial derivative of $f_5$ with respect to $b_2$.  Note below that $a'$ is the derivative of the activation function.

$\frac{\partial f_5}{\partial b_2} = \frac{\partial f_5}{\partial f_4}\frac{\partial f_4}{\partial b_2} = 2 (\hat{Y}-Y)\frac{\partial f_4}{\partial b_2}$

$\frac{\partial f_4}{\partial b_2} = \frac{\partial f_4}{\partial f_3} \frac{\partial f_3}{\partial b_2} = a'(f_3) \frac{\partial f_3}{\partial b_2}$

$\frac{\partial f_3}{\partial b_2} = 1$

Thus, $\frac{\partial f_5}{\partial b_2} = 2(\hat{Y}-Y)a'(f_3)$.



Next, let's find $\frac{\partial f_5}{\partial b_1}$

(Below, I've omitted the intermediary step of showing $\frac{\partial g}{\partial x} = \frac{\partial g}{\partial f} \frac{\partial f}{\partial x}$.)

$\frac{\partial f_5}{\partial b_1} =  2 (\hat{Y}-Y)\frac{\partial f_4}{\partial b_1}$

$\frac{\partial f_4}{\partial b_1} = a'(f_3) \frac{\partial f_3}{\partial b_1}$

$\frac{\partial f_3}{\partial b_1} =  W_2 \cdot \frac{\partial f_2}{\partial b_1}$

$\frac{\partial f_2}{\partial b_1} = a'(f_1) \frac{\partial f_1}{\partial b_1}$

$\frac{\partial f_1}{\partial b_1} = 1$

Thus $\frac{\partial f_5}{\partial b_1} = 2(\hat{Y}-Y)a'(f_3)\cdot W_2 \cdot a'(f_1)$.

Before we go any further, there are a two useful things to notice:

1. The loss function's derivative (in this case, $2(\hat{Y}-Y)$) will always be the first term in the partial derivative of the loss with respect to any weight or bias.
2. The partial derivatives of the bias vectors is recursively defined. $\frac{\partial \text{L}}{\partial b_{n-1}} = \frac{\partial \text{L}}{\partial b_n} \cdot W_{n} \cdot a'(z_{n-1})$ where $z_c$ is defined to be the result of $W_{c} \cdot f_{2c-2} + b_{c}$. In other words, $z_c$ is the result of multiplying the previous layer by the $c^{th}$ weight matrix and adding the $c^{th}$ bias vector. We let $L$ represent the general loss function, applied after an arbitrary number of layers.



Let's do the weight matrices $W_1, W_2, ...$ next:

First, let's find $\frac{\partial f_5}{\partial W_2}$

$\frac{\partial f_5}{\partial W_2} = 2 (\hat{Y}-Y)\frac{\partial f_4}{\partial W_2}$

$\frac{\partial f_4}{\partial W_2} = a'(f_3) \frac{\partial f_3}{\partial W_2}$

$\frac{\partial f_3}{\partial W_2} = f_2 = a(f_1)$

Thus, $\frac{\partial f_5}{\partial W_2} = 2(\hat{Y}-Y)a'(f_3)f_2 = \frac{\partial f_5}{\partial b_1}a(f_1)$. 



Now we find $\frac{\partial f_5}{\partial W_1}$

$\frac{\partial f_5}{\partial W_1} = 2 (\hat{Y}-Y)\frac{\partial f_4}{\partial W_1}$

$\frac{\partial f_4}{\partial W_1} = a'(f_3) \frac{\partial f_3}{\partial W_1}$

$\frac{\partial f_3}{\partial W_1} =  W_2 \cdot \frac{\partial f_2}{\partial W_1}$

$\frac{\partial f_2}{\partial W_1} = a'(f_1) \frac{\partial f_1}{\partial W_1}$

$\frac{\partial f_1}{\partial W_1} = f_0 = X$

Thus $\frac{\partial f_5}{\partial W_1} = 2(\hat{Y}-Y)a'(f_3)\cdot W_2 \cdot a'(f_1) f_0 = \frac{\partial f_5}{\partial b_1}f_0$



Here, in both partial derivatives, we see something useful: The partial derivative of the loss function with respect to a weight matrix can be calculated in part using the partial derivative of the loss function with respect to the bias vector in the same layer. The extra term we need is the activation function applied element-wise to the layer before it.

In other words: $\frac{\partial \text{L}}{\partial W_n} = \frac{\partial \text{L}}{\partial b_n} a(z_{n-1})$. 

Thus, as long as we store both the results of $z_c$ and $a(z_c)$ during a forward pass operation, we'll have most of the information we need to calculate the partial derivatives.

We're now ready to write the code:

```python
class NN:

	def backprop(self, x, y):
    	z = []
        activations = [x]
        for i in range(self.num_layers-1):
            x = np.dot(x, self.w[i]) + self.b[i]
            z.append(x)
            x = self.activ.fn(x)
            activations.append(x)
    
```

To start with we perform a forward pass. Along the way, we store the results in `activations` and `z`. One small caveat: we start with `x` in `activations` as well because our recursive definition bottoms out at the input value, so we need for the gradients at the first layer.

Now, we go backwards and recursively calculate our gradients:

```python
class NN:

    def backprop(self, train_x, train_Y):
    	'''
    	same as above
    	'''
        deltas = []
        b_grad = []
        w_grad = []
        for i in range(len(z)):
            if i == 0:
                delta = self.loss.deriv(activations[-1], y
                                       )*self.activ.deriv(z[-1])
                deltas.append(delta)
            if i != 0:
                deltas.append(np.dot(deltas[i-1], self.w[-
                i].T)*self.activ.deriv(z[-i-1]))
            b_grad.append(np.sum(deltas[i], axis=0))
            w_grad.append(np.dot(activations[-2-i].T, deltas[i]))
        return w_grad,b_grad
```

`deltas` is a list holding $\frac{\partial L}{\partial b_c}$ values. The first case handles the derivative of the loss function. We pass it in `activations[-1]` which represents the output of our neural net (as it's the activation of the last layer) and multiply it by `activ.deriv`, the derivative of the activation function (which we assume we've defined elsewhere).

Otherwise, we follow the recursive formula from earlier and multiply the previous `delta` value by the next weight matrix and we multiply it by $a'$ of the next $z_n$ value. To get the $\frac{\partial L}{\partial b_c}$ value, we simply take the current value of delta (and sum up if our input was a matrix rather than a vector). To get the $\frac{\partial L}{\partial W_c}$ value, we follow the recursive formula and perform one more matrix multiplication (we index `activations`by `[-2-i]` because we added `x` as an extra value when starting out).

And we're done! We've now calculated the partial derivatives for all the weights and biases. Next time, we'll dive into different optimization methods and go over how to put these gradients to use.