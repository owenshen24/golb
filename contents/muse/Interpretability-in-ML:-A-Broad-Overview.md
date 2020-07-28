title: Interpretability in ML: A Broad Overview

This blog post is my attempt to give an overview of the sub-field of machine learning interpretability. I do not intend for this post to be necessarily comprehensive, but my goal is to review conceptual frameworks, existing research, and future directions. Most of these ideas are based heavily off of Zach Lipton's [Mythos of Model Interpretability](https://arxiv.org/pdf/1606.03490.pdf), which I think is the best paper for understanding the different definitions of interpretability (and related techniques). For a deeper dive into specific techniques, I recommend [A Survey Of Methods For Explaining Black Box Models](https://arxiv.org/pdf/1802.01933.pdf) which covers a wide variety of approaches for many different ML well as model-agnostic approaches. For neural nets specifically, [Explainable Deep Learning:A Field Guide for the Uninitiated](https://arxiv.org/pdf/2004.14545.pdf) provides an in-depth read.

(Shout-out to [Connected Papers](https://www.connectedpapers.com/main/d516daff247f7157fccde6649ace91d969cd1973/The-Mythos-of-Model-Interpretability/) which made navigating the paper landscape for interpretability very bearable.)

As always, you can find code used to generate the images [here](https://github.com/owenshen24/interp-exp) on GitHub.

In the rest of this post, we'll go over many ways to formalize what "interpretability" means.    Broadly, interpretability focuses on the *how*; it's focused on getting some notion of an explanation for the decisions made by our models. Below, each section is operationalized by a concrete question we can ask of our ML model using a specific definition of interpretability. Before that, though, if you're new to all this, I'll explain briefly about why we might care about interpretability at all. 

## Why Care About Interpretability?

Firstly, interpretability in ML is useful because it can aid in trust. As humans, we may be reluctant to rely on ML models for certain critical tasks , e.g. medical diagnosis, unless we know "how they work". There's often a fear of unknown unknowns when trusting in something opaque, which we see when people confront new technology. Approaches to interpretability which focus on transparency could help mitigate some of these fears. 

Secondly, safety. There is almost always some sort of [shift in distributions](https://arxiv.org/pdf/1606.06565v1.pdf) between model training and deployment. Failures to generalize or Goodhart's Law issues like [specification gaming](https://deepmind.com/blog/article/Specification-gaming-the-flip-side-of-AI-ingenuity) are still open problems that could lead to issues in the near future. Approaches to interpretability which explain the model's representations or which features are most relevant could help diagnose these issues earlier and provide more opportunities to intervene.

Thirdly, and perhaps most interestingly, contestability. As we delegate more decision-making to ML models, it becomes important for people to appeal these decisions made. Black-box models provide no such recourse because they don't decompose into anything that *can* be contested. This has already led to major criticism of proprietary recidivism predictors like [COMPAS](https://en.wikipedia.org/wiki/COMPAS_(software)#Critiques_and_legal_rulings). Approaches to interpretability which focus on decomposing the model into sub-models or explicate a chain of reasoning could help with such appeals.

# Defining Interpretability
Lipton's paper breaks interpretability down into two types, transparency and post-hoc.

## Transparency Interpretability

These three questions are from Lipton's section on transparency as interpretability, where he features on properties of the model that are useful to understand and can be known before training begins. 

### Can a human walk through the model's steps? (Simulatibility)

This property is about whether or not a human could go through each step of the algorithm and have it make sense to them at each step. Linear models and decision trees are often cited as interpretable models using such justifications; the computation they require is simple, no fancy matrix operations or nonlinear transformations. 

Linear models are also nice because the parameters themselves have a very direct mapping–they represent how important different input features are. For example, I trained a linear classifier on MNIST, and here are some of the weights, each of which correspond to a pixel value:

```
0.00000000e+00,  0.00000000e+00,  3.90594519e-05,  7.10306823e-05,
0.00000000e+00,  0.00000000e+00,  0.00000000e+00, -1.47542413e-03,
-1.67811041e-04, -3.83280468e-02, -8.10846867e-02, -5.01943218e-02,
-2.90314621e-02, -2.65494116e-02, -8.29385683e-03,  0.00000000e+00,
0.00000000e+00,  1.67390785e-04,  3.92789141e-04,  0.00000000e+00,
0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00
```

By themselves, these weights are hard to interpret. Even if we knew which pixels they corresponded to, it's difficult to try and pin down what a certain pixel even represents for large images. However, there is an easy trick to turn these weights into something interpretable. We simply reshape them into the same shape as our model and view it as an image, with the pixel color represented by the weight value.

Here are the weights for the model that looks for 0:

![a picture of a grid with 0 highlighted](/images/linear-0.png)

And here are the weights for the model that looks for 3:

![a picture of a grid with 3 highlighted](/images/linear-3.png)

In both cases, we can see that the blue regions, which represent positive weight, correspond to a configuration of pixels that look roughly like the digit being detected for. In the case of 0, we can see a distinct blank spot in the center of the image and a curve-like shape around it, whereas the curves of the 3 are also apparent.

However, Lipton points out that this desiderata can be less about the specific choice of model and more about the *size* of the model. A decision tree with a billion nodes, for example, may still be difficult to understand. Understanding is also about being able to hold most of the model in your mind, which is often about how the model is parameterized. 

One approach towards achieving this for neural nets is [tree regularization](http://www.shallowmind.co/jekyll/pixyll/2017/12/30/tree-regularization/) which adds a regularization term that corresponds (roughly) to the size of the decision tree that can approximate the net being trained. The hope here is to eventually output a shallow decision tree that performs comparably to a neural net. Another approach is [neural backed decision trees](https://arxiv.org/pdf/2004.00221.pdf) which use another type of regularization to learn a hierarchy over class labels, which then get used to form a decision tree. 

Of course, parameterization is not the whole story. There are methods like K-Nearest Neighbors which are eerized by your entire dataset; this could be billions of points. Yet, there is a sense in which KNN is still interpretable despite its massive size. We can cleanly describe what the algorithm does, and we can even see "why" it made such a choice because the algorithm is so simple.

### Is the model interpretable at every step, or with regards to its sub-components? (Decomposability)

Another desirable feature would be to understand what the model is doing at each step. For example, imagine a decision tree whose nodes correspond to easily identifiable factors like age or height. This can sometimes be difficult because model performance is very tightly coupled with the representations used. Raw features, e.g. RGB pixel values, are often not very interpretable by themselves, but interpretable features may not be the most informative for the model.

For example, I trained a decision tree for MNIST using the following interpretable features:

1. The average brightness of the image - `avg_lumin`
2. The average brightness of the image's outline (found using an edge detector) - `edge_prop`
3. The number of corners found in the image's outline `num_corners`
4. The width of the image - `max_width`
5. The height of the image - `max_height`

It seems like there would be at least *some* useful information in these features; ones tend to have less area (so `avg_lumin` would be lower), eights might have more corners, etc. etc. Yet, the resulting decision tree of depth 3, shown below, however, only achieves 33% training accuracy. Going all the way to depth 10 only bumps it to around 50%.

![a decision tree trained on MNIST with interpretable features](/images/interp_mnist_decision_tree.png)

If we look at the nodes, we can perhaps see what's going on. At the top, we can see that our model will predict a 1 if the width is less than 7.5 pixels, which makes sense as 1 is likely going to be the thinnest digit. Near the bottom, we see that the number of corners is being used to differentiate between 7 and 4. And 4s do have more visual corners than 7s. But this is very rough, and the overall performance is still not very good.

To compare this with raw features, I also trained a depth 3 decision tree using direct pixel values, i.e. a vector of 784 grayscale values. The resulting model, shown below, gets 50% train and test accuracy.

![a normal decision tree trained on MNIST](/images/mnist_decision_tree.png)

Here, it's not clear at all why these pixel values were chosen to be the splitting points. And yet the resulting decision tree, for the same number of nodes, does much better. In this simple case, the performance vs interpretability trade-off in representation is quite apparent. 

### Does the algorithm itself confer any guarantees? (Algorithmic Transparency)

This asks if our learning algorithm has any properties which make it easy to understand. For example, we might know that the algorithm only outputs sparse models, or perhaps it always converges to a certain type of solution. In these cases, the resulting learned model can be more amenable to analysis. For example, the [Hard Margin SVM](https://davidrosenberg.github.io/mlcourse/Labs/UniquenessOfSVM.pdf) is guaranteed to find a unique solution which maximizes the margin. In another vein, the [perceptron](https://owenshen24.github.io/perceptron/) is guaranteed to find parameters (not necessarily unique ones, though) that achieve a training loss of 0 if the data are linearly separable.

When it comes to deep learning, I'm less familiar with these kinds of results. My rough understanding is that the equivalence class of models which achieve comparable training error can be quite large, even with regularization, which makes uniqueness results hard to come by. 

As I mentioned earlier with KNN, it seems, aside from mechanical transparency, there's another level of understanding regarding "what the algorithm actually does in simple terms".  KNN is easy to describe as "it reports the labels of the points closest to the input". The part of this property that's doing the most work here is the way we actually do the describing. Obviously most ML models can be abstracted as "it finds parameters which satisfy certain constraints", but this is very broad. It seems harder to find a description at the same level of granularity for neural nets beyond something like "it learns a high-dimensional manifold that maps onto the input data".

## Post-Hoc Interpretability

These four questions are from Lipton's section on post-hoc interpretability, which focus on things we learn from the model after training has occurred. 

### Can the model give an explanation for its decision, after the fact? (Text Explanation)

Similar to how humans often give post-hoc justifications for their actions, it could be informative to have models which can also give explanations, perhaps in text. Naive methods of pairing text with decisions, however, are likely going to optimize for something like "how credible the explanation sounds to a human" rather than "how accurate the explanation is at summarizing the internal steps taken".

While this seems clearly desirable, I think research in this area is hard to come by, and Lipton only offers one paper that is RL-focused. On ConnectedPapers, I found that said paper is part of a larger related field of [reinforcement learning with human advice](https://www.connectedpapers.com/main/a32f4d93f7e50aad52210ab464f4d8e360eb7a7d/Newtonian-Action-Advice-Integrating-Human-Verbal-Instruction-with-Reinforcement-Learning/graph). This seems to focus on the converse problem–given human explanations, how can models incorporate them into their decision-making? Maybe insights here can eventually be used in the other direction.

### Can the model identify what is/was important to its decision-making? (Visualization/Local Explanations)

This focuses on how the inputs and outputs change, relative to one another. 

Saliency maps are a broad class of approaches that look at where the inputs change in order to change the outputs. A simple way to do this is to take the derivative of the loss function with respect to the input. Past this, there are many modifications which involve averaging the gradient, perturbing the input, or local approximations.  [Understanding Deep Networks via Extremal Perturbations and Smooth Masks](https://arxiv.org/pdf/1910.08485.pdf) has a good overview of the work in this area.

For example, I trained a CNN on MNIST and did a simple gradient visualization on an image of this 3:

![a picture of a 3 in MNIST](/images/mnist-3-0.png)

Using PyTorch, I took the derivative of the logit that corresponds to the class 3 with respect to the input image. This gave me the image below. Here, the white pixels correspond to parts of the image that would increase the logit value for 3, and the black pixels correspond to the reverse. We can see the rough curves of the three come through. 

![a picture of the gradient for 3](/images/mnist-3-grad-0.png)

Note how this is different from the visualization we previously had with the linear classifier in red and blue in the first section. Those visuals represented the importance in *aggregate* for the entire input space. The visualization here is only for this specific input. For a different input, e.g. a different 3, the local gradient would look different, as shown below:

This 3:

![a picture of another 3 in MNIST](/images/mnist-3-7.png)

yields this gradient:

![a picture of a gradient for another 3 in MNIST](/images/mnist-3-grad-7.png)

Another group of approaches focus on visualizing with respect to the model parameters themselves, rather than the input. A lot of the work has been done by Chris Olah, Shan Carter, Ludwig Schubert, and others on [distill.pub](https://distill.pub/). Their work in this area has gone from [visualizing the activations of specific neurons and layers](https://distill.pub/2017/feature-visualization), to entire [maps of activations for many networks](https://distill.pub/2019/activation-atlas/), to [decomposing models into interpretable building blocks](https://distill.pub/2020/circuits/zoom-in/). Another great visualization resource for this type of work is the [OpenAI Microscope](https://microscope.openai.com/models). Progress here has been very exciting, but it remains to be seen if similar approaches can be found for neural nets which focus on tasks other than image recognition.

### Can the model show what else in the training data it thinks are related to this input/output? (Explanation by Example)

This asks for what other training examples are similar to the current input. When the similarity metric is just distance in the original feature space, this is akin to KNN with K = 1. More sophisticated methods may look for examples which are similar in whatever representation or latent space the model is using. The human justification for this type of approach is that it is similar to reasoning by analogy, where we present a related scenario to support our actions. 

While I think this is useful, it definitely doesn't seem like all we need for understanding, or even most of what we'd need.

## What Else Might Be Important?

These are a mix of other questions I thought of before/after reading the above papers. Some of them are also from Lipton's paper, but from the earlier sections on interpretability desiderata. Because [answering questions is harder than asking them](https://mlu.red/52622266310.html), I've also taken the time to give some partial responses to these questions, but these are not well-researched and should be taken as my own thoughts only.

1. What are the relevant features for the model? What is superfluous?
   * We've seen that linear models can easily identify relevant features. Regularization and other approaches to learn sparse models or encodings can also help with this. One interesting direction (that may already be explored) is to evaluate the model on augmented training data that has structured noise or features that correlate with real features and see what happens.
2. How can you describe what the model does in simpler terms?
   * The direct way to approach this question is to focus on approximating the model's performance using fewer parameters. A more interesting approach is to try and summarize what the model does in plain English or some other language. Having a simplified description could help with understanding, at least for our intuition.
3. What can the model tell you to allow you to approximate its performance in another setting or another model?
   * Another way to think about models which are interpretable is that they are doing some sort of modeling of the world. If you asked a person, for example, why they made some decision, they might tell you relevant facts about the world which could help you come to the same decision. Maybe some sort of teacher-learner RL type scenario where we can formalize knowledge transfer? But ultimately it seems important for the insights to be useful for humans; the feedback loop seems too long to make it an objective to optimize for, but maybe there's a clever way to approximate it…There might be a way where we instead train a model to output some representation or distribution that, when added to some other interpretable model (which could be a human's reasoning), leads to improved performance.
4. How informative is this model, relative to another more interpretable model?
   * Currently, deep learning outperforms other more interpretable models on a wide variety of tasks. Past just looking at loss, perhaps there is some way we can formalize how much more information the black box model is using. In the case of learned features versus hand-picked features, it could be useful to understand from an information theory perspective how much more informative the learned features are. Presumably interpretable features would tend to be more correlated with one another.
5. What guarantees does the model have to shifts in distribution?
   * Regularization, data augmentation, and directly training with perturbed examples all help with this issue. But perhaps there are other algorithmic guarantees we could derive for our models. 
6. What trips up the model (and also the human)?
   * One interesting sign that our model is reasoning in interpretable ways is to see if examples which trip up humans also trip up the model. There was some work a little while back on adversarial examples which found that certain examples which fooled the network also fooled humans. Lack of divergence on these troubling examples could be a positive sign.
7. What trips up the model (but not the human)?
   * Conversely, we might get better insight into our model by honing in on "easy" examples (for a human) that prove to be difficult for our model. This would likely be indicative of the model using features that we are not, and thus it's learned a different manifold (or whatever) through the input space.
8. What does the model know about the data-generation process?
   * In most cases, this is encoded by our prior, which is then reflected in the class of models we do empirical risk minimization over. Apart from that, it does seem like there are relevant facts about the world which could be helpful to encode. A lot of the symbolic AI approaches to this seem to have failed, and it's unclear to me what a hybrid process would look like. Perhaps some of the human-assisted RL stuff could provide a solution for how to weigh between human advice and learned patterns.
9. Does the model express uncertainty where it should?
   * In cases where the input is something completely nonsensical, it seems perhaps desirable for the model to throw its hands up in the air and say "I don't know", rather than trying its best to give an answer. Humans do this, where we might object to a question on grounds of a type error. For a model, this might require understanding the space of possible inputs. 
10. What relationships does the model use?
   * The model could be using direct correlations found in the data. Or it could be modeling some sort of causal graph. Or it could be using latent factors to build an approximate version of what's going on. Understanding what relationships in the data are lending themselves to helping the model and what relationships are stored could be useful.
11. Are the model's results contestable?
   * We touched on this at the very beginning of the post, but there are not many modern approaches which seem to have done this. The most contestable model might look something like an automated theorem prover which uses statements about the world to build an argument. Then we would simply check each line. Past that, one nice-to-have which could facilitate this is to use machine learning systems which build explicit models about the world. In any case, this pushes our models to make their assumptions about the world more explicit.

## What's Next?

Broadly, I think there are two main directions that interpretability research should go, outside of the obvious direction of "find better ways to formalize what we mean by interpretability". These two areas are evaluation and utility.

### Evaluation

The first area is to find better ways of evaluating these numerous interpretability methods. For many of these visualization-based approaches, a default method seems to be sanity-checking with our own eyes, making sure that interpretable features are being highlighted. Indeed, that's what we did for the MNIST examples above. However, [Sanity Checks for Saliency Maps](https://www.arxiv-vanity.com/papers/1810.03292/), a recent paper, makes a strong case for why this is definitely not enough.

As mentioned earlier, saliency maps represent a broad class of approaches that try to understand what parts of the input are important for the model's output, often through some sort of gradient. The outputs of several of these methods are shown below. Upon visual inspection, they might seem reasonable as they all seem to focus on the relevant parts of the image.

![saliency map image](/images/saliency-maps.png)

However, the very last column is the output, not for a saliency map, but for an edge detector applied to the input. This makes it not a function of the model, but merely the input. Yet, it is able to output "saliency maps" which are visually comparable to these other results. This might cause us to wonder if the other approaches are really telling us something about the model. The authors propose several tests to investigate. 

The first test compares the saliency map of a trained model with a model that has randomly initialized weights. Here, clearly if the saliency maps look similar, then it really is more dependent on the input and not the model's parameters.

The second test compares the saliency map of a trained model with a trained model that was given randomly permuted labels. Here, once again, if the saliency maps look similar, this is also a sign of input dependence because the same "salient" features have been used to justify two different labels.

Overall, the authors find that the basic gradient map shows desired sensitivity to the above tests, whereas certain other approaches like Guided BackProp do not.

I haven't looked too deep into each one of the saliency map approaches, but I think the evaluation methods here are very reasonable and yet somehow seem to be missed in previous (and later?) papers. For example, the paper on [Grad-CAM](https://arxiv.org/pdf/1610.02391.pdf) goes in-depth over the ways in which their saliency map can help aid in providing explanations or identifying bias for the dataset. But they do not consider the sensitivity of their approach to model parameters. 

In the above paper on sanity-checks, they find that Grad-CAM actually is sensitive to changes in the input, which is good, but I definitely would like to see these sanity-checks being applied more frequently. Outside of new approaches, I think additional benchmarks for interpretability that mimic real-world use cases could be of great value to the field.

Some other tasks, off the top of my head, which seem possibly useful:

LIST

### Utility

The second area is to ensure that these interpretability approaches are actually providing value. Even if we find ways of explaining models that are actually sensitive to the learned parameters (and everything else), I think it still remains to be seen if these explanations are actually useful in practice. At least for current techniques, I think the answer is uncertain and possibly even negative.

[Manipulating and Measuring Model Interpretability](https://arxiv.org/pdf/1802.07810.pdf), a large pre-registered from Microsoft Research, found that models which had additional information like model weights were often not useful in helping users decide how to make more accurate judgments on their own or notice when the model was wrong. (Users were given either a black-box model or a more interpretable one.)

They found that:

> "[o]n typical examples, we saw no significant difference between a transparent model with few features and a black-box model with many features in terms of how closely participants followed the model’s predictions. We also saw that people would have been better off simply following the models rather than adjusting their predictions. Even more surprisingly, we found that transparent models had the unwanted effect of impairing people’s ability to correct inaccurate predictions, seemingly due to people being overwhelmed by the additional information that the transparent model presented"

Another paper, [Interpreting Interpretability: Understanding Data Scientists’ Use of Interpretability Tools for MachineLearning](http://www.jennwv.com/papers/interp-ds.pdf), found that even data scientists may not understand what interpretable visualizations tell them, and this can inspire unwarranted confidence in the underlying model, even leading to ad-hoc rationalization of suspicious results. 

Lastly, [Evaluating Explainable AI: Which Algorithmic Explanations Help Users Predict Model Behavior?](https://arxiv.org/pdf/2005.01831.pdf), is a recent study of five interpretability techniques and how they empirically help humans. The authors found very few benefits from any of techniques. Of particular note is that explanations which were rated to be higher quality by participants were not very useful in actually improving human performance.

All of this points to the difficult road ahead for interpretability research. These approaches and visuals are liable to be misused and misinterpreted. Even once we get improved notions of intepretability with intuitive properties, it still remains to be seen if we can use them to achieve the benefits I listed out in the very beginning. While it certainly seems more difficult to formalize interpretability than to use it well, I'm glad that empirical tests are already being done; they can hopefully also guide where the research goes next.

Finally, lurking behind all this is the question of decreased performance and adoption. It's obvious these days that black box models dominate in terms of results for many areas. Any additional work to induce a more interpretable model, or to derive a post-hoc explanation brings an additional cost. At this point in time, all the approaches towards improving interpretability we've seen either increase training / processing time, reduce accuracy, or do some combination of both. For those especially worried about competition, arms races, and multipolar traps, the case to adopt these approaches (past whatever token compliance will satisfy the technology ethics boards of the future) seems weak. This is also troubling.