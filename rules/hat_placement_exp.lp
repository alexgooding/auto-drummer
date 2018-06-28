% The rules associated with experimental hat placement.

%Hats placed on every odd half-beat as a ground rhythm.
4 {chooseHit(h, T) : oddX2(T)}.

%Between 0 and 8 hats placed on odd quarter-beats.
0 {chooseHit(h, T) : odd(T)} 8.

%Between 0 and 2 hats placed on even quarter-beats.
0 {chooseHit(h, T) : even(T)} 2.

%Hit density constraint.

X {chooseHit(h, T) : time(T)} Y :- hatExpMin(X), hatExpMax(Y).

%Hit density parameters.

%hatExpMin(0).
%hatExpMax(16).
