% Generate


% Define

%Between 2 and 4 kicks must be assigned.
2 {chooseHit(k, T) : time(T)} 4.

%Defining odd quarterbeats.
odd(2*T-1) :- time(T), 2*T-1 <= 16.

%Between 2 and 3 snares must be assigned to an odd quarterbeat.
%One in the first half of the measure, one in the second half as a minimum.
%1 {chooseHit(s, T) : odd(T), T <= 7} 1.
%1 {chooseHit(s, T) : odd(T), T >= 9} 1.
%0 {chooseHit(s, T) : odd(T)} 1.
2 {chooseHit(s, T) : odd(T)} 3.

%Hats placed on every odd quarterbeat.
8 {chooseHit(h, T) : odd(T)}.

%Kicks and snares cannot be placed within 2 quarterbeats of each other
:- chooseHit(k, T), chooseHit(s, T+1).
:- chooseHit(k, T), chooseHit(s, T).
:- chooseHit(k, T), chooseHit(s, T-1).
:- chooseHit(s, T), chooseHit(k, T+1).
:- chooseHit(s, T), chooseHit(k, T).
:- chooseHit(s, T), chooseHit(k, T-1).
:- chooseHit(k, T), chooseHit(k, T+1).
:- chooseHit(k, T), chooseHit(k, T-1).


% Facts

%Kick on first beat.
chooseHit(k, 1).

%Defining hit types and time period.
hit(k). hit(s). %hit(h).
time(1..16).

#show chooseHit/2.