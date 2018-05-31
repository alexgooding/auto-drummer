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