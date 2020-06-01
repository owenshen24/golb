title: Acronyms vs Surname?

### Motivation

I've been writing some papers lately, and one thing that has bugged me is how many different formatting styles have resorted to (LastName et al) for inline citations. Not only is this problematic when authors contribute equally, but there aren't that many last names in the world. Surely there are bound to be many collisions, perhaps even within a paper? I myself just cited two different Klines for a recent paper.

Then, while musing, I figured that perhaps the acronym of the paper's title could serve as a more unique identifier instead of just the lead author's last name. For example, if Victoria Wang wrote a paper called Discovering A New Prime, we'd use (DANP) instead of (Wang) as an inline citation. Perhaps this is obvious to you already. Of course, the next thing to do is to empirically verify this.

I found this [great dataset on Kaggle](https://www.kaggle.com/neelshah18/arxivdataset) which contains around 40,000 papers related to AI/CV from Arxiv, along with the author information, title, and abstract. From there, I wrote some [basic code](https://github.com/owenshen24/Acronym-vs-Surname) to compare the distributions of title acronyms versus surnames.

### Results

The first thing that seems important to look at is what proportion of papers would be "collisions", i.e. papers that would have the same identifier, if we were to use either the paper's title acronym versus the last name of the first author.

Turns out, lots of people have the same last name:

![chart showing that 21% of papers have no collisions](/images/pie-chart-surname.png)

Under the typical schema of using the last name of the first author, we find that only 20.9% of papers would be uniquely identified. (I realize this would be a lot higher if we also used the date of publication, or additional authors, but please indulge me for now.)

The outlook is significantly better if we use acronyms:

![chart showing that 98.2% of papers have no collisions](/images/pie-chart-title.png)

Here, we find that 98.2% of all papers would have a unique acronym, if we based it off of the title.

The next thing to look at is what the actual distribution of collisions looks like. Are there a few acronyms or surnames that many papers share (i.e. few collisions, high count for each), or is there a mix of many small coincidences (i.e. many collisions, low count for each)?

The distribution for last names is *very* fat-tailed:<style>.no-max {max-height: unset; padding: 0rem;}</style>
<img src="/images/distr-surname.png" class="no-max" height="1300">

What are those last names at the very bottom of the graph that have several hundred collisions? We'll get to those in a moment.

The distribution for acronyms is very tight:

![chart showing not a fat tail](/images/distr-title.png)

Here, we see that there are very few collisions with many counts. Only one acronym has apparently 12 papers which share the same acronym, a far cry from the several hundred if we use last names.

Now that we've seen the shape of our data, we might be interested in what those extreme values are. I've compiled the 10 most frequently seen last names in the table below:

<table>
<thead>
<tr>
<th>Last Name</th>
<th>Count</th>
</tr>
</thead>
<tbody>
<tr>
<td>Wang</td>
<td>766</td>
</tr>
<tr>
<td>Zhang</td>
<td>663</td>
</tr>
<tr>
<td>Li</td>
<td>653</td>
</tr>
<tr>
<td>Chen</td>
<td>536</td>
</tr>
<tr>
<td>Liu</td>
<td>482</td>
</tr>
<tr>
<td>Yang</td>
<td>262</td>
</tr>
<tr>
<td>Xu</td>
<td>253</td>
</tr>
<tr>
<td>Wu</td>
<td>220</td>
</tr>
<tr>
<td>Zhu</td>
<td>187</td>
</tr>
</tbody>
</table>


We'll do the same for the acronym data:

<table>
<thead>
<tr>
<th>Acronym</th>
<th>Count</th>
</tr>
</thead>
<tbody>
<tr>
<td>POTTCOUIAI</td>
<td>12</td>
</tr>
<tr>
<td>SC</td>
<td>7</td>
</tr>
<tr>
<td>POTFCOUIAI</td>
<td>5</td>
</tr>
<tr>
<td>POTSCOUIAI</td>
<td>5</td>
</tr>
<tr>
<td>CF</td>
<td>5</td>
</tr>
<tr>
<td>CC</td>
<td>5</td>
</tr>
<tr>
<td>CP</td>
<td>5</td>
</tr>
<tr>
<td>CB</td>
<td>5</td>
</tr>
<tr>
<td>BS</td>
<td>4</td>
</tr>
</tbody>
</table>


Once again, we notice that even at the most extreme, these collisions have very few counts. But what's up with that really long acronym, the POT__COUIAI, which shows up in a few different guises? It turns out that those are all from the journal *Proceedings of the Xth Conference on Uncertainty in Artificial
  Intelligence*. So it's less about some mystic convergence in titles and more about the fact that the papers on Arxiv also include journals.

As for the other ones, we notice that they're all two word titles, which makes it a lot more likely for collisions to happen, so that's not too surprising. Several examples of "SC" papers include *Statistical Constraints*, *Sequencing Chess*, and *Stereoscopic Cinema*.

### Conclusion

I think many people would have found my hypothesis likely at the start. After all, last names have to follow many human constraints, like having a mix of vowels and consonants, whereas the constraints on titles are a lot looser. As I alluded to earlier, I've sort of stacked the deck against the last name identifier method. Adding in the publication year, the first name, or additional authors, will all greatly decrease the chance of collisions.

Still, I think this can still lead to some confusion, especially as there's a lot of baggage related to one's last name. (EX: I might mistake Klein 2004 and Klein 1996 as being from the same author, or that Jon Krakauer is related to John Krakauer.)

I'm not suggesting that acronyms are really an ideal solution, as many of them are not very pronounceable. But I do think this should push us to think about better ways to refer to scientific papers.
