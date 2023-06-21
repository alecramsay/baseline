Unfortunately, six weeks is long enough for me to completely lose all context of where we were in the process of getting baselines working for all this states. This is a combination of what I can reconstruct and infer along with some questions. 

I'd love your sense of where things are -- i.e., what data you expect and what you do -- so I can compare that with my notes.

As far as I can tell, we seemed to have stopped when were working on two issues:
1. Perf for NY, CA, and TX; and
2. Some combination of water and land zero-population precincts for LA, MD, and NJ and KS, NV, and UT

I *think* we stopped when you're trying various strategies for getting NY (and implicitly CA and TX, I think) to run in a reasonable amount of time / rebalance.

Right around that time though, we were also making mods to deal with unpopulated precincts. I did some experiments with modifying the graph/adjacencies to bridge across unpopulated precincts, but that code is disabled. I *think* you were going to some epsilon trick. I found this note that I wrote in Slack: "When we know you can handle zero population (land and water) with your epsilon trick, I can not set the water-only flag in my script and ultimately I can rip out that code." I don't know if you did that / are doing that.

So, I have two questions:
* What bug did you fix? Was it the rebalancing stuff to make NY (and others) run / run faster?
* Are you doing the epsilon trick? and should I still be removing water-only precincts from the data and adjacencies files? I still have the code for that in my prep scripts--I just can remember if I should be using it or whether you handle all zero population precincts now (both water-only and with land).

Sorry that I can't remember better. Happy to chat, if that's easier.