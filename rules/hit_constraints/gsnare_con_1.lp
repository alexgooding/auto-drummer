% The rules associated with mildly constrained ghost snare placement.

%Ghost snares cannot be placed on the same quarter-beat as a different type of hit.
:- chooseHit(g, T), chooseHit(k, T).
:- chooseHit(g, T), chooseHit(s, T).
:- chooseHit(g, T), chooseHit(h, T).
:- chooseHit(g, T), chooseHit(p, T).
