% The rules associated with conventional snare placement.

%2 snares must be assigned to an odd quarter-beat conventionally.
1 {chooseHit(s, T) : oddFH(T)} 1.
1 {chooseHit(s, T) : oddSH(T)} 1.

%At least one snare must fall on the 5th or 13th quarter-beat of the measure.
:- not chooseHit(s, 5), not chooseHit(s, 13).

%Snare cannot fall on the 3rd quarter-beat of the measure.
:- chooseHit(s, 3).
