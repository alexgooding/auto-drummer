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

%Defining the relevant quarter-beat number facts for a one measure pattern.

%Segmenting the measure into 16 quarter-beats.
time(1..16).

%Defining even quarter-beats.
even(2;4;6;8;10;12;14;16). 

%Defining odd quarter-beats.
odd(1;3;5;7;9;11;13;15).

%Defining odd half-beats.
oddX2(1;5;9;13). 

%Defining first half of the measures odd quarter-beats.
oddFH(3;5;7).

%Defining second half of the measures odd quarter-beats.
oddSH(11;13;15).

%Choose what output to show.
#show chooseHit/2.
