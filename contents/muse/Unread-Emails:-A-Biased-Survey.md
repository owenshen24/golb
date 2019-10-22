title: Unread Emails: A Biased Survey
summary: I ask my Facebook friends how many unread emails they have.

So a while back, I've noticed that my parents have lots of unread emails, somewhere in the thousands. A lot of them seemed to be spam or marketing emails. I also know of lots of people who seem to be very good at managing their inbox. For me personally, I have around 0-10 emails unread in my inbox, as I keep emails I want to respond to unread, or emails which represent to-dos.

It seemed likely there was a bimodal distribution, with lots of people close to zero, and lots of people at infinity, or whatever the max email limit is. To figure this out, I ran a super informal survey on my Facebook friends, and I got 80 responses. I give the results below:

(Note the data can be found [here](/assets/unread_emails.csv). If you want to add your data, you can take the survey [here](https://forms.gle/KNpDpt54TvjEiPzX9).)

Here's a histogram which shows the general distribution:

![histogram of unread email values](/images/unread_emails_hist.png)

It looks like most people are at most at the several thousands, with a very long tail of people in the tens of thousands. If we zoom in, though, we realize most people are far from even one thousand.

Here's the same distribution, now log-scaled:

![histogram of unread emails, log scaled](/images/unread_emails_hist_log.png)

Now we see that around half of the participants are at 100 unread emails or less. Out of the 80 participants, 25 of them had exactly 0 emails in their inbox. In general, I think my friends are much more productivity focused than the general crowd. I expect more people to have heard of things like inbox zero.

I also asked for the participants' ages. Most people were between 18 and 35. I've plotted the them below in a scatter-plot:

![scatterplot of age and unread email count](/images/unread_emails_scatter.png)

Maybe an older (or younger) crowd would have different numbers? I don't expect to draw any grand conclusions from this all. Mostly just to sate my own curiosity.
 