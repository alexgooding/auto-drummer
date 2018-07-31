% The rules associated with percussion placement.

%Between X and Y percussion hits placed anywhere on the measure.
X {chooseHit(p, T) : time(T)} Y :- percMin(X), percMax(Y).
