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

% The rules associated with conventional snare placement.

%2 snares must be assigned to an odd quarter-beat conventionally.
1 {chooseHit(s, T) : oddFH(T)} 1.
1 {chooseHit(s, T) : oddSH(T)} 1.

%At least one snare must fall on the 5th or 13th quarter-beat of the measure.
:- not chooseHit(s, 5), not chooseHit(s, 13).

%Snare cannot fall on the 3rd quarter-beat of the measure.
:- chooseHit(s, 3).
