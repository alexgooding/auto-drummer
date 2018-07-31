% The rules associated with moderately constrained hat placement.

%Even quarter-beat hats are not placed after a kick or snare hit.
:- chooseHit(h, 2*T), chooseHit(k, 2*T-1).
:- chooseHit(h, 2*T), chooseHit(s, 2*T-1).
