%Defining the relevant quarter-beat number facts for a one measure pattern.

%Segmenting the measure into 16 quarter-beats.
time(1..16).

%Defining even quarter-beats.
even(2;4;6;8;10;12;14;16). 

%Defining odd quarter-beats.
odd(1;3;5;7;9;11;13;15).

%Defining odd half-beats.
oddX2(1;5;9;13). 

%Defining first half of the measures odd quarter-beats.
oddFH(3;5;7).

%Defining second half of the measures odd quarter-beats.
oddSH(11;13;15).

%Choose what output to show.
#show chooseHit/2.
% The rules associated with kick placement.

%Between X and Y kicks must be assigned.
X {chooseHit(k, T) : time(T)} Y :- kickMin(X), kickMax(Y).

%Hit density parameters.

%kickMin(0).
%kickMax(3).
% The rules associated with mildly constrained kick placement.

%Kick on first beat.
chooseHit(k, 1).

%No kick on the last quarter-beat of the measure.
:- chooseHit(k, 16).
% The rules associated with moderately constrained kick placement.

%No kicks 1 beat apart.
:- chooseHit(k, T), chooseHit(k, T+4).
% The rules associated with conventional snare placement.

%2 snares must be assigned to an odd quarter-beat conventionally.
1 {chooseHit(s, T) : oddFH(T)} 1.
1 {chooseHit(s, T) : oddSH(T)} 1.

%At least one snare must fall on the 5th or 13th quarter-beat of the measure.
:- not chooseHit(s, 5), not chooseHit(s, 13).

%Snare cannot fall on the 3rd quarter-beat of the measure.
:- chooseHit(s, 3).
% The rules associated with mildly constrained kick snare interaction.

%Kicks and snares cannot be placed within 2 quarter-beats of each other
:- chooseHit(k, T), chooseHit(s, T+1).
:- chooseHit(k, T), chooseHit(s, T).
:- chooseHit(s, T), chooseHit(k, T+1).
:- chooseHit(k, T), chooseHit(k, T+1).

%No quick repeating patterns of kicks and snares (k-s-k or s-k-s)
:- chooseHit(k, T), chooseHit(s, T+2), chooseHit(k, T+4).
:- chooseHit(s, T), chooseHit(k, T+2), chooseHit(s, T+4).
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

X {chooseHit(h, T) : time(T)} Y :- hatConvMin(X), hatConvMax(Y).

%Hit density parameters.

hatConvMin(0).
hatConvMax(10) :- not b.
hatConvMax(4) :- b.
% The rules associated with mildly constrained hat placement.

%Only even quarter-beat hats placed just before a kick hit.
:- chooseHit(h, 2*T), time(T), not chooseHit(k, 2*T+1).
% The rules associated with moderately constrained hat placement.

%Even quarter-beat hats are not placed after a kick or snare hit.
:- chooseHit(h, 2*T), time(T), chooseHit(k, 2*T-1).
:- chooseHit(h, 2*T), time(T), chooseHit(s, 2*T-1).
% The rules associated with percussion placement.

%Between X and Y percussion hits placed anywhere on the measure.
X {chooseHit(p, T) : time(T)} Y :- percMin(X), percMax(Y).

%Hit density parameters.

%percMin(0).
%percMax(1).
% The rules associated with mildly constrained percussion placement.

%Percussion hits can only be placed where no other hit has been placed.
:- chooseHit(p, T), chooseHit(k, T).
:- chooseHit(p, T), chooseHit(s, T).
:- chooseHit(p, T), chooseHit(h, T).
% The rules associated with moderately constrained percussion placement.

%Percussion hits cannot be placed within two quarter-beats of another hit.
:- chooseHit(p, T), chooseHit(k, T-1).
:- chooseHit(p, T), chooseHit(s, T-1).
:- chooseHit(p, T), chooseHit(h, T-1).
:- chooseHit(p, T), chooseHit(k, T+1).
:- chooseHit(p, T), chooseHit(s, T+1).
:- chooseHit(p, T), chooseHit(h, T+1).
:- chooseHit(p, 16).
% The rules associated with ghost snare placement.

%Between X and Y ghost snare hits placed on even quarter-beats.
X {chooseHit(g, T) : even(T)} Y :- gSnareMin(X), gSnareMax(Y).

%Hit density parameters.

%gSnareMin(0).
%gSnareMax(3).
% The rules associated with mildly constrained ghost snare placement.

%Ghost snares cannot be placed on the same quarter-beat as a different type of hit.
:- chooseHit(g, T), chooseHit(k, T).
:- chooseHit(g, T), chooseHit(s, T).
:- chooseHit(g, T), chooseHit(h, T).
:- chooseHit(g, T), chooseHit(p, T).
% The rules associated with moderately constrained percussion placement.

%Ghost snare hits must placed suitably to create shuffle - they can fill gaps where hats are not placed.
:- chooseHit(g, T), chooseHit(k, T-1), not chooseHit(s, T+1).
:- chooseHit(g, T-1), chooseHit(s, T), chooseHit(g, T+1).
:- chooseHit(g, T-1), chooseHit(k, T), chooseHit(g, T+1).
:- chooseHit(g, T), chooseHit(s, T-1).
:- chooseHit(g, T), chooseHit(s, T+1), not chooseHit(g, T-2).

kickMin(0).
kickMax(3).
snareMin(2).
snareMax(3).
hatExpMin(0).
hatExpMax(16).
percMin(0).
percMax(1).
gSnareMin(0).
gSnareMax(3).

