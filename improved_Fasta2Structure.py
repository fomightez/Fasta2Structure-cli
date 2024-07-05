# improved `Fasta2Structure.py` to allow running on command line without tkinter
####-----
'''
It checks if the script is running in a terminal using sys.stdin.isatty().
It tries to import Tkinter and create a root window to check if Tkinter is installed and no paths provided on command line.
If the script is running in a terminal and Tkinter is installed and no path is provided, it runs the existing Tkinter GUI code.
If the script is not running in a terminal or Tkinter is not installed, it assumes it's being run from the command line and expects one or more FASTA file paths as command-line arguments.
If no command-line arguments are provided, it prints an error message and exits.
Otherwise, it runs the existing non-GUI code to process the provided FASTA files.
'''
####-----

##########################################################################################
###------------ Top of improved mainly comes from start and functions defined in unimproved
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from Bio import AlignIO
import os
import threading
import traceback
import logging

logging.basicConfig(filename='log.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def convert_to_binary(sequence):
    binary_mapping = {'A': '0 ', 'T': '1 ', 'C': '2 ', 'G': '3 ', '-': '-9 ', '?': '-9 '}
    return ' '.join([binary_mapping.get(base, '-9') for base in sequence])


def get_variable_sites(alignment):
    variable_sites = []
    for i in range(alignment.get_alignment_length()):
        column = alignment[:, i]
        if len(set(column)) > 1:
            variable_sites.append(i)
    return variable_sites


def process_fasta_file(filepath, sequence_dict, file_index, progress_callback):
    try:
        alignment = AlignIO.read(filepath, "fasta")
        variable_sites = get_variable_sites(alignment)

        logging.info(f'Variable sites for {filepath}: {variable_sites}')

        for record in alignment:
            variable_site_sequence = ''.join([record.seq[i] for i in variable_sites])
            binary_sequence = convert_to_binary(variable_site_sequence)
            if record.id in sequence_dict:
                sequence_dict[record.id][file_index] = binary_sequence
            else:
                sequence_dict[record.id] = {file_index: binary_sequence}

        variable_sites_count = len(variable_sites)
        progress_callback(variable_sites_count)
        return variable_sites_count
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        traceback.print_exc()
        progress_callback(0)
        return 0


def pad_missing_sequences(sequence_dict, variable_sites_per_file):
    for seq_id, sequences in sequence_dict.items():
        padded_sequences = []
        for i in range(len(variable_sites_per_file)):
            if i in sequences:
                padded_sequences.append(sequences[i])
            else:
                pad_string = " ".join(["-9"] * variable_sites_per_file[i]) + " "
                padded_sequences.append(pad_string)
        sequence_dict[seq_id] = ' '.join(padded_sequences)


def concatenate_results(sequence_dict):
    concatenated_results = []
    for seq_id, binary_sequence in sequence_dict.items():
        concatenated_results.append(f"{seq_id} {binary_sequence}\n")
    return ''.join(concatenated_results)


def browse_files():
    filepaths = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                            title="Select FASTA file",
                                            filetypes=(("FASTA file", "*.fas"), ("All files", "*.*")))

    if not filepaths:
        return

    sequence_dict = {}
    variable_sites_per_file = []
    progress_value = tk.DoubleVar()
    progress_bar = tk.ttk.Progressbar(root, variable=progress_value, maximum=len(filepaths), mode='determinate')
    progress_bar.pack(pady=10, fill='x')
    progress_label = tk.Label(root, text="")
    progress_label.pack(pady=5)

    logging.info(f'{len(filepaths)} FASTA files selected.')

    def process_files():
        try:
            for i, filepath in enumerate(filepaths):
                variable_sites_count = process_fasta_file(filepath, sequence_dict, i,
                                                          lambda value: progress_value.set(i + 1) or progress_label.configure(
                                                              text=f"Processing file {i + 1}/{len(filepaths)} ({value} variable sites)"))
                variable_sites_per_file.append(variable_sites_count)

            pad_missing_sequences(sequence_dict, variable_sites_per_file)
            concatenated_results = concatenate_results(sequence_dict)

            preview_textbox.configure(state='normal')
            preview_textbox.delete('1.0', tk.END)
            preview_textbox.insert(tk.END, concatenated_results)
            preview_textbox.configure(state='disabled')

            output_filename = "Structure.str"

            with open(output_filename, "w") as output_file:
                output_file.write(concatenated_results)

            output_label.configure(text=f"Converted files saved as: {output_filename}")
            progress_label.configure(text="Conversion completed successfully!")
        except Exception as e:
            logging.error(f'An error occurred: {e}')
            traceback.print_exc()
            progress_label.configure(text="An error occurred during the conversion process.")

    threading.Thread(target=process_files).start()
