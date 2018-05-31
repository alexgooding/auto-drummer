% The rules associated with moderately constrained percussion placement.

%Percussion hits cannot be placed within two quarter-beats of another hit.
:- chooseHit(p, T), chooseHit(k, T-1).
:- chooseHit(p, T), chooseHit(s, T-1).
:- chooseHit(p, T), chooseHit(h, T-1).
:- chooseHit(p, T), chooseHit(k, T+1).
:- chooseHit(p, T), chooseHit(s, T+1).
:- chooseHit(p, T), chooseHit(h, T+1).
:- chooseHit(p, 16).