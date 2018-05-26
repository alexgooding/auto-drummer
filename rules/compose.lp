% Define

%Between 1 and 3 kicks must be assigned.
1 {chooseHit(k, T) : time(T)} 3.

%Defining odd quarterbeats.
odd(2*T-1) :- time(T), 2*T-1 <= 16.

%Between 2 and 3 snares must be assigned to an odd quarter-beat.
2 {chooseHit(s, T) : odd(T)} 3.

%Hats placed on every odd quarterbeat.
8 {chooseHit(h, T) : odd(T)}.

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

%No kick on the last quarter-beat of the measure.
:- chooseHit(k, 16).

% Facts

%Kick on first beat.
chooseHit(k, 1).

%Defining hit types and time period.
hit(k). hit(s). %hit(h).
time(1..16).

#show chooseHit/2.