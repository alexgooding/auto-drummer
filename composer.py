import subprocess
from os.path import join as pjoin
from os import remove as remove_file
import json
from random import randint

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import FixedLocator

from midiutil import MIDIFile

#Configure Clingo parameters

clingo_path = 'solver\\clingo.exe'
clingo_options = ['--outf=2','-n 0', '--time-limit=10']
clingo_command = [clingo_path] + clingo_options

#Define rule paths

all_rules = [['rules\\hit_placement\\kick_placement.lp', 'rules\\hit_constraints\\kick_con_1.lp', 'rules\\hit_constraints\\kick_con_2.lp'], \
             ['rules\\hit_placement\\snare_placement_exp.lp', 'rules\\hit_placement\\snare_placement_conv.lp'], \
             ['rules\\hit_constraints\\kick_snare_con_1.lp'], \
             ['rules\\hit_placement\\hat_placement_exp.lp', 'rules\\hit_placement\\hat_placement_conv.lp' , 'rules\\hit_constraints\\hat_con_1.lp', 'rules\\hit_constraints\\hat_con_2.lp'], \
             ['rules\\hit_placement\\perc_placement.lp', 'rules\\hit_constraints\\perc_con_1.lp', 'rules\\hit_constraints\\perc_con_2.lp'], \
             ['rules\\hit_placement\\gsnare_placement.lp', 'rules\\hit_constraints\\gsnare_con_1.lp', 'rules\\hit_constraints\\gsnare_con_2.lp']]

#Solve the ruleset by accessing the Clingo solver through the command line.
def _solve(program):
    input = program.encode()
    #Stop the console window from showing during execution.
    #This is used when distributing as a .exe
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    process = subprocess.Popen(clingo_command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=startupinfo)
    output, error = process.communicate(input)
    result = json.loads(output.decode())
    if result['Result'] == 'SATISFIABLE':
        return [value['Value'] for value in result['Call'][0]['Witnesses']]
    else:
        return None

#Write the one bar problem rule set.
def _write_problem(constraints):
    rules = ['rules\\time_facts\\time.lp']
    i = 0
    for row in all_rules:
        for j in range(0, len(row)):
            if constraints[i][j]:
                rules.append(all_rules[i][j])
        i += 1
    #rules.append('rules\\time_facts\\time.lp')
    with open('rules\\temp\\1_bar_problem.lp', 'w') as outfile:
        for fname in rules:
            with open(fname) as infile:
                outfile.write(infile.read())    

#Solve the one bar problem in Clingo, specifying what kind of pattern will be generated.
#Print the number of solutions.
def _generate_solutions(constraints, user_input):
    _write_problem(constraints)
    if user_input:     
        with open('rules\\temp\\1_bar_problem.lp', 'a') as outfile:
            outfile.write('\n'.join(user_input) + '\n')
    problem = open('rules\\temp\\1_bar_problem.lp', 'r').read()
    solutions = _solve(problem)
    #Print the number of patterns found.
    if solutions is not None:
        print(str(len(solutions)) + " 1 bar patterns have been found.\n")
    else:
        print("No patterns have been found.\n")

    return solutions


#Represent hit_list as a table.

def _print_hits(pattern_index, hit_list, humanisation, pattern_length = 1): 

    #X represents the data points to be plotted on the grid. 
    #It also stores velocity data about each hit.
    X = np.zeros((4, 16 * pattern_length))

    #iterator
    j = 0

    for i in hit_list:
        if i[0] == 'k':
            X[3][int(i[1])-1] = 1./(volume-abs(humanisation[j])*300)
        if i[0] == 's':
            X[2][int(i[1])-1] = 1./(volume-abs(humanisation[j])*300)
        if i[0] == 'g':
            X[2][int(i[1])-1] = 1./(40-abs(humanisation[j])*300)
        if i[0] == 'h':
            X[1][int(i[1])-1] = 1./(volume-abs(humanisation[j])*300)
        if i[0] == 'p':
            X[0][int(i[1])-1] = 1./(volume-abs(humanisation[j])*300)
        j += 1

    #Normalise zero values for heat mapping purposes.
    normal_value = np.amax(X) + 0.005
    X[X == 0] = normal_value

    #Plot figure.
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(X, cmap=plt.get_cmap('gist_gray'))

    y_labels = ['Percussion', 'Hat', 'Snare', 'Kick']
    ax.set_xticks(list(range(0, 16 * pattern_length)))
    ax.set_yticks(list(range(0, 4)))
    ax.set_yticklabels(y_labels)
    ax.set_xticklabels(list(range(1, 16 * pattern_length + 1)))
    
    minor_xlocator = AutoMinorLocator(2)
    minor_ylocator = FixedLocator([x + 0.5 for x in range(0, 16 * pattern_length)])
    ax.xaxis.set_minor_locator(minor_xlocator)
    ax.yaxis.set_minor_locator(minor_ylocator)
    ax.grid(which='minor', color='0.4', linestyle='dashed')
    
    fig.patch.set_facecolor("None")

    canvas = FigureCanvas(fig)

    canvas.setStyleSheet("background-color:transparent;")

    canvas.draw()

    return canvas