###------------ END OF original top, mainly from unimproved code--------------###
################################################################################

###-------------------HELPER FUNCTIONS by Wayne for non-GUI use---------------###
def generate_output_file_name(file_name):
    '''
    Takes a file name as an argument and returns string for the name of the
    output file. The generated name is based on the original file
    name.

    Specific example
    ================
    Calling function with
        ("ITS.fas")
    returns
        "ITS_Structure.str
    '''
    main_part_of_name, file_extension = os.path.splitext(
        file_name) #from http://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    if '.' in file_name:  #I don't know if this is needed with the os.path.splitext method but I had it before so left it
        return main_part_of_name + "_Structure" + ".str"
    else:
        return file_name + ".str"

def make_temp_filename(filepaths):
    '''
    Takes a list of filepaths and makes a file name that nothing should match 
    based on that and uuid use.
    '''
    import uuid
    return "tmp{}{}.fa".format(
        os.path.splitext(os.path.basename(filepaths[0]))[0],uuid.uuid4().time)

def parse_inputs(inputs):
    fasta_files_in_directory = []
    for input_item in inputs:
        if os.path.isdir(input_item):
            # If it's a directory, add all .fa and .fasta files in it
            fasta_files.extend([os.path.join(input_item, f) for f in os.listdir(input_item) 
                                if f.endswith(('.fa', '.fasta', '.fas'))])
        elif os.path.isfile(input_item) and input_item.endswith(('.fa', '.fasta', '.fas')):
            # If it's a file with the correct extension, add it
            fasta_files.append(input_item)
        else:
            print(f"Warning: '{input_item}' is not a valid FASTA file or directory. Skipping.")
    
    return fasta_files

def process_multiple_fastas_together(filepaths):
    sequence_dict = {}
    variable_sites_per_file = []

    for i, filepath in enumerate(filepaths):
        file_sequence_dict = {}
        variable_sites_count = process_fasta_file(filepath, file_sequence_dict, i, lambda x: None)
        variable_sites_per_file.append(variable_sites_count)

        # Merge file_sequence_dict into the main sequence_dict
        for seq_id, sequences in file_sequence_dict.items():
            if seq_id not in sequence_dict:
                sequence_dict[seq_id] = {}
            sequence_dict[seq_id].update(sequences)

    pad_missing_sequences(sequence_dict, variable_sites_per_file)
    concatenated_results = concatenate_results(sequence_dict)

    output_filename = "Structure.str"
    with open(output_filename, "w") as output_file:
        output_file.write(concatenated_results)
    print(f"Converted files saved as: {output_filename}")


def process_single_fasta(filepath):
    sequence_dict = {}
    variable_sites_count = process_fasta_file(filepath, sequence_dict, 0, lambda x: None)
    
    pad_missing_sequences(sequence_dict, [variable_sites_count])
    concatenated_results = concatenate_results(sequence_dict)

    output_filename = f"{os.path.splitext(os.path.basename(filepath))[0]}_Structure.str"
    with open(output_filename, "w") as output_file:
        output_file.write(concatenated_results)
    print(f"Converted file saved as: {output_filename}")

