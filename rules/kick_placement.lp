% The rules associated with kick placement.

%Between X and Y kicks must be assigned.
X {chooseHit(k, T) : time(T)} Y :- kickMin(X), kickMax(Y).

%Hit density parameters.

kickMin(0).
kickMax(3).