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

% The rules associated with mildly constrained kick snare interaction.

%Kicks and snares cannot be placed within 2 quarter-beats of each other
:- chooseHit(k, T), chooseHit(s, T+1).
:- chooseHit(k, T), chooseHit(s, T).
:- chooseHit(s, T), chooseHit(k, T+1).
:- chooseHit(k, T), chooseHit(k, T+1).

%No quick repeating patterns of kicks and snares (k-s-k or s-k-s)
:- chooseHit(k, T), chooseHit(s, T+2), chooseHit(k, T+4).
:- chooseHit(s, T), chooseHit(k, T+2), chooseHit(s, T+4).