###---------END OF HELPER FUNCTIONS by Wayne for non-GUI use-----------------###
###---------END OF HELPER FUNCTIONS by Wayne for non-GUI use-----------------###


# Decide to use GUI interface or stick to stdin, stderr, stdout as interface. Give feedback if not providing arguments
# Check if the script is running in a terminal or situation like inside Jupyter, i.e., if Tkinter cannot connect to a graphical display. 
# FULL DESCRIPTION OF SITUATION: Tkinter is installed and importable because it is part of the standard library, but if the original Fasta2Structure.py script (https://github.com/AdamBessa/Fasta2Structure/blob/9721bb545a8277c3ddbca74bc987e89563475bce/Fasta2Structure.py) is run on the command line with `python Fasta2Structure.py` or in Jupyter with `%run Fasta2Structure.py`,it gives `_tkinter.TclError: no display name and no $DISPLAY environment variable` because it cannot initialize a graphical window due to the absence of a display server connection." In this situatuon I then want to run using arguments to specify the file or directory to act on. If there is no arguments, then display USAGE/help via argparse.
try:
    root = tk.Tk()
    Tkinter_can_connect_to_graphical_display= True
    root.withdraw()  # Destroy the test Tk window
except (tk.TclError): # handle the error `_tkinter.TclError: no display name and no $DISPLAY environment variable` when running in command line where Tkinter GUI cannot start up properly
    Tkinter_can_connect_to_graphical_display = False


# Set up for Usgae/help and handling input arguments
import argparse
import textwrap

description = textwrap.dedent("""\
    improved_Fasta2Structure.py converts Multiple Aligned FASTA Files to STRUCTURE Format.
    It can be used in two ways:
    1. GUI mode: When run without arguments in a desktop environment, it launches a GUI.
    2. Command-line mode: Used with arguments to process FASTA files directly.

    Command-line mode means it can run where used on a remote server without a grahical 
    display serving Jupyter (headless) or integrated into workflow managment tools like
    Snakemake & NextFlow.

    Command-line usage examples:
    - Single multi-sequence FASTA file: python improved_Fasta2Structure.py my_fasta.fa
    - Multiple FASTA files: python improved_Fasta2Structure.py file1.fa file2.fa file3.fa (I THINK ORDER MATTERS BUT NOT 100% SURE YET BECAUSE A PAIN TO TEST IN GUI.)
    - Directory with FASTA files: python improved_Fasta2Structure.py path/to/fasta/directory

    Jupyter usage examples for situations where graphical display not connected or opting for text-based only:
    - Single multi-sequence FASTA file: %run improved_Fasta2Structure.py my_fasta.fa
    - Multiple FASTA files: %run improved_Fasta2Structure.py file1.fa file2.fa file3.fa
    - Directory with FASTA files: %run improved_Fasta2Structure.py path/to/fasta/directory

    Specific CLI usage for INCLUDED examples (swap `python` for `%run` for Jupyter):
    - Single multi-sequence FASTA file: python improved_Fasta2Structure.py Example_data/Datasets/ITS.fas
    - Multiple FASTA files: python improved_Fasta2Structure.py Example_data/Datasets/ITS.fas Example_data/Datasets/trnD-trnT.fas Example_data/Datasets/trnH-trnK.fas 
    - Directory with FASTA files: python improved_Fasta2Structure.py Example_data/Datasets/



    **** GUI & main script by Adam Bessa-Silva; CLI adaptation by Wayne Decatur (fomightez @ github) ***
    """)

