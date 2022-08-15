__author__ = "Amaral LAN"
__copyright__ = "Copyright 2022, Amaral LAN"
__credits__ = ["Amaral LAN"]
__version__ = "0.1"
__maintainer__ = "Amaral LAN"
__email__ = "amaral@northwestern.edu"
__status__ = "beta"

import matplotlib.pyplot as plt
import matplotlib.cm as cm

from collections import Counter
from pathlib import Path
from random import random
from string import punctuation, whitespace


def read_text_file(file_path, encoding = 'UTF-8'):
    """
    This function takes a path to a text file with a specific
    encoding and returns a list of lines in the file.
    
    inputs:
        file_path -- str or PosixPath object
        encoding -- str
        
    returns:
        all_the_lines -- list of str
    """
    with open(file_path, 'r', encoding= encoding) as file_in:
        all_the_lines = file_in.readlines()
        
    return all_the_lines


def extract_play(play_name, complete_works):
    """
    This function takes as input the name of a play in 
    Shakespeare's Complete Works text file from Project
    Gutenberg and returns the lines for that play
    
    inputs:
        play_name -- str
        complete_works -- list of str
        
    returns:
        the_play -- list of str
    """
    # find line_start and line_end
    #
    found_start = False
    for i, line in enumerate(complete_works):
        if line.strip() == play_name:
            print(f"{i:>4} -- {line.strip()}")
            line_start = i
            found_start = True
            continue
        
        if found_start and line.strip() == 'THE END':
            print(f"{i:>4} -- {line.strip()}")
            line_end = i
            break
        
    the_play = complete_works[line_start:line_end]

    print(f"\nThe play {play_name} has {len(the_play)} lines.\n")
    
    return the_play


def get_characters(the_play, boundary_line = 25):
    """
    This function takes as input a list of lines from
    a play in Shakespeare's Complete Works text file 
    from Project Gutenberg and returns a dictionary with 
    names of the characgters in the play and their
    description.
    
    inputs:
        play_name -- str
        boundary_line -- int defining the range of lines
        
    returns:
        personae -- dict with character names as keys
                    and descriptions as value
    """
    found_personae = False
    personae = {}
    for i, line in enumerate(the_play):
        if line.strip() == 'Dramatis Personae':
            print(f"{i:>4} -- {line.strip()}")
            line_start = i
            found_personae = True
            continue
    
        if found_personae and i < boundary_line:
            words = line.strip().split(',')

            # key is first item
            key = words[0].strip()

            # empty or not in upper letters is not character
            if not key or key.upper() != key:
                print(f"{i:>4} --{key}-- Not a character.")
                continue
        
            # value is the joint with commas of following items
            value = ','.join(words[1:])        
            print(f"{i:>4} -- {key:>20} -- {value}")
            personae[key] = value

    return personae


def get_character_lines( character, the_play ):
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
    start_string = '  ' + character
    continuation_string = '    '
    
    found_lines = False
    for i, line in enumerate(the_play):
        if line.split('.')[0] == start_string:
#             print(f"{i:>4}--{line.rstrip()}")
            found_lines = True
            character_lines.append(line)
            continue

        if found_lines:
            if line[:4] == continuation_string:
#                 print(f"{i:>4}--{line.rstrip()}")
                character_lines.append(line)
            else:
                found_lines = False
                continue    
    
    return character_lines


def extract_words_from_lines( character, character_lines ):
    """
    This function takes the name of a character and a list 
    with all the lines from a character in the play and returns 
    a list of words
    
    inputs:
        character -- str
        character_lines -- list of str
        
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
#         print(f"{i:>4} -- {line_words}")

        for word in line_words:
#             print(f"\t{word.rstrip(punctuation)}")
            character_words.append(word.rstrip(punctuation).lower())

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


def text_entropy( counter ):
    """
    This function takes a Counter object and returns the entropy of the 
    underlying text.
    
    inputs:
        counter -- Counter object
        
    returns:
        entropy -- float
    """
    entropy = 0
    
    counts = list( dict(counter).values() )
    N = sum(counts)
    
    for n_i in counts:
        p_i = n_i / N
        entropy -= p_i * np.log2(p_i)

    print(f"The entropy of this corpus is {entropy:.2f}\n" )
    
    return entropy