#Create MIDI representation of the drum pattern.

#offset needed to convert to MIDI time.
offset = 0.25
duration = 0.125 # In beats
tempo    = 174  # In BPM
volume   = 100  # 0-127, as per the MIDI standard

#Write a MIDI file for a set of hits with a given file name.
def _write_midi(hit_list, fill_list, save_path, file_name, humanisation):
    midi_patttern = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                          # automatically)
    midi_patttern.addTempo(0, 0, tempo)

    #iterator
    j = 0
    #Add kicks to middle C, snares to C#3 and hats to D3.
    for i in hit_list:
        if i[0] == 'k':
            if i[1] == '1':
                midi_patttern.addNote(0, 0, 60, float(i[1])/4-offset, duration, int(volume-abs(humanisation[j])*300))
            else:
                midi_patttern.addNote(0, 0, 60, float(i[1])/4-offset+humanisation[j], duration, int(volume-abs(humanisation[j])*300))
        if i[0] == 's':
            if i[1] == '1':
                midi_patttern.addNote(0, 0, 61, float(i[1])/4-offset, duration, int(volume-abs(humanisation[j])*300))
            else:
                midi_patttern.addNote(0, 0, 61, float(i[1])/4-offset+humanisation[j], duration, int(volume-abs(humanisation[j])*300))
        if i[0] == 'g':
            if i[1] == '1':
                midi_patttern.addNote(0, 0, 61, float(i[1])/4-offset, duration, int(40-abs(humanisation[j])*300))
            else:
                midi_patttern.addNote(0, 0, 61, float(i[1])/4-offset+humanisation[j], duration, int(40-abs(humanisation[j])*300))
        if i[0] == 'h':
            if i[1] == '1':
                midi_patttern.addNote(0, 0, 62, float(i[1])/4-offset, duration, int(volume-abs(humanisation[j])*300))
            else:
                midi_patttern.addNote(0, 0, 62, float(i[1])/4-offset+humanisation[j], duration, int(volume-abs(humanisation[j])*300))
        if i[0] == 'p':
            if i[1] == '1':
                midi_patttern.addNote(0, 0, 63, float(i[1])/4-offset, duration, int(volume-abs(humanisation[j])*300))
            else:
                midi_patttern.addNote(0, 0, 63, float(i[1])/4-offset+humanisation[j], duration, int(volume-abs(humanisation[j])*300))
        j += 1

    for i in fill_list:
        if i[0] == 'k':
            midi_patttern.addNote(0, 0, 60, float(i[1])/4-offset+humanisation[j], duration, int(volume-15-abs(humanisation[j])*500))
        if i[0] == 's':
            midi_patttern.addNote(0, 0, 61, float(i[1])/4-offset+humanisation[j], duration, int(volume-10-abs(humanisation[j])*500))
        if i[0] == 'h':
            midi_patttern.addNote(0, 0, 62, float(i[1])/4-offset+humanisation[j], duration, int(volume-12-abs(humanisation[j])*500))
            
    file_path = pjoin(save_path, file_name)
    with open(file_path, "wb") as output_file:
        midi_patttern.writeFile(output_file) 

