% The rules associated with ghost snare placement.

%Between X and Y ghost snare hits placed on even quarter-beats.
X {chooseHit(g, T) : even(T)} Y :- gSnareMin(X), gSnareMax(Y).

%Hit density parameters.

%gSnareMin(0).
%gSnareMax(3).
