# Test MinMax WithDepth(cut-off) with 2 (or more) different heuristics, which one is better?

We tested 2 different heuristics. Both heuristics assign values to each check to see if the game is over, based on whether a piece fulfills certain conditions. The difference between the two heuristics is:

    1. The utility results of each check will be summed.
    2. The overall utility value will be the maximum of each check.

Additionally, the final result will be multiplied by *20 if it is a winning state.

![alt text](images/how%20does%20our%20heuristic%20works.png "how does our heuristic works")

We chose these heuristics because they are two similar but different concepts. The first heuristic chooses a position where there are more moves that lead to victory, while the second heuristic chooses a position where there is a safer way to win.

These different ideas lead the bot to think about whether it is better to have a position where a rival's mistake leads to victory or a bot that sees the victory and focuses on it.

The first thing we did before testing the heuristics was to determine which depth was best to use when facing the heuristics using our best possible bot:

![alt text](images/games%20using%20different%20depth.PNG "games using different depth")

Based on our testing, we found that using depth 3 and 2 resulted in better performance for our bots. This may seem counterintuitive, but it's because our heuristics are focused on winning rather than considering the opponent's possible moves, so bots that see victories in fewer moves tend to perform better.

After determining the best depths, we had our bots play against each other, and the results were as follows:

    * gamereport 1 = heuristic 1 with depth 3 as black won against heuristic 2 with depth 3 as white
    * gamereport 2 = heuristic 1 with depth 3 as white won against heuristic 2 with depth 3 as black
    * gamereport 3 = heuristic 2 with depth 3 as black won against heuristic 1 with depth 2 as white
    * gamereport 4 = heuristic 1 with depth 2 as black won against heuristic 2 with depth 3 as white
    * gamereport 5 = heuristic 2 with depth 2 as black won against heuristic 1 with depth 3 as white
    * gamereport 6 = heuristic 1 with depth 3 as black won against heuristic 2 with depth 2 as white 


We concluded that while the two heuristics perform similarly, heuristic 1 is generally better than heuristic 2 when using the same depth. Therefore, we recommend using heuristic 1, which considers the sum of different utility results. Additionally, having the first move gives an advantage over the opponent, so it's also important to take that into consideration.


# Run the MinMax + α − β pruning algorithm and report a graph of #turn vs #pruning. Change the order of actions (to expand from the right) and report the same graph. Is it different? Why?

We ran the + α − β pruning algorithm using the same depth to find the best order of actions that results in the highest number of prunings. Initially, we manually changed the order of actions, but then we decided to use a randomizer to change the order of moves randomly each time. By doing this, we obtained the following graphs.

![alt text](images/prunnings%20using%20same%20depth.png. "prunnings using same depth")

![alt text](images/terminal%20boards%20using%20same%20depth.png "terminal boards using same depth")

After running the MinMax + α − β pruning algorithm to find the best order of actions to achieve the highest number of prunings, we initially tried manually changing the order of actions, but later implemented a randomizer to change the order of actions randomly for each sub-board generated. The resulting graph showed that using random moves could lead to more prunings and terminal boards, but it was also more likely to find an order of actions that was more harmful than beneficial.

Taking this into account, we ultimately decided on the best order of actions: SE, SW, NE, NW, E, W, S, N. Through trial and error, we discovered that bots tend to perform better when ending games by moving from the center towards the corners. Therefore, it is more likely to find terminal boards when the order of actions involves diagonal movements that aim to reach these corners.

In this case, the best order of actions is either order 2 or order 5, which start with an Eastward move, followed by a Northeast or Southeast move, and then a Northwest or Southwest move. These movements signify an attempt to gather pieces in the Northeast or Northwest, or Southeast or Southwest corners. This idea of gathering pieces in a corner is a simple yet effective strategy, and our experiments have shown that it is better than making random moves or non-diagonal moves.

Through these experiments, we have found that a human-like strategy of seeking out corners with pieces and moving from the center towards these corners results in better outcomes than making random or non-diagonal moves.

# Run the game once and report a graph of #turn vs #expanded states for the MinMax + α − β pruning and MinMaxWithDepth(cut-off) algorithms.

mogus