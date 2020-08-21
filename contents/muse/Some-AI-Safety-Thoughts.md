title: Some AI Safety Thoughts

I had a nice chat with Alex Flint today, and here are some things that came up, which seem worth writing down:

One view of interpretability is about *communication* between the model and another model (or person or whatever). Model distillation / approximation is one way to get at this. One possible operationalization is to have a training loop where a stronger learner needs to output something that a weaker learner can also use to do well at the same task. This seems problematic, however. One thing is that this seems just like an inefficient way to train the weak learner. The other thing is that, even if you do this right, you may have accidentally just turned the first learner into an optimizer instead of a model that's good at communicating to other models. But not necessarily, of course. 

Design versus search. How can we design ML algorithms that do reasoning in a more principled way? How can we make search more like design? One thing is to try to do the learning in more distinct stages. First, train some sort of unsupervised learner to try and cluster/model the underlying data. Then, find some way to encode certain biases about what "reasonable hypotheses" look like. Finally, start the actual supervised training loop where we have some way to optimize the actual hypothesis generation. 

Is the interpretability in the *model* or in the *data*? Data seems to start off rather interpretable, but then it often gets transformed into some other representation which is more efficient but also more opaque. Maybe we could train a model and then use the intermediary representations in another model? That is, train a model to try and understand what another model was doing? This is sort of like the auto-encoder paradigm, except that we aren't doing the two optimization steps in tandem.

Do models start off interpretable? I guess most initializations are fairly interpretable, as they usually just output 0 or do something that's largely uninformative. But then they become more opaque? 



