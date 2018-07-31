% The rules associated with experimental snare placement.

%Between 2 and 3 snares must be assigned to an odd quarter-beat.
X {chooseHit(s, T) : odd(T)} Y :- snareMin(X), snareMax(Y).

%Snares cannot be placed 2 quarter-beats apart.
:- chooseHit(s, T), chooseHit(s, T+2).
