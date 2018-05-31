% The rules associated with mildly constrained kick placement.

%Kick on first beat.
chooseHit(k, 1).

%No kick on the last quarter-beat of the measure.
:- chooseHit(k, 16).
