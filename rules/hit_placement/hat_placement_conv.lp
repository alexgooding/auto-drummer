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
