% Define

%Between 0 and 3 kicks must be assigned.
0 {chooseHit(k, T) : time(T)} 3.

%Defining even quarter-beats.
even(2*T) :- time(T), 2*T <= 16.

%Defining odd quarter-beats.
odd(2*T-1) :- time(T), 2*T-1 <= 16.

%Defining odd half-beats.
oddX2(4*T-3) :- time(T), 4*T-3 <= 16.

%Between 2 and 3 snares must be assigned to an odd quarter-beat.
2 {chooseHit(s, T) : odd(T)} 3.

%Hats placed on every odd half-beat as a ground rhythm.
4 {chooseHit(h, T) : oddX2(T)}.

%Between 0 and 8 hats placed on odd quarter-beats.
0 {chooseHit(h, T) : odd(T)} 8.

%Between 0 and 2 hats placed on even quarter-beats.
0 {chooseHit(h, T) : even(T)} 2.

%Between 0 and 1 percussion hits placed anywhere on the measure.
0 {chooseHit(p, T) : time(T)} 1.

%Between 0 and 4 ghost snare hits placed on even quarter-beats.
0 {chooseHit(g, T) : even(T)} 4.

%Constraints

%No kick on the last quarter-beat of the measure.
:- chooseHit(k, 16).

%Kicks and snares cannot be placed within 2 quarter-beats of each other
:- chooseHit(k, T), chooseHit(s, T+1).
:- chooseHit(k, T), chooseHit(s, T).
:- chooseHit(s, T), chooseHit(k, T+1).
:- chooseHit(s, T), chooseHit(k, T).
:- chooseHit(k, T), chooseHit(k, T+1).

%Snares cannot be placed 2 quarter-beats apart.
:- chooseHit(s, T), chooseHit(s, T+2).

%No quick repeating patterns of kicks and snares (k-s-k or s-k-s)
:- chooseHit(k, T), chooseHit(s, T+2), chooseHit(k, T+4).
:- chooseHit(s, T), chooseHit(k, T+2), chooseHit(s, T+4).

%Only even quarter-beat hats placed just before a kick hit.
:- chooseHit(h, 2*T), time(T), not chooseHit(k, 2*T+1).

%Percussion hits can only be placed where no other hit has been placed.
:- chooseHit(p, T), chooseHit(k, T).
:- chooseHit(p, T), chooseHit(s, T).
:- chooseHit(p, T), chooseHit(h, T).

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