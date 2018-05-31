% Define

%Between 0 and 3 kicks must be assigned.
0 {chooseHit(k, T) : time(T)} 3.

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

%Defining a boolean variable.
{b}.

%Between 2 and 4 snares must be assigned to an odd quarter-beat conventionally.
1 {chooseHit(s, T) : oddFH(T)} 1.
1 {chooseHit(s, T) : oddSH(T)} 1.

%Hats placed on every odd half-beat or quarter-beat as a ground rhythm.
4 {chooseHit(h, T) : oddX2(T)} 4:- b.
8 {chooseHit(h, T) : odd(T)} 8:- not b.

%Between 0 and 2 hats placed on even quarter-beats.
0 {chooseHit(h, T) : even(T)} 2.

%Between 0 and 1 percussion hits placed anywhere on the measure.
0 {chooseHit(p, T) : time(T)} 1.

%Between 0 and 4 ghost snare hits placed on even quarter-beats.
0 {chooseHit(g, T) : even(T)} 4.

%Constraints

%No kick on the last quarter-beat of the measure.
:- chooseHit(k, 16).

%No kicks 1 beat apart.
:- chooseHit(k, T), chooseHit(k, T+4).

%Kicks and snares cannot be placed within 2 quarter-beats of each other
:- chooseHit(k, T), chooseHit(s, T+1).
:- chooseHit(k, T), chooseHit(s, T).
:- chooseHit(s, T), chooseHit(k, T+1).
:- chooseHit(s, T), chooseHit(k, T).
:- chooseHit(k, T), chooseHit(k, T+1).

%At least one snare must fall on the 5th or 13th quarter-beat of the measure.
:- not chooseHit(s, 5), not chooseHit(s, 13).

%No quick repeating patterns of kicks and snares (k-s-k or s-k-s)
:- chooseHit(k, T), chooseHit(s, T+2), chooseHit(k, T+4).
:- chooseHit(s, T), chooseHit(k, T+2), chooseHit(s, T+4).

%Only even quarter-beat hats placed just before a kick hit and not after a kick or snare hit. 
%False if using half-beat hats too.
:- chooseHit(h, 2*T), time(T), not chooseHit(k, 2*T+1).
:- chooseHit(h, 2*T), time(T), chooseHit(k, 2*T-1).
:- chooseHit(h, 2*T), time(T), chooseHit(s, 2*T-1).
:- chooseHit(h, 2*T), time(T), b.

%Percussion hits cannot be placed within two quarter-beats of another hit.
:- chooseHit(p, T), chooseHit(k, T-1).
:- chooseHit(p, T), chooseHit(s, T-1).
:- chooseHit(p, T), chooseHit(h, T-1).
:- chooseHit(p, T), chooseHit(k, T).
:- chooseHit(p, T), chooseHit(s, T).
:- chooseHit(p, T), chooseHit(h, T).
:- chooseHit(p, T), chooseHit(k, T+1).
:- chooseHit(p, T), chooseHit(s, T+1).
:- chooseHit(p, T), chooseHit(h, T+1).
:- chooseHit(p, 16).

%Ghost snare hits must placed suitably to create shuffle - they can fill gaps where hats are not placed.
:- chooseHit(g, T), chooseHit(k, T).
:- chooseHit(g, T), chooseHit(s, T).
:- chooseHit(g, T), chooseHit(h, T).
:- chooseHit(g, T), chooseHit(p, T).
:- chooseHit(g, T), chooseHit(k, T-1), not chooseHit(s, T+1).
:- chooseHit(g, T-1), chooseHit(s, T), chooseHit(g, T+1).
:- chooseHit(g, T-1), chooseHit(k, T), chooseHit(g, T+1).
:- chooseHit(g, T), chooseHit(s, T-1).
:- chooseHit(g, T), chooseHit(s, T+1), not chooseHit(g, T-2).

% Facts

%Kick on first beat.
chooseHit(k, 1).

%Defining the time period.
time(1..16).

#show chooseHit/2.