%A set of boolean variables that determine which modifications to 
%the one bar pattern will take place.
{a}. {b}. {c}. {d}. {e}. {f}. {g}. {h}. {i}. {j}. {k}. {l}. {m}. {n}.

%Extend the 1 measure pattern to the length of 2 bars or 32 quarter-beats.
%This depends on which booleans are True or not True.

chooseHit(k, T+16) :- chooseHit(k, T), time(T), not a.
chooseHit(k, T+16) :- chooseHit(k, T), odd1Q(T), not b.
chooseHit(k, T+16) :- chooseHit(k, T), odd2Q(T), not c.
chooseHit(k, T+16) :- chooseHit(k, T), odd3Q(T), not d.
chooseHit(k, T+16) :- chooseHit(k, T), odd4Q(T), not e.
chooseHit(s, T+16) :- chooseHit(s, T), time(T), not f.
chooseHit(s, T+16) :- chooseHit(s, T), odd1Q(T), not g.
chooseHit(s, T+16) :- chooseHit(s, T), odd2Q(T), not h.
chooseHit(s, T+16) :- chooseHit(s, T), odd3Q(T), not i.
chooseHit(s, T+16) :- chooseHit(s, T), odd4Q(T), not j.
chooseHit(h, T+16) :- chooseHit(h, T), time(T).
chooseHit(p, T+16) :- chooseHit(p, T), time(T).
chooseHit(g, T+16) :- chooseHit(g, T), time(T).

%Add variety to the second bar.

%Allow various 2 quarter-beat shifts of the kick and snare using the add facts.
1 {chooseHit(k, T+16+K) : add(K)} 1 :- chooseHit(k, T), odd1Q(T), a, b.
1 {chooseHit(k, T+16+K) : add(K)} 1 :- chooseHit(k, T), odd2Q(T), a, c.
1 {chooseHit(k, T+16+K) : add(K)} 1 :- chooseHit(k, T), odd3Q(T), a, d.
1 {chooseHit(k, T+16+K) : add(K)} 1 :- chooseHit(k, T), odd4Q(T), a, e.

1 {chooseHit(s, T+16+K) : add(K)} 1 :- chooseHit(s, T), odd1Q(T), f, g.
1 {chooseHit(s, T+16+K) : add(K)} 1 :- chooseHit(s, T), odd2Q(T), f, h.
1 {chooseHit(s, T+16+K) : add(K)} 1 :- chooseHit(s, T), odd3Q(T), f, i.
1 {chooseHit(s, T+16+K) : add(K)} 1 :- chooseHit(s, T), odd4Q(T), f, j.

%Possibility to place kick hits on the 19th quarter-beat and 27th quarter-beat.
chooseHit(k, 19) :- k.
chooseHit(k, 27) :- l.

%chooseHit(s, T+18) :- chooseHit(s, T), oddSH(T), m. 
%chooseHit(g, T+19) :- chooseHit(g, T), oddSH(T), n.

%Time constraints.
:- chooseHit(k, T), T > 32.
:- chooseHit(s, T), T > 32.
:- chooseHit(h, T), T > 32.
:- chooseHit(p, T), T > 32.
:- chooseHit(g, T), T > 32.

%Snares cannot be placed 2 or 4 quarter-beats apart.
:- chooseHit(s, T), chooseHit(s, T+2).
:- chooseHit(s, T), chooseHit(s, T+4).

%Additional facts to shift hits and to break the measure up further.
add(-2;0;2).

odd1Q(1;3).
odd2Q(5;7).
odd3Q(9;11).
odd4Q(13;15).