parser = argparse.ArgumentParser(
    prog='improved_Fasta2Structure.py',
    description=description,
    formatter_class=argparse.RawDescriptionHelpFormatter
)
fasta_extensions_allowed = ('.fa', '.fasta', '.fas')
fasta_extensions_allowed_text_for_help = "'" + "', '".join(fasta_extensions_allowed[:-1]) + "', or '" + fasta_extensions_allowed[-1] + "'"
parser.add_argument("input", nargs='+', help=f"FASTA file or files or directory \
    containing FASTA files. FASTA files in a directory (with extensions {fasta_extensions_allowed_text_for_help}) will be treated as if all of the filepaths for each had been provided when invoking the script. Multiple FASTA files provided in arguments will be processed in the same manner as if all selected at the same time by the GUI interface of the original `Fasta2Structure.py` NOTE, I THINK ORDER MATTERS BUT NOT 100% SURE YET BECAUSE A PAIN TO TEST IN GUI.", metavar="INPUT_FASTA")

# Parse the arguments
args = parser.parse_args()

'''
argeparse automatically handles if user calls the script with `-h` or `--help` flag and prints the USAGE.

Other triggers for USAGE to display:
- Tkinter cannot connect to a graphical display and no arguments are provided

The GUI will run if a graphical display can be connected to by Tkinter and the script is called with no arguments.
'''

# If the script is running in a terminal/on command line or in Jupyter run headlessly and so Tkinter cannot connect to a graphical display and no arguments are provided into the call to the script, then print general USAGE info
if (not Tkinter_can_connect_to_graphical_display) and not args.input:
    parser.print_help()
    sys.exit(1)




# If the script is called and no arguments are provided and TKINTER CAN CONNECT TO A GRAPHICAL DISPLAY, run the GUI
if Tkinter_can_connect_to_graphical_display and len(sys.argv) == 1:
    # The original Tkinter code from https://github.com/AdamBessa/Fasta2Structure/blob/9721bb545a8277c3ddbca74bc987e89563475bce/Fasta2Structure.py here
    root = tk.Tk()
    root.title("Fasta to Structure")

    browse_button = tk.Button(root, text="Select FASTA files", command=browse_files)
    browse_button.pack(pady=20)

    preview_label = tk.Label(root, text="Preview:")
    preview_label.pack()

    preview_textbox = ScrolledText(root, height=10)
    preview_textbox.pack(pady=10)

    output_label = tk.Label(root, text="")
    output_label.pack(pady=10)

    root.mainloop()
# Since arguments were provided when the script, which we know because at this point we've already dealt with all the possibilities when no arguments provided, that is the file or directory the user wants to act on, and so we should continue on acting on that sticking to using stdin, stderr, and stdout for interaction. We don't need to concern ourselves with if Tkinter can connect to a graphical display because we should now have all the information that the windowed interface facilitates determining in the GUI situation.
else:
    # The section handling the conversion without using Tkinter GUI, i.e. CLI mode section.
    # if more than one input file is provided, treat them as related, the way the
    # original file iterated on them with `for i, filepath in enumerate(filepaths):`
    # accumulating variable sites from each file.
    # Otherwise check if provided argument is a directory and then process each FASTA in as if separate, or just process the one FASTA file as multi-sequence.
    filepaths = sys.argv[1:]
    if not filepaths:
        print("No FASTA files provided. Please provide one or more FASTA file paths as command-line arguments or a path to a directory holding FASTA files to convert.")
        sys.exit(1)
    if len(args.input) > 1:
        # Multiple input files, process them as the GUI does if specify three unrelated alignments 
        logging.info(f'{len(args.input)} FASTA files selected.')
        process_multiple_fastas_together(args.input)
    elif os.path.isdir(args.input[0]):
        # Input is a directory, process all FASTAs together like if each found 
        # provided filepath
        fasta_files = [os.path.join(args.input[0], f) for f in os.listdir(args.input[0]) 
                       if f.endswith(fasta_extensions_allowed)]
        logging.info(f'{len(fasta_files)} FASTA files selected.')
        process_multiple_fastas_together(fasta_files)
    else:
        # Single input file, process it as a multi-sequence FASTA
        logging.info(f'{len(args.input[0])} FASTA files selected.')
        process_single_fasta(args.input[0])

