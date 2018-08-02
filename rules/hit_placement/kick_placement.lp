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

% The rules associated with kick placement.

%Between X and Y kicks must be assigned.
X {chooseHit(k, T) : time(T)} Y :- kickMin(X), kickMax(Y).

%Kick on first beat.
chooseHit(k, 1).
