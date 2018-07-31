% The rules associated with mildly constrained percussion placement.

%Percussion hits can only be placed where no other hit has been placed.
:- chooseHit(p, T), chooseHit(k, T).
:- chooseHit(p, T), chooseHit(s, T).
:- chooseHit(p, T), chooseHit(h, T).
