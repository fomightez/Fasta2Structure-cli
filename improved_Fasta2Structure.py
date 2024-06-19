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
###------------ END OF original top mainly form unimproved code--------------###
################################################################################


# Check if the script is running in a terminal
is_terminal = sys.stdin.isatty()

# Check if Tkinter is installed
try:
    root = tkinter.Tk()
    tkinter_installed = True
    root.withdraw()  # Hide the Tk window
except (tkinter.TclError, ModuleNotFoundError):
    tkinter_installed = False

# If the script is running in a terminal and Tkinter is installed and no arguments provided, run the GUI
if is_terminal and tkinter_installed and len(sys.argv) == 1:
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
else:
    # The section handling the converstion without using Tkinter
    filepaths = sys.argv[1:]
    if not filepaths:
        print("No FASTA files provided. Please provide one or more FASTA file paths as command-line arguments or a path to a directory holding FASTA files to convert.")
        sys.exit(1)

    sequence_dict = {}
    variable_sites_per_file = []

    for i, filepath in enumerate(filepaths):
        variable_sites_count = process_fasta_file(filepath, sequence_dict, i, lambda value: print(f"Processing file {i + 1}/{len(filepaths)} ({value} variable sites)"))
        variable_sites_per_file.append(variable_sites_count)

    pad_missing_sequences(sequence_dict, variable_sites_per_file)
    concatenated_results = concatenate_results(sequence_dict)

    output_filename = "Structure.str"
    with open(output_filename, "w") as output_file:
        output_file.write(concatenated_results)

    print(f"Converted files saved as: {output_filename}")