#Extend the one bar pattern to a given length with given contraints.
def _extend_pattern(pattern, extended_length, constraints, fills):
    #Maps out the location and length of fills within the pattern.
    fill_locations = []

    final_solution = pattern

    #extended_constraints removes the placement rule sets as they are not needed.
    extended_constraints = constraints[:]

    extended_constraints[0][0] = False
    extended_constraints[1][:] = False, False
    extended_constraints[3][0:1] = False, False
    extended_constraints[4][0] = False
    extended_constraints[5][0] = False

    #Create the list of base rule sets to add to the n length problem.
    n_bar_rules_base = ['rules\\pattern_extension\\extend_to_n_bars.lp']
    i = 0
    for row in all_rules:
        for j in range(0, len(row)):
            if extended_constraints[i][j]:
                n_bar_rules_base.append(all_rules[i][j])
        i += 1

    for j in range(2, extended_length + 1):

        n_bar_rules = n_bar_rules_base[:]

        #Determine whether a fill should be placed within the even bar.
        #0 is no fill, 1 is a short fill (1 beat) and 2 a long fill (2 beats).
        fill_type = 0
        if fills:
            if j % 2 == 0:
                fill_type = randint(0, 1)
            if j % 4 == 0:
                fill_type = randint(0, 2)

        #Add the start and end point of any fills present in terms of quarter-beats.
        fill_locations.append(j*16-fill_type*4)
        fill_locations.append(j*16)

        #Add the relevant fill rule set to the problem rules.
        if fill_type != 0:
            n_bar_rules.append('rules\\fills\\fill_' + str(fill_type) + '.lp')

        #Generate the relevant time facts for this iteration.
        extended_time = _extend_time((j-2) * 16)

        #Add limit to keep chosen hits within pattern length for this iteration.
        extended_time_constraints = _extend_time_constraints(fill_type, j * 16)

        #Write a new problem rule set for the extended pattern.
        with open('rules\\temp\\' + str(j) + '_bar_problem.lp', 'w') as outfile:
            for fname in n_bar_rules:
                with open(fname) as infile:
                    outfile.write(infile.read())

        with open('rules\\temp\\' + str(j) + '_bar_problem.lp', 'a') as outfile:
            outfile.write('\n'.join(extended_time) + '\n')
            outfile.write('\n'.join(extended_time_constraints) + '\n')
            #Add the chosen hits from the previous bar.  
            outfile.write('\n'.join([hit + '.' for hit in final_solution]) + '\n')
            
        problem = open('rules\\temp\\' + str(j) + '_bar_problem.lp', 'r').read()
        solutions = _solve(problem)

        #Return None if no valid solutions are found to allow another attempt.
        if solutions == None:
            return None, fill_locations
        print(str(len(solutions)) + " " + str(j) + " bar patterns have been found based on the randomly selected one bar pattern.\n")
        rand_index = randint(0, len(solutions)-1)
        final_solution = solutions[rand_index][:] 
    return final_solution, fill_locations

#Construct a list with new time facts relevant to the extended problem.
#n represents the number of quarter-beats we are extending the two bar pattern by.
def _extend_time(n):
    extended_time = []
    min_time = 1 + n
    max_time = 16 + n
    max_1Q = 3 + n
    min_2Q = 5 + n
    max_2Q = 7 + n
    min_3Q = 9 + n
    max_3Q = 11 + n
    min_4Q = 13 + n
    max_4Q = 15 + n
    extended_time.append("time(" + str(min_time) + ".." + str(max_time) + "). ")
    extended_time.append("odd1Q(" + str(min_time) + ";" + str(max_1Q) + "). ")
    extended_time.append("odd2Q(" + str(min_2Q) + ";" + str(max_2Q) + "). ")
    extended_time.append("odd3Q(" + str(min_3Q) + ";" + str(max_3Q) + "). ")
    extended_time.append("odd4Q(" + str(min_4Q) + ";" + str(max_4Q) + "). ")
    extended_time.append("oddSH(" + str(min_3Q) + ";" + str(max_3Q) + ";" + str(min_4Q) + ";" + str(max_4Q) + "). ")

    return extended_time

