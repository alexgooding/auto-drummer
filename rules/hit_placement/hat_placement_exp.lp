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

% The rules associated with experimental hat placement.

%Hats placed on every odd half-beat as a ground rhythm.
4 {chooseHit(h, T) : oddX2(T)}.

%Between 0 and 8 hats placed on odd quarter-beats.
0 {chooseHit(h, T) : odd(T)} 8.

%Between 0 and 2 hats placed on even quarter-beats.
0 {chooseHit(h, T) : even(T)} 2.

%Hit density constraint.

X {chooseHit(h, T) : time(T)} Y :- hatExpMin(X), hatExpMax(Y).
