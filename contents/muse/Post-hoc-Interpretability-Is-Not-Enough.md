title: Post-hoc Interpretability Is Not Enough

[Post-hoc intepretability](https://mlu.red/muse/52906366310.html) in machine learning is about extracting explanations after the model has already been trained. In many cases, we further relax our assumptions and assume the model is a black-box. I think these sorts of techniques are likely not going to be enough for AI alignment. To be clear, I don't think anyone is currently claiming the opposite. But I still wanted to list out my reasons, especially as other people may disagree for other reasons.

### 1] Post-hoc interpretability lags behind the forefront of the field

Post-hoc methods have yet to scale up to the largest ML models we see today. I don't think, for example, that we have anything yet for GPT-3. Also, partially by definition, we require a model to be already trained before we can apply these methods. Especially in the case where we can only do such investigations after deployment, it may be too late to deal with errors in production. Even if we get to investigate the models prior to deployment, there will likely be further progress while we investigate the current model. In either case, post-hoc methods do not put us in a good position to influence what's happening at the forefront.

### 2] Post-hoc interpretability cannot answer certain types of questions

I'll try to flesh this out later on, but my guess is that there is a large class of questions we can't answer with post-hoc techniques. One group seems to be questions about the model's training training trajectory, questions like "Would increasing the prevalence of this data point have led to better performance?" Another group of related questions is counterfactuals about the final ML model, questions like "What would your output hypothesis have looked like if this data point was in your dataset?" There have already been critiques of this form, so this is nothing new.

### 3] Post-hoc interpretability metrics are already gameable

Recent work has shown that currently populat perturbation-based methods for extracting post-hoc explanations of black-box models can be gamed. [This work](http://sameersingh.org/files/papers/advlime-aies20.pdf), for example, shows adversarial examples for LIME and SHAP, two popular and lauded approaches for post-hoc explanations. Knowing Goodhart's Law, this was an expected outcome, sooner or later. I expect there are probably metrics that can be less easily gamed, but still.

Where, then, do I see post-hoc methods being useful?

### 1] Investigation during training

I think post-hoc techniques can help identify how relevant features change during testing. It seems like there could be informative ways to talk about the trajectory of the model throughout testing, how relevant features change, etc. etc. in a way that can better fit the "learning analogy".

### 2] Actually, post-hoc is useful and the above is false

I think the sentiment of Chris Olah, Shan Carter, and others working on interpretability at OpenAI have this sort of sentiment in their [thread on circuits](https://distill.pub/2020/circuits/zoom-in/#claim-1). Here, they seem to claim that (at least certain) neural nets are already modular with respect to their function and composition and that, furthermore, post-hoc visualization techniques can offer insight into their functions. I thnk this is really intriguing, but I'm unsure if this will capture longer-term dependencies if the net isn't regularized in some way to have interpretable output at each step.

### 3] Revealing what sorts of models we should aim for 

If the goal of post-hoc interpretability is to tell us things about our model, then maybe it seems good to try and figure out what those are, and then design a model which just makes those things clear from the start. I don't know about this, as it seems like humans use some sort of not-interpretable thing to make decisions, and then we explain them in terms of concepts. But it's not clear to me at all that we're actually manipulating concepts under the hood. If so, then this seems like we might have to deal with messy internals and then look for meaning after the fact.
