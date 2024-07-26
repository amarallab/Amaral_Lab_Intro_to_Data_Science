__author__ = "Amaral LAN"
__copyright__ = "Copyright 2022,2023, Amaral LAN"
__credits__ = ["Amaral LAN"]
__version__ = "0.3"
__maintainer__ = "Amaral LAN"
__email__ = "amaral@northwestern.edu"
__status__ = "alpha"

import matplotlib.pyplot as plt
import matplotlib.cm as cm

from collections import Counter
from pathlib import Path
from random import random
from string import punctuation, whitespace


def read_complete_works( folder = Path.cwd() / 'Data' ):
    """
    This function reads the file with Complete Works of William Shakespeare
    and returns a list with lines in the file and a dictionary information about 
    each of the works included.
    
    inputs:
        folder -- pathlib Path for folder where 'Shakespeare.txt' can be found
        
    returns:
        complete_works -- list of str
        plays -- dict with play title as key and a dictionary with keys {year, first_line, last_line} as value 
        
    """
    file_path = folder / 'Shakespeare.txt'
    with open( file_path, 'r', encoding = 'UTF-8' ) as file_in:
        complete_works = file_in.readlines()
    
    elect_pattern = '<<THIS ELECTRONIC VERSION OF THE COMPLETE WORKS OF WILLIAM'
    is_inside_speech = False
    found_play = False

    plays = {}
    for i, line in enumerate(complete_works):
        if not is_inside_speech and line.strip() == elect_pattern:
            is_inside_speech = True     # found speech of character
            continue

        if is_inside_speech and line.strip().isnumeric():
            # Different plays have different number (2, 3, or 6) of empty lines between 
            # year and title.
            # Title of play is always in upper case letters.
            #
            if ( complete_works[i+2].upper() == complete_works[i+2] or
                 complete_works[i+3].upper() == complete_works[i+3] or 
                 complete_works[i+6].upper() == complete_works[i+6] ):
                
                found_play = True
                year_play = int( line.strip() )

                # Get to the title and store year of release and first line of play
                #
                if complete_works[i+2].strip() == '':
                    if complete_works[i+3].strip() == '':
                        title_play = complete_works[i+6].strip()
                        plays[title_play] = {'year': year_play, 'first_line': i+6}
                    else:
                        title_play = complete_works[i+3].strip()
                        plays[title_play] = {'year': year_play, 'first_line': i+3}
                else:    
                    title_play = complete_works[i+2].strip()
                    plays[title_play] = {'year': year_play, 'first_line': i+2}
                continue
            
        if found_play and line.strip() == 'THE END':
            plays[title_play]['last_line'] = i
            found_play = False
            is_inside_speech = False

    return complete_works, plays


def get_characters(the_play):
    """
    This function takes as input a list of lines from
    a play in Shakespeare's Complete Works text file 
    from Project Gutenberg and returns a dictionary with 
    names of the characgters in the play and their
    description.
    
    inputs:
        play_name -- str
        
    returns:
        personae -- dict with character name as key
                    and character description as value
    """
    # Get relevant lines
    #
    start_pattern = 'Dramatis Personae'
    end_pattern = '<<THIS ELECTRONIC VERSION OF THE COMPLETE WORKS OF WILLIAM'

    found_personae = False
    for i, line in enumerate(the_play):
        if start_pattern in line:
            start_line = i + 1
            continue 

        if end_pattern in line:
            end_line = i
            break

    personae_text = the_play[start_line: end_line]
    print( personae_text )
    print()
    
    
    personae = {}  

    for i, line in enumerate(personae_text):
        if line == '\n':
            continue

#         print(f"{i:>3} -- {line.strip()}")

        # Split by comma, take first item if is all caps, 
        # join the rest
        #
        items = line.strip().split(',')

        if items[0].upper() == items[0]:
            name = items[0].strip()
            description = ','.join(items[1:]).strip()
            personae[name] = description

    print( personae )

    return personae


def get_character_lines(character, the_play):
    """
    This function takes the name of a character and the lines from the play
    extracted from GP's Complete Works of William Shakespeare and returns
    a list with all the lines from that character in the play
    
    inputs:
        character -- str
        the_play -- list of str
        
    returns:
        character_lines -- list of str
    """
    character_lines = []
    character = character.upper()
    
    start_string = ' '*2 + character
    continuation_string = ' '*4
    
    found_lines = False
    for i, line in enumerate(the_play):
        if line.split('.')[0] == start_string:
            found_lines = True
            character_lines.append(line.replace(start_string+ '.', '').strip())
            continue

        if found_lines:
            if line[:len(continuation_string)] == continuation_string:
                character_lines.append(line.strip())
            else:
                found_lines = False
                continue 
    
    return character_lines


def extract_words_from_lines(character, character_lines, punct = punctuation):
    """
    This function takes the name of a character and a list 
    with all the lines from a character in the play and returns 
    a list of words
    
    inputs:
        character -- str
        character_lines -- list of str
        punct -- str with punctuation characters to be stripped
        
    returns:
        character_words -- list of str
    """
    character_words = []
    character = character.upper()
    character_string = character + '.'
    
    for i, line in enumerate(character_lines):
        if character_string in line:
            line = line.replace(character_string, ' ')

        line_words = line.strip().split()

        for word in line_words:
            character_words.append(word.rstrip(punct).lower())

    print(f"{character.capitalize()}'s lines comprise {len(character_words)} words.\n")
    print(f"{character.capitalize()}'s lines comprise {len(set(character_words))} unique words.\n")
    
    return character_words


def plot_survival_function_word_frequency(corpus_name, counter, ax):
    """
    This function takes a courpus name, a collection.Counter object
    and a matplotlib ax object and calculates the survival function
    from the counter data and modifies the ax object.
    
    inputs:
        corpus_name -- str
        counter -- collection.Counter object
        ax -- matplotlib ax object
    """
    # calculate survival function
    #
    counts = list( dict(counter).values() )
    k_values = []
    survival_function = []

    n = len(counts)
    for k in sorted(counts):
        if k not in k_values:
            k_values.append(k)
            survival_function.append(n)
            n -= 1
        else:
            n -= 1

    # plot data
    #
    ax.loglog()
    ax.plot( k_values, survival_function, 'r-', lw = 2, label = 'Othello' )
    ax.legend(loc = 'best', frameon = False, fontsize = my_fontsize)

    plt.tight_layout()  
    
    return


