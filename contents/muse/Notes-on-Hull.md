title: Notes on Hull

### Types of financial derivatives

Forward contracts are just agreements to buy/sell an asset at a certain price in the future. They don't cost anything to make (but presumably they're binding).

Futures are a market for the acquisition of assets in the future. You're buying or selling an asset, conditional on a delivery later on time. This means the price can fluctuate. Presumably the closer it is to the present, the more the futures price will reflect that?

Options are a contract that give you the right to buy or sell an asset at a specific price by some expiration date in the future. They cost money to purchase, but you don't have to exercise this right.

### Options

Options are interesting because they have large upside and capped downside. At worst, you eat the cost of purchasing the contract, but if the price skyrockets (or plummets), the price of the contract can increase by a lot.

Both the distance from the expiration date and volatility contribute to an increase in the option's price. Puts and calls are both upper-bounded by the price of the underlying stock price.

Puts are more bounded, however, because you can make at most \$X, where X is the price specified in the contract, and this only happens if the underlying stock goes all the way to 0.

Calls have higher theoretical bounds because the stock price can double, or more.

Furthermore, it's basically always better to sell your puts early because their bounded return. For calls, if your goal is to hold onto the underlying asset, you can always do better by exercising the call on the expiration date. If your goal is to make a profit, you can do better by selling the contract rather than exercising the option yourself.

