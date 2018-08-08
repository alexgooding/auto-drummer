%% Copyright (C) 2018 Alex Gooding

%% This program is free software: you can redistribute it and/or modify
%% it under the terms of the GNU General Public License as published by
%% the Free Software Foundation, either version 3 of the License, or
%% (at your option) any later version.

%% This program is distributed in the hope that it will be useful,
%% but WITHOUT ANY WARRANTY; without even the implied warranty of
%% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%% GNU General Public License for more details.

%% You should have received a copy of the GNU General Public License
%% along with this program.  If not, see <https://www.gnu.org/licenses/>.

%A set of boolean variables that determine which modifications to 
%the one bar pattern will take place.
{a}. {b}. {c}. {d}. {e}. {f}. {g}. {h}. {i}. {j}. 

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

%Additional facts to shift hits and to break the measure up further.
add(-2;0;2).

#show chooseHit/2.
#show fillHit/2.
