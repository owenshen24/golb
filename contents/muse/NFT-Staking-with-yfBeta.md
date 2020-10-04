title: NFT Staking with yfBeta

# Intro

If you haven't already, you probably want to read my short piece about [Dynamic NFTs](https://mlu.red/muse/53028466310.html) for some context.

Well, it's finally here. After one failed launch, much stress and pain, we're here for real. NFT staking for yfBeta is now live (or soon to be) on [yflambda.finance](yflambda.finance). Before we go any farther, I want to remind everyone of a few things:

* For now, this is still unofficial. I'll wait for the community to vote and decide on how integrate this should be with our core platform. That's why this is hosted on a different domain, rather than the yfbeta site.
* The code is still unaudited. However, I have tested it both on mainnet and testnet, and I've also onboarded several early users, all of whom have been able to use the app with no issues. Note that this is not the same thing as saying the code is 100% bug-free, but I've put in much more effort this time to test.
* This is not the final version. I still have ideas to improve upon how NFTs can be used; please look forward to an NFT v2 in the near future with even more features and utility.

# How NFT staking works

With that out of the way, how does the current NFT staking work? What do you stake, and what do you get? 

The current NFT staking flow works like this:

1. You lock up your yfB by staking into the contract. This is one transaction (two, if you need to approve spending).
2. You then mine a Gem that represents your staked yfB.  This is one transaction.
3. When you want to stop staking, you Withdraw All. This is one transaction.

The NFT Gem that you mine has a few nifty properties:

1. As long as you're staked, it'll keep counting up the amount of time staked. This will allow its image to update to new forms, i.e. shinier colors.
2. When you unstake, your Gem will be counted as "dead", and it'll no longer update. The current iteration will show your Gem in static, gray image.
3. As an ERC-721 token, Gems are visible on platforms like OpenSea and Rarible and can even be traded.

# Gems, explained

The ERC-721 standard is unfortunate in that it doesn't specify a way of defining an on-chain data store. The recommended method is to store data off-chain, at least when you look at the OpenSea docs. I prefer on-chain data when feasible (i.e. images are hard to store, so off-chain makes more sense), so I've built info directly into the contract.

Each Gem keeps track of:

- The amount staked to create the Gem.
- Whether or not the underlying yfB is still being staked.
- The starting block when the stake started.
- The ending block when the stake ended, if applicable.
- The initial miner of the Gem, i.e. the person who originally staked.

The only information that's uniquely stored off-chain is the image file. The rest of the attributes are being duplicated from on-chain data. OpenSea gets the data by querying my API endpoint, which I generate by querying on-chain data, and then adding the corresponding image URL.

For now, I need to manually update the server to give accurate information to OpenSea via the tokenURI, so don't panic if it takes up to a day or two for it to fully update.

# Future plans

I think that the current NFT staking contract provides a twists on the NFT model that, at the very least, are fun to look at and play with. Past that, I have some ideas for what a v2 would look like in terms of adding more gamification and giving users more options. Some examples of additional features include adding Gem rarity, setting lock-up times, and a built-in marketplace for trading.

Now that users have these NFTs, I think there are a few ways we can further capitalize on this. My original plan was to fill a need I saw in the community–a lack of use for the native token, and it's been exciting seeing people take this idea farther. Two such ideas which seem especially exciting are NFT governance and using Gems as a requirement to enter certain future vaults.

I'll be pushing out the first set of visual upgrades to the gems, so please stay tuned. This and further updates will be coming soon:tm:.

# Closing thoughts

I told the community that NFT staking was coming in 2-4 weeks, and it's been only 12 days or so since the original NFT launch. So I beat out even my most optimistic estimate. I'm still reeling over the original bug, but I've tested things more thoroughly this time, so I really hope there isn't another issue.

Working on this project has been exciting, as I've been able to get much more familiar with many new technologies. But it has also been incredibly tiring, both interacting with the community across Discord and Telegram, as well as actually coding this up. I'll still be around, but please don't be surprised if I'm around less for a while.