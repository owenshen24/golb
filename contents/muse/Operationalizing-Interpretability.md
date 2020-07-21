title: Operationalizing Interpretability

This blog post is my attempt to get some more clarity on how to think about interpretability in ML. Zach Lipton's [Mythos of Model Interpretability](https://arxiv.org/pdf/1606.03490.pdf) is a great survey of the different definitions that people use when they talk about "interpretability". Another useful paper is to be [A Survey Of Methods For Explaining Black Box Models](https://arxiv.org/pdf/1802.01933.pdf) which covers a wide variety of approaches for many different ML well as model-agnostic approaches. For neural nets specifically, [Explainable Deep Learning:A Field Guide for the Uninitiated](https://arxiv.org/pdf/2004.14545.pdf) provides an in-depth read. Lastly, shout-out to [Connected Papers](https://www.connectedpapers.com/main/d516daff247f7157fccde6649ace91d969cd1973/The-Mythos-of-Model-Interpretability/) which made navigating the paper landscape for interpretability very bearable.

One way to operationalize the concepts in these papers is to translate them into concrete questions we can ask of a machine learning model. Below, I've listed out a set of such questions, what concepts they reference, and what research exists to solve them.

# Transparency Interpretability

These three questions are from Lipton's section on Transparency as interpretability, where he features on properties of the model that are useful to understand and can be known before training begins.

### Can a human walk through the model's steps? (Simulatibility)

This property is about whether or not a human could go through each step of the algorithm and have it make sense to them at each step. Linear models and decision trees are often cited as interpretable models in these domains because the computation they require is simple, no fancy matrix operations or nonlinear transformations. However, Lipton points out that this desiderata is often less about the specific choice of model and more about the *size* of the model. After all, a decision tree with thousands of nodes would likely still be complicated to understand. Understanding is also about being able to hold most of the model in your mind, which is often about how the model is parameterized. 

Of course, parameterization is itself an imperfect metric. K-Nearest Neighbors, for example, is an algorithm parameterized by your entire dataset–which could be millions of points–but it seems rather feasible for a human to perform the KNN algorithm. Furthermore, KNN has several other desirable properties related to interpretability, like telling you what points in your dataset induced its decision (albeit this is trivially true, given what the algorithm does).

* talk about why linear models and decision trees are favored
* show an example with a thick decision tree model for MNIST
* explain Lipton's point about how this often really is about model size
* except it's not always true as KNN makes a lot of sense, and can even answer other questions, but it's parameterized by the entire dataset

### Is the model interpretable at every step, or with regards to its sub-components? (Decomposability)

Another desirable feature would be to understand what the model is doing at each step. For example, a decision tree whose nodes correspond to easily identifiable factors like age or height. This can sometimes be difficult because model performance is very tightly coupled with the representations used. Raw features are often not very interpretable by themselves, for example the RGB pixel values of an image. Thus, while this seems very useful to have in theory, it seems difficult to achieve.

* explain how this often requires feature-engineering
* show an example w/ MNIST and hand-picked features

### Does the algorithm itself confer any guarantee? (Algorithmic Transparency)

This asks if our learning algorithm has any properties which make it easy to understand. For example, we might know that the algorithm only outputs sparse models, or perhaps it always converges to a certain type of solution. In these cases, the resulting learned model can be more amenable to analysis.

* perhaps show a linear model or an SVM, something with convergence guarantees

# Post-Hoc Interpretability

These four questions are from Lipton's section on Post-Hoc Interpretability, which are things we learn from the model after training has occurred.

### Can the model give an explanation for its decision, after the fact? (Text Explanation)

Similar to how humans often give post-hoc justifications for their actions, it could be informative to have models which can also give explanations, perhaps in text. Naive methods of pairing text with decisions, however, are likely going to optimize for something like "how credible the explanation sounds to a human" rather than "how accurate the explanation is at summarizing the internal steps taken".

### Can the model identify what is/was important to its decisionmaking? (Visualization/Local Explanations)

We can ask a variety of questions about our input and outputs from the model. We might be interested to know which parts of the input are responsible for most of the output or how little the input has to change for the output to change. Other techniques focus on outputting an interpretable model in the neighborhood of the input, so we can at least understand how the model changes locally.

### Can the model show what else in the training data it thinks are related to this input/output? (Explanation by Example)

This is a generalization of what KNN does. We can ask the model for which examples it thinks are similar to the current input. If the similar input had an output similar to the current one, this can sort of be thought as an explanation by analogy.

# Some more questions

These are a mix of other questions I thought of before/after reading the above papers. Some of them are also from Lipton's paper, but from the earlier sections on interpretability desiderata.

1. What are the relevant features for the model? What is superfluous?
2. What is the space of inputs for which the model is well-defined?
3. How can you describe what the model does in simpler terms?
4. What can the model tell you to allow you to approximate its performance in another setting or another model?
5. How informative is this model, relative to another more interpretable model?
6. What guarantees does the model have to shifts in distribution?
7. What trips up the model (and also the human)?
8. What trips up the model (but not the human)?
9. What does the model know about the data-generation process?
10. How much context does the model have?
11. Does the model express uncertainty where it should?
12. What relationships does the model use?
13. How easy can the model be gamed after deployment?
14. Are the model's results contestable, i.e. are they based on claims that can be disproven?

To conclude, however, I think there is an argument the current landscape of interpretability techniques are not having their desired effect–namely that of improving the decision-making abilities of the people who use them. A large pre-registered [study](https://arxiv.org/pdf/1802.07810.pdf) from Microsoft found that models which had additional information (intended to add interpretability) were often not useful in helping users decide how to make more accurate judgments on their own or notice when the model was wrong.

They find that, *"[o]n typical examples, we saw no significant difference between a transparent model with few features and a black-box model with many features in terms of how closely participants followed the model’s predictions. We also saw that people would have been better off simply following the models rather than adjusting their predictions. Even more surprisingly, we found that transparent models had the unwanted effect of impairing people’s ability to correct inaccurate predictions, seemingly due to people being overwhelmed by the additional information that the transparent model presented"*.

Another [study](http://www.jennwv.com/papers/interp-ds.pdf) found that even data scientists may not understand what interpretable visualizations tell them, and this can inspire unwarranted confidence in the underlying model. 

Lastly, a recent [study](https://arxiv.org/pdf/2005.01831.pdf) of five interpretability techniques and how they help humans with model simulatability found very few benefits from any technique. Of particular note is that explanations which were rated to be higher quality by participants were not very useful in improving human performance.

Overall, this isn't too damning if you're mostly interested in interpretability from the AI safety perspective. Presumably the people using the tools will be more informed about what interpretability results mean, which can sidestep some of these errors. But it does seem problematic that, from a normal user's perspective, these approaches are not having the intended result, especially with how hot it is to talk about "explainable AI" right now.