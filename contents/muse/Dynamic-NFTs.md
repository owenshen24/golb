title: Dynamic NFTs

So NFTs are really hot right now in the crypto-sphere. If you aren't aware, NFT are non-fungible tokens, which mean that they aren't denominated, like normal currency. Instead, each item has a unique id, and they can have different properties. CryptoKitties is a well-known project that uses NFTs to represent the kittens that users trade and breed. 

I'm not quite sure why, but it's very popular to implement them into different projects right now. With marketplaces like OpenSea (where users can buy and sell NFTs) and projects like Meme (where users can stake their MEME tokens for trading cards and even live event privileges), the space has exploded. Here, I'm going to cover an idea that I think has been underexplored in the space of NFTs, which I've spent a little bit of time thinking about: Dynamic NFTs.

What does that mean? A Dynamic NFT is a token that responds in some way to other conditions, either on-chain or off-chain. For example, an NFT based on some underlying asset (e.g. Ethereum) whose image actually grows or shrinks relative to the asset's performance. Even from just a novelty and art perspective (which, arguably, is what is driving a lot of this NFT hype), I think that this could be interesting. One drawback from the rise of platforms like Rarible which automate the entire NFT creation process is that it leaves out the space for this type of custom behavior. Look around, and you'll see static images, GIFs, and maybe even an NFT bundled with some other item, but there isn't anything really *responsive*.

Some brainstormed examples where Dynamic NFTs could be interesting:

1. Your character in a game is represented as an NFT, and when you equip items, the NFT gets modified. This makes it easy to transfer ownership over your character (along with all its items).
2. You mint an NFT that looks at trades you make on a DEX like Uniswap. It keeps a running total of your gains and losses, giving you a badge you can display to others.
3. You set up a Pokemon-like game on-chain, and you can update the NFT's image when your monster evolves.

Other less fleshed-out ideas:

1. Something with oracles, e.g. weather data, where you could trade a multi-use oracle, e.g. an item pre-loaded with 10 API calls or something.
2. Something with pre-loaded accounts, where the NFT represents a basket of tokens the user can spend.
3. Lootboxes.
4. Lootboxes which allow for re-rolls.
5. Rechargable NFTs.

To be clear, I don't think there's any real "new" functionality that's being added here with Dynamic NFTs. You could do all of this with smart contracts and use some other sort of token-holder-based check to see who owns them, etc. etc.

But, *given* that they're hot right now, this definitely seems like low-hanging fruit that can capitalize on the space and provide value. One way to think about Dynamic NFTs is that they enable tokenization over code execution. It's easier and more composable to trade NFTs than it is to transfer ownership over smart contracts. 

I'll be releasing a project soon that has a relatively simple take on this (and I'll talk more about the technical details post-release), but I hope to see other people iterating on this idea as well.