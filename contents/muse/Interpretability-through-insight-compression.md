title: Interpretability through insight compression

In interpretable machine learning, I think one important question we should be able to ask of our models is “What is something useful you can tell me about your understanding of the data?” Much of the current research lacks agreement on a standardized definition, and existing methods are often subjectively evaluated (e.g. “It just looks better”). I don’t expect the following definition to be useful everywhere, but I think it opens up a set of questions that haven’t been explored yet.

Ideally, we want our models to be useful outside of just their black-box output; one way to extract more value and potentially learn more about how they operate is to impose the additional constraint that they output something useful, i.e. an “insight”, to the human operator. The insight should be something that helps our own performance at the task.

A simple way to formalize this in the typical machine learning paradigm is to set up a dual-training loop where a powerful model is optimized to both minimize loss, as well as output some bits that optimize a weaker model (which approximates a human). A set of concrete steps I’d take might look like:

1. Determine a reasonable toy task as proof of concept
2. Think about to what extent the toy task can generalize
3. Find a way to represent human judgment via a model
4. The difficulty here will be encoding the model in a way that we can then port the insights back into human ontology.
5. Set up the actual training loop in PyTorch and run the code.
6. Inspect the final output model’s insights.

I think this idea is mostly based on how successful I can be at evaluating the usefulness of the additional bits as insight at scale, in a way that approximates how a human might actually respond. The main concern I have with this is that the simple training setup as described above could end up just being a proxy optimizer for the smaller model. A negative outcome would be if this ends up being an example of mesa-optimization for the larger model. I think this could still be useful, even in such a case, as it provides a small-scale example of mesa-optimization in practice.
