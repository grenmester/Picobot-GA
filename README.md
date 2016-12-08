# Picobot GA

Our program is based off of [Picobot](https://www.cs.hmc.edu/picobot/), a programming challenge that wherein a pixel with user-defined instructions must touch every pixel in a map without any memory. The Program class creates a list of all possible Picobot rules, specifies how a program will move given its surroundings, and controls mutations and program breeding, while the World class creates an ASCII representation of the Picobot map and provides the means for the Picobot programs to gauge their surroundings and move. Finally, the final global functions control a genetic algorithm in which the Picobot programs that reach the most number of squares are allowed to breed to create a new generation of programs in the hopes that each generation produces a better set of rules than the last.

### Test Run

We tested our code by running `GA`, the genetic algorithm code, with 200 individuals per generation and 20 generations to optimize runtime and performance. To refine our program, we altered the number of trials that are run to calculate each program's fitness, the number of steps each program takes in a trial, the mutation rate, the fraction of programs we consider fit to mate, and the number of states allowed. Increasing trials reduces variability in the fitness scores but takes longer to run, so we settled on 10 as an optimal amount. Increasing the number of steps increases the fitnesses of our programs overall (ones that are inefficient but very fit are allowed to run), and only increases runtime slightly, so we settled on 2,000 (enough for a program to fill the board about 4 times, in case it is repetitive). The mutation rate was one of the hardest variables to optimize. If it's too low, fitnesses stagnate after a certain number of generations, but if it is too high, fitnesses can decrease suddenly after some generations. We found that a mutation rate of 0.2 provided the best balance. Decreasing the fraction of programs we consider fit to mate can increase fitness scores, but can also lead to stagnation; this variable must be balanced with the mutation rate to balance fitness and stagnation. We found that a rate of 0.1 matched well with our 0.2 mutation rate. Finally, increasing the number of states can increase fitness by allowing more complex programs to run, but increases runtime. Reducing the states to 4 decreased fitness significantly (to 0.3) and raising it did not have a significant effect on fitness, so we left it at 5. Overall, we created each new generation by keeping the top 10% of programs, and breeding two randomly selected programs from the 10% to generate the rest of the generation. Meanwhile, a mutation is introduced to 20% of the new generation (one rule is randomized) to maintain variation in the gene pool.

Our fittest Picobot program:

```
0 NExx -> S 4
0 NxWx -> E 0
0 Nxxx -> W 1
0 xExS -> N 4
0 xExx -> W 3
0 xxWS -> E 3
0 xxWx -> S 0
0 xxxS -> N 0
0 xxxx -> N 0
1 NExx -> S 0
1 NxWx -> S 4
1 Nxxx -> S 4
1 xExS -> W 0
1 xExx -> N 1
1 xxWS -> E 2
1 xxWx -> N 1
1 xxxS -> E 0
1 xxxx -> W 4
2 NExx -> W 2
2 NxWx -> S 2
2 Nxxx -> E 0
2 xExS -> N 0
2 xExx -> S 3
2 xxWS -> E 3
2 xxWx -> N 2
2 xxxS -> E 0
2 xxxx -> W 4
3 NExx -> W 1
3 NxWx -> E 1
3 Nxxx -> S 2
3 xExS -> N 1
3 xExx -> N 2
3 xxWS -> E 0
3 xxWx -> S 3
3 xxxS -> E 3
3 xxxx -> S 4
4 NExx -> S 2
4 NxWx -> E 1
4 Nxxx -> E 0
4 xExS -> W 4
4 xExx -> W 3
4 xxWS -> E 2
4 xxWx -> S 4
4 xxxS -> W 2
4 xxxx -> S 4
```

Our fittest Picobot had a fitness of 0.9716. It filled the room by moving north and south in each column while moving west, and then bouncing off the southwest corner back to the east wall. As with most of our programs, this one sometimes has trouble with corners and the left and right edges, but can consistently fill more than 95% of the room.

***

Picobot GA was written by Jacky Lee, Chris Ferrarin, and Evan Liang.
