% The rules associated with moderately constrained percussion placement.

%Ghost snare hits must placed suitably to create shuffle - they can fill gaps where hats are not placed.
:- chooseHit(g, T), chooseHit(k, T-1), not chooseHit(s, T+1).
:- chooseHit(g, T-1), chooseHit(s, T), chooseHit(g, T+1).
:- chooseHit(g, T-1), chooseHit(k, T), chooseHit(g, T+1).
:- chooseHit(g, T), chooseHit(s, T-1).
:- chooseHit(g, T), chooseHit(s, T+1), not chooseHit(g, T-2).

