% The rules associated with conventional hat placement.

%Defining a boolean variable.
{b}.

%Hats placed on every odd half-beat or quarter-beat as a ground rhythm.
4 {chooseHit(h, T) : oddX2(T)} 4:- b.
8 {chooseHit(h, T) : odd(T)} 8:- not b.

%Between 0 and 2 hats placed on even quarter-beats.
0 {chooseHit(h, T) : even(T)} 2.

%Don't allow even quarter-beat hat hits when the groud beat is every half-beat.
:- chooseHit(h, 2*T), time(T), b.

%Hit density constraint.

X {chooseHit(h, T) : time(T)} Y :- hatMin(X), hatMax(Y).

%Hit density parameters.

hatMin(0).
hatMax(10) :- not b.
hatMax(4) :- b.