#Construct a list of time constraints for ordinary hits and fill hits.
def _extend_time_constraints(fill_type, limit):
    extended_time_constraints = []
    if fill_type == 0:
        extended_time_constraints.append(":- chooseHit(k, T), T > " + str(limit) + ". ")
        extended_time_constraints.append(":- chooseHit(s, T), T > " + str(limit) + ". ")
        extended_time_constraints.append(":- chooseHit(h, T), T > " + str(limit) + ". ")
        extended_time_constraints.append(":- chooseHit(p, T), T > " + str(limit) + ". ")
        extended_time_constraints.append(":- chooseHit(g, T), T > " + str(limit) + ". ")
    else:
        fill_limit = limit - 4*fill_type
        minimum = limit - 16
        extended_time_constraints.append(":- chooseHit(k, T), T > " + str(limit) + ". ")
        extended_time_constraints.append(":- chooseHit(s, T), T > " + str(limit) + ". ")
        extended_time_constraints.append(":- chooseHit(h, T), T > " + str(limit) + ". ")
        extended_time_constraints.append(":- chooseHit(p, T), T > " + str(limit) + ". ")
        extended_time_constraints.append(":- chooseHit(g, T), T > " + str(limit) + ". ")
        extended_time_constraints.append(":- fillHit(k, T), T <= " + str(fill_limit) + ", T > " + str(minimum) + ". ")
        extended_time_constraints.append(":- fillHit(s, T), T <= " + str(fill_limit) + ", T > " + str(minimum) + ". ")
        extended_time_constraints.append(":- fillHit(h, T), T <= " + str(fill_limit) + ", T > " + str(minimum) + ". ")

    return extended_time_constraints

#Iterate over the 1 bar patterns until a valid 2+ bar pattern is found (within the search limit).
#This only applies when attempting to generate a 2+ bar pattern. Otherwise a random 1 bar pattern is chosen.
def _search_solutions(solutions, constraints, fills, pattern_length, search_limit):
    rand_solution = None
    fill_locations = None
    i = 0
    while(rand_solution == None and i < search_limit):
        rand_index = randint(0, len(solutions)-1)
        rand_solution = solutions[rand_index][:]
        #Allow for extension of the base pattern if pattern_length is not 1.
        if pattern_length != 1:
            rand_solution,  fill_locations = _extend_pattern(rand_solution, pattern_length, constraints, fills)
        i += 1 

    return rand_solution, rand_index, fill_locations   

#Generate n random patterns from the answer set, depending on the rules chosen and any user input.
#A level of humanisation is chosen between 0 and 0.05. 
#Print and store solutions as MIDI files in the save path with a defined file name. Defaults to 1 pattern of length 1 bar with no user input.
def generate_patterns(constraints, fills, save_path, file_name, n = 1, pattern_length = 1, humanisation_intensity = 0, user_input = None):
    solutions = _generate_solutions(constraints, user_input)
    pattern_plot = None
    fill_locations = None
    if solutions is None:
        return None
    for i in range(1, n+1):
        rand_solution, rand_index, fill_locations = _search_solutions(solutions, constraints, fills, pattern_length, 20)
        #Return none if no solution can be found.
        if rand_solution == None:
            return None
        
        #Splitting the random solution into main pattern hits and fill hits. 
        hit_strs = [item for item in rand_solution if 'f' not in item]
        fill_strs = [item for item in rand_solution if 'f' in item]
        hit_list = []
        fill_list = []

        #Converting the random solution into a (hit, quarter-beat) list of type (char, char).
        for hit in hit_strs:
            hit_list.append(hit[hit.find("(")+1:hit.find(")")].split(","))
        for hit in fill_strs:
            fill_list.append(hit[hit.find("(")+1:hit.find(")")].split(","))
        
        #Removing the hits from hit list that conflict with the drum fill hits.
        if fill_locations is not None:
            for j in range(0, len(fill_locations), 2):
                hit_list[:] = [item for item in hit_list if not (int(item[1]) > fill_locations[j] and int(item[1]) <= fill_locations[j+1])]

        #humanisation value to randomly nudge hits around and change velocity.
        #The further away from 0 the hit is nudged, the quieter it is hit.
        humanisation = np.random.normal(0, humanisation_intensity, len(hit_list + fill_list))

        pattern_plot = _print_hits(rand_index, hit_list + fill_list, humanisation, pattern_length)
        print("\n")
        if i == 1:
            _write_midi(hit_list, fill_list, save_path, file_name + ".mid", humanisation)
        else:
            _write_midi(hit_list, fill_list, save_path, file_name + "_" + str(i-1) + ".mid", humanisation)

    #Remove temporary problem files
    for i in range(1, pattern_length+1):
        remove_file('rules\\temp\\' + str(i) + '_bar_problem.lp')

    return pattern_plot
