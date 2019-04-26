title: Working on MLU 2.0

So I finally got around to updating my site. It's been my goal for a while ot have a nice place where I can port over all of my blog posts, and I'm excited to be wrapping up the static site generator. I don't think the overall code was very large, but it feels good because I wrote the whole thing, so I know what's going on. I'd previously tried both Jekyll and Hugo, and they both seemed over-the-top for what I wanted.

Going through the whole process, I can see now why certain design decisions were made, as I had to make similar ones. Things like whether or not to include defaults, checking for metadata, being smart about updates, etc. etc.

But now I can rejoice because I think I've ironed out most of the bugs! I have a static site generator that is pretty smart about only updating files which have been edited, and it supports the changing of titles, which is pretty nice. Sort of. While typing this, I just realized that I don't actually have support for dead links. While my index page keeps track of when pages change, I don't take into account the changing of the actual page slug.

And, really, there's no reason except for my own clarity, why the actual page slug has to change. Given that I'm already using numeric IDs, I could just make the slug the ID itself. And that would solve backwards compatibility, given that I'm already counting up.

Most of these changes, though, seem like they're more relevant to Muse than to MLU. My current Muse implementation is pretty nice, I think. It's simple, everything's on one page, and anchors allow hotlinking to any single post. There's client-side search, which is always cool, and it's readable enough. 

I think that having a one-page blog, though, isn't great from a UX perspective; it encourages binging and that sort of thing. So that's why I made the conscious decision of having an index to break it up.

I'm pretty satisfied with the separation between MLU and Muse, and the slight differences between them. I'll probably write more about the writing process soon, but the whole point, after all, of a short-form blog, is to be able to just randomly write stuff, yeah?