import subprocess
from os.path import join as pjoin
import json
from midiutil import MIDIFile
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#Configure Clingo parameters

clingo_path = 'C:\\Users\\lenovo\\Documents\\MSc Computer Science\\ASP\\clingo.exe'
clingo_options = ['--outf=2','-n 0', '--time-limit=10']
clingo_command = [clingo_path] + clingo_options

#Define rule paths

all_rules = [['rules\\kick_placement.lp', 'rules\\kick_con_1.lp', 'rules\\kick_con_2.lp'], \
             ['rules\\snare_placement_exp.lp', 'rules\\snare_placement_conv.lp'], \
             ['rules\\kick_snare_con_1.lp'], \
             ['rules\\hat_placement_exp.lp', 'rules\\hat_placement_conv.lp' , 'rules\\hat_con_1.lp', 'rules\\hat_con_2.lp'], \
             ['rules\\perc_placement.lp', 'rules\\perc_con_1.lp', 'rules\\perc_con_2.lp'], \
             ['rules\\gsnare_placement.lp', 'rules\\gsnare_con_1.lp', 'rules\\gsnare_con_2.lp']]

#Solve the ruleset.
def solve(program):
    input = program.encode()
    process = subprocess.Popen(clingo_command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output, error = process.communicate(input)
    result = json.loads(output.decode())
    if result['Result'] == 'SATISFIABLE':
        return [value['Value'] for value in result['Call'][0]['Witnesses']]
    else:
        return None

#Write the one bar problem rule set.
def write_problem(constraints):
    rules = ['rules\\time.lp']
    i = 0
    for row in all_rules:
        for j in range(0, len(row)):
            if constraints[i][j]:
                rules.append(all_rules[i][j])
        i += 1
    with open('rules\\problem.lp', 'w') as outfile:
        for fname in rules:
            with open(fname) as infile:
                outfile.write(infile.read())    

#Solve the one bar problem in Clingo, specifying what kind of pattern will be generated.
#Print the number of solutions.
def generate_solutions(constraints, user_input):
    write_problem(constraints)
    if user_input:     
        with open('rules\\problem.lp', 'a') as outfile:
            outfile.write('\n'.join(user_input) + '\n')
    problem = open('rules\\problem.lp', 'r').read()
    solutions = solve(problem)
    #Print the number of patterns found.
    if solutions is not None:
        print(str(len(solutions)) + " 1 bar patterns have been found.\n")
    else:
        print("No patterns have been found.\n")

    return solutions


#Represent hit_list as a table.
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import FixedLocator

def print_hits(pattern_index, hit_list, humanisation, pattern_length = 1): 

    X = np.zeros((5, 16 * pattern_length))

    #iterator
    j = 0

    for i in hit_list:
        if i[0] == 'k':
            X[4][int(i[1])-1] = 1./(volume-abs(humanisation[j])*300)
        if i[0] == 's':
            X[3][int(i[1])-1] = 1./(volume-abs(humanisation[j])*300)
        if i[0] == 'g':
            X[2][int(i[1])-1] = 1./(40-abs(humanisation[j])*300)
        if i[0] == 'h':
            X[1][int(i[1])-1] = 1./(volume-abs(humanisation[j])*300)
        if i[0] == 'p':
            X[0][int(i[1])-1] = 1./(volume-abs(humanisation[j])*300)
        j += 1

    normalValue = np.amax(X) + 0.005
    X[X == 0] = normalValue

    #plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(X, cmap=plt.get_cmap('gist_gray'))

    y_labels = ['Percussion', 'Hat', 'Ghost Snare', 'Snare', 'Kick']
    ax.set_xticks(list(range(0, 16 * pattern_length)))
    ax.set_yticks(list(range(0, 5)))
    ax.set_yticklabels(y_labels)
    ax.set_xticklabels(list(range(1, 16 * pattern_length + 1)))
    
    minor_xlocator = AutoMinorLocator(2)
    minor_ylocator = FixedLocator([x + 0.5 for x in range(0, 16 * pattern_length)])
    ax.xaxis.set_minor_locator(minor_xlocator)
    ax.yaxis.set_minor_locator(minor_ylocator)
    ax.grid(which='minor', color='0.4', linestyle='dashed')
    
    fig.patch.set_facecolor("None")
    #ax.set_title("Pattern " + str(pattern_index), fontsize=18)

    #plt.show()

    canvas = FigureCanvas(fig)

    canvas.setStyleSheet("background-color:transparent;")

    canvas.draw()

    return canvas


#Create MIDI representation of the drum pattern.

#offset needed to convert to MIDI time.
offset = 0.25
track    = 0
channel  = 0
duration = 0.125 # In beats
tempo    = 174  # In BPM
volume   = 100  # 0-127, as per the MIDI standard

#Write a MIDI file for a set of hits with a given file name.
def write_midi(hit_list, savePath, file_name, humanisation):
    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                          # automatically)
    MyMIDI.addTempo(track, 0, tempo)

    #iterator
    j = 0
    #Add kicks to middle C, snares to C#3 and hats to D3.
    for i in hit_list:
        if i[0] == 'k':
            if i[1] == '1':
                MyMIDI.addNote(track, channel, 60, float(i[1])/4-offset, duration, int(volume-abs(humanisation[j])*300))
            else:
                MyMIDI.addNote(track, channel, 60, float(i[1])/4-offset+humanisation[j], duration, int(volume-abs(humanisation[j])*300))
        if i[0] == 's':
            if i[1] == '1':
                MyMIDI.addNote(track, channel, 61, float(i[1])/4-offset, duration, int(volume-abs(humanisation[j])*300))
            else:
                MyMIDI.addNote(track, channel, 61, float(i[1])/4-offset+humanisation[j], duration, int(volume-abs(humanisation[j])*300))
        if i[0] == 'g':
            if i[1] == '1':
                MyMIDI.addNote(track, channel, 61, float(i[1])/4-offset, duration, int(40-abs(humanisation[j])*300))
            else:
                MyMIDI.addNote(track, channel, 61, float(i[1])/4-offset+humanisation[j], duration, int(40-abs(humanisation[j])*300))
        if i[0] == 'h':
            if i[1] == '1':
                MyMIDI.addNote(track, channel, 62, float(i[1])/4-offset, duration, int(volume-abs(humanisation[j])*300))
            else:
                MyMIDI.addNote(track, channel, 62, float(i[1])/4-offset+humanisation[j], duration, int(volume-abs(humanisation[j])*300))
        if i[0] == 'p':
            if i[1] == '1':
                MyMIDI.addNote(track, channel, 63, float(i[1])/4-offset, duration, int(volume-abs(humanisation[j])*300))
            else:
                MyMIDI.addNote(track, channel, 63, float(i[1])/4-offset+humanisation[j], duration, int(volume-abs(humanisation[j])*300))
        j += 1
            
    filePath = pjoin(savePath, file_name)
    with open(filePath, "wb") as output_file:
        MyMIDI.writeFile(output_file)

#Extend the one bar pattern to a given length with given contraints.
def extend_pattern(pattern, extended_length, constraints):
    final_solution = pattern

    #extendedConstraints removes the placement rule sets as they are not needed.
    extendedConstraints = constraints[:]

    extendedConstraints[0][0] = False
    extendedConstraints[1][:] = False, False
    extendedConstraints[3][0:1] = False, False
    extendedConstraints[4][0] = False
    extendedConstraints[5][0] = False

    n_bar_rules = ['rules\\time.lp', 'rules\\extend_to_n_bars.lp']
    i = 0
    for row in all_rules:
        for j in range(0, len(row)):
            if extendedConstraints[i][j]:
                n_bar_rules.append(all_rules[i][j])
        i += 1

    with open('rules\\problem_n_bar.lp', 'w') as outfile:
        for fname in n_bar_rules:
            with open(fname) as infile:
                outfile.write(infile.read())

    timeConstraints = []
    limit = extended_length * 16

    timeConstraints.append(":- chooseHit(k, T), T > " + str(limit) + ". ")
    timeConstraints.append(":- chooseHit(s, T), T > " + str(limit) + ". ")
    timeConstraints.append(":- chooseHit(h, T), T > " + str(limit) + ". ")
    timeConstraints.append(":- chooseHit(p, T), T > " + str(limit) + ". ")
    timeConstraints.append(":- chooseHit(g, T), T > " + str(limit) + ". ")

    with open('rules\\problem_n_bar.lp', 'a') as outfile:
        outfile.write('\n'.join(timeConstraints) + '\n')

    for j in range(2, extended_length + 1):
        
        extendedTime = []
        n = (j-2) * 16
        minTime = 1 + n
        maxTime = 16 + n
        min1Q = 1 + n
        max1Q = 3 + n
        min2Q = 5 + n
        max2Q = 7 + n
        min3Q = 9 + n
        max3Q = 11 + n
        min4Q = 13 + n
        max4Q = 15 + n
        extendedTime.append("time(" + str(minTime) + ".." + str(maxTime) + "). ")
        extendedTime.append("odd1Q(" + str(min1Q) + ";" + str(max1Q) + "). ")
        extendedTime.append("odd2Q(" + str(min2Q) + ";" + str(max2Q) + "). ")
        extendedTime.append("odd3Q(" + str(min3Q) + ";" + str(max3Q) + "). ")
        extendedTime.append("odd4Q(" + str(min4Q) + ";" + str(max4Q) + "). ")
        extendedTime.append("oddSH(" + str(max3Q) + ";" + str(min4Q) + ";" + str(max4Q) + "). ")

        with open('rules\\problem_n_bar.lp', 'a') as outfile:
            outfile.write('\n'.join(extendedTime) + '\n')    
        
        with open('rules\\problem_n_bar.lp', 'a') as outfile:
            outfile.write('\n'.join([hit + '.' for hit in final_solution]) + '\n')

        """
        timeConstraints = []
        limit = i * 16

        timeConstraints.append(":- chooseHit(k, T), T > " + str(limit) + ". ")
        timeConstraints.append(":- chooseHit(s, T), T > " + str(limit) + ". ")
        timeConstraints.append(":- chooseHit(h, T), T > " + str(limit) + ". ")
        timeConstraints.append(":- chooseHit(p, T), T > " + str(limit) + ". ")
        timeConstraints.append(":- chooseHit(g, T), T > " + str(limit) + ". ")

        with open('rules\\problem_n_bar.lp', 'a') as outfile:
            outfile.write('\n'.join(timeConstraints) + '\n')

        """

        problem = open('rules\\problem_n_bar.lp', 'r').read()
        solutions = solve(problem)

        """
        editProblem = open('rules\\problem_n_bar.lp', 'r')
        lines = editProblem.readlines()
        lines = lines[:-5]

        editProblem = open('rules\\problem_n_bar.lp', 'w')
        editProblem.writelines(lines)
        editProblem.close()
        """

        #Return if no valid solutions are found to allow another attempt.
        if solutions == None:
            return None
        print(str(len(solutions)) + " " + str(j) + " bar patterns have been found based on the randomly selected one bar pattern.\n")
        rand_index = randint(0, len(solutions)-1)
        final_solution = solutions[rand_index][:]   
    return final_solution

#Generate n random patterns from the answer set, depending on the rules chosen and any user input.
#A level of humanisation is chosen between 0 and 0.05. 
#Print and store solutions as MIDI files in the save path with a defined file name. Defaults to 1 pattern of length 1 bar with no user input.
from random import randint

def generate_patterns(constraints, savePath, fileName, n = 1, pattern_length = 1, humanisation_intensity = 0, user_input = None):
    solutions = generate_solutions(constraints, user_input)
    patternPlot = None
    if solutions is None:
        return 
    for i in range(1, n+1):
        rand_solution = None
        #Iterate over the 1 bar patterns until a valid 2+ bar pattern is found (within 20 attempts).
        #This only applies when attempting to generate a 2+ bar pattern.
        j = 0
        while(rand_solution == None and j < 20):
            rand_index = randint(0, len(solutions)-1)
            rand_solution = solutions[rand_index][:]
            #Allow for extension of the base pattern if pattern_length is not 1.
            if pattern_length != 1:
                rand_solution = extend_pattern(rand_solution, pattern_length, constraints)
            j += 1
        #Return none if no solution can be found.
        if rand_solution == None:
            return patternPlot
        #Converting the random solution into a (hit, quarter-beat) list of type (char, char).
        hit_list = []
        for hit in rand_solution:
            hit_list.append(hit[hit.find("(")+1:hit.find(")")].split(","))

        #humanisation value to randomly nudge hits around and change velocity.
        #The further away from 0 the hit is nudged, the quieter it is hit.
        humanisation = np.random.normal(0, humanisation_intensity, len(hit_list))

        patternPlot = print_hits(rand_index, hit_list, humanisation, pattern_length)
        print("\n")
        if i == 1:
            write_midi(hit_list, savePath, fileName + ".mid", humanisation)
        else:
            write_midi(hit_list, savePath, fileName + "_" + str(i-1) + ".mid", humanisation)

    return patternPlot
