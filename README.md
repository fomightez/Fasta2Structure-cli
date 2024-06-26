[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/Fasta2Structure-cli/main?urlpath=%2Flab%2Ftree%2Findex.ipynb)

---------------
Attribution
----------
This fork of [the official Fasta2Structure repository](https://github.com/AdamBessa/Fasta2Structure) was set up to take advantage of the MyBinder system to offer a resource to run Fasta2Structure without the user needing to download, install, or maintain any software. Plus, no need to be running it in a typical desktop situation and so the Fasta2Structure script is more convenient to use pretty much anywhere. See [here](https://mybinder.readthedocs.io/en/latest/) for documentation about Binder as deployed at [MyBinder.org](https://mybinder.org/).  
Please see [the official Fasta2Structure repository](https://github.com/AdamBessa/Fasta2Structure) for more information about Fasta2Structure.  
**Remember, if you are using Fasta2Structure, please cite**:  
[Fasta2Structure: a user-friendly tool for converting multiple aligned FASTA files to STRUCTURE format. Bessa-Silva A. BMC Bioinformatics. 2024 Feb 15;25(1):73. doi: 10.1186/s12859-024-05697-7. PMID: 38365590](https://pubmed.ncbi.nlm.nih.gov/38365590/)


# Fasta2Structure-cli
Fasta2Structure: A User-Friendly Tool for Converting Multiple Aligned FASTA Files to STRUCTURE Format, that is even more user-friendly because it doesn't need Tkinter and can this run well anywhere, such as on a computer cluster or in modern Jupyter.  
Plus, combined with Jupyter served by the MyBinder service it will make it easier for anyone to try the software or use it without installing anything on their own computer.  

To make it more convenient to use, I've modified the Fasta2Structure script to allow more ways to run it to produce Fasta2Structure-cli.  
You can still try the original Tkinter-based software presently available at https://github.com/AdamBessa/Fasta2Structure without installing anything on your computer. You can go [here](https://gist.github.com/fomightez/e65761a066f56cbbc4c9b5b882c87380) and find a step-by-step to use a remote virtual desktop to test the Fasta2Structure script. Only you'll find it isn't as convenient as what is provided here.

I **WILL DO(delete this note when done)** have added tests to make sure the Fasta2Structure-cli gives the same result as the Tkinter-based software presently available at https://github.com/AdamBessa/Fasta2Structure.

The STRUCTURE software has gained popularity as a tool for population structure and genetic analysis. However, tailoring data to meet STRUCTURE's specific requirements can be challenging and prone to errors, particularly when managing multilocus data. Here, I introduce a graphical user interface (GUI) application designed to simplify the process of converting multiple sequence alignments into a single, cohesive file that is compatible with the STRUCTURE software. The application has been developed using Tkinter for the GUI and Biopython for handling FASTA files. It processes the files, identifies variable sites, and converts the sequences into a binary format. Subsequently, the sequences are concatenated and displayed within the graphical interface's text area, enabling users to review and verify the results. Furthermore, the program saves the concatenated results in a file, thereby providing a ready-to-use input for the STRUCTURE software. This application presents an efficient and reliable solution for transforming multiple aligned FASTA files into a concatenated binary format file, which is compatible with the STRUCTURE software. With its user-friendly graphical interface and error-reduction strategy, this tool proves to be invaluable for researchers engaged in population structure and genetic analysis. This program is designed to convert FASTA files into a binary representation that is then used to identify variable sites. This binary representation is then saved in a structure (.str) file. Variable sites are defined as positions in the sequence where the nucleotides differ among the sequences in the alignment. These sites are identified and flagged, and the resulting data is saved in a specific format that can be used for further analysis. The program allows users to select multiple FASTA files at once and performs the conversion of all selected files in the background. During the conversion, progress is indicated via a progress bar and a text label.



## Dependencies and Version

This program depends on the following Python libraries, which need to be installed in order for the program to run properly:

Python: The recommended version for this program is Python 3.7 or higher.

Tkinter: This is a standard library for Python 3 and hence its version will be tied to the installed Python version. It should be compatible with Python 3.7 or higher.

Biopython: The recommended version for this program is Biopython 1.78 or higher.

Logging: This too is a standard library for Python 3 and hence its version will be tied to the installed Python version. It should be compatible with Python 3.7 or higher.

OS: This too is a standard library for Python 3 and hence its version will be tied to the installed Python version. It should be compatible with Python 3.7 or higher.

Threading: This too is a standard library for Python 3 and hence its version will be tied to the installed Python version. It should be compatible with Python 3.7 or higher.

Traceback: This too is a standard library for Python 3 and hence its version will be tied to the installed Python version. It should be compatible with Python 3.7 or higher.

You can check the versions of these libraries installed on your system using the pip show <library_name> command. For instance, to check the version of Biopython, you can use the command pip show biopython.

Please note that for Windows users, all these dependencies are already included in the executable file and do not need to be installed separately.

Dependencies Installation

Linux
Open a terminal and execute the following commands:

```text
sudo apt-get update
sudo apt-get install -y python3-tk python3-pip
pip3 install biopython
```


macOS
Open a terminal and execute the following commands:

```text
brew install python3-tk
pip3 install biopython
```


Usage
After the dependencies have been installed, you can run the program from the terminal:

For Linux/macOS:

```text
cd ~/Desktop/fasta2structure
```


Replace "YourUsername" with your actual username.

Run the program with the following command:


```text
python Fasta2Structure.py
```


A window will open. Click on the "Select FASTA files" button and choose the FASTA files you wish to convert. The program will start processing the files and you will see the progress bar being updated. When the conversion is complete, the result will be shown in the "Preview" area and a .str file will be saved in the current directory named "Structure.str".

![image](https://github.com/AdamBessa/Fasta2Structure/assets/16911690/c5e83473-58d3-4206-ab7b-216f004cff3d)



![image](https://github.com/AdamBessa/Fasta2Structure/assets/16911690/85827670-c6db-4463-b625-f4148fa56d3a)



![image](https://github.com/AdamBessa/Fasta2Structure/assets/16911690/2f3363e9-4b9a-4c30-b53e-3969d9021a11)



## Windows Version

For users running the Windows operating system, there is no need for a separate installation process. The program is delivered as a standalone executable file that can be run by double-clicking the file. This version includes all the necessary dependencies, so you don't need to install anything separately. Simply download the executable file, and you can start using the program by double-clicking on it.

Remember that the use remains the same: upon opening, a window will appear where you can click on the "Select FASTA files" button and choose the FASTA files you wish to convert. Progress will be displayed in the same way as described above.

Output Examples
Here are some examples of outputs you can expect when using this program.

For the FASTA input:
```text
>seq1
ATGCCGA
>seq2
AT-CCA
```

Example files that you can use to test this program are provided in the "Example_data" folder. These files are in FASTA format and can be used to observe how the program functions and to understand the output it generates.

The output will be:
```text
seq1 0 3 2 0 1 3
seq2 0 -9 2 2 1 3
```



Post-Processing Instructions

Once you have used the Fasta to Structure Conversion Tool to process your FASTA files, there's a crucial manual step you need to carry out to complete the data preparation for population genetic analysis. This step involves adding a "Pop ID" to each sample in the output "Structure.str" file.

Understanding Pop ID

A "Pop ID" is a unique identifier given to each sample that indicates which population the sample belongs to. This information is vital for population genetics studies as it allows the software to distinguish between samples from different populations.

The concept of a population is based on the specific research questions and can be influenced by various biological and geographical factors. Populations can be differentiated by criteria such as:

Geographic location: Different populations might be sampled from distinct locations.

Phenotypic characteristics: Observable traits might define different groups within the studied species.

Genetic lineage: Genetic data might suggest distinct lineages that are treated as separate populations.

Ecological niches: Populations might be adapted to different ecological conditions.

Since these criteria are highly specific to the context of each study, the tool leaves the assignment of Pop IDs to the researcher.

Adding Pop IDs Manually
To assign Pop IDs to your data in the "Structure.str" file, you'll need to follow these steps:

Open the Output File:

Open "Structure.str" using a text editor for simple formats or spreadsheet software like Microsoft Excel or Google Sheets for a more tabular format.
Review Your Criteria for Population Assignment:

Before you start editing the file, have a clear understanding of your criteria for defining populations.

Insert Pop IDs:

Add a new column or prepend each line with the Pop ID corresponding to each sample. Ensure that this identifier is consistent for all samples belonging to the same population.

Save Your Changes:

After inserting all Pop IDs, save the file (see Example_data/Results/Structure.str).

For more information on the STRUCTURE software format, please refer to the following link: https://web.stanford.edu/group/pritchardlab/structure.html.


Note: Users may also add a count of loci or codes on the first line of the output file Structure.str, if necessary.

Log File

The program logs information about the conversion process in a log file called log.log. This file logs the variable sites for each processed FASTA file and any errors that may have occurred during the conversion. You can check this file for more information if something goes wrong. The entries in the log file follow the format %(name)s - %(levelname)s - %(message)s and are written at the INFO logging level. This means that all messages at the INFO, WARNING, ERROR, and CRITICAL levels will be logged.

Example of a log file entry:
```tex
root - INFO - Variable sites for /path/to/file.fas: [1, 3]
```

Maintenance

1.	Program Maintenance: 

• Bug Fixes: 

Any bugs reported by users or identified by the program developer will be investigated and resolved by the developer. The frequency of bug fixes will be determined by the severity of the bug and its impact on the program's functionality. 

• Updates and Enhancements: 

Updates will be carried out as necessary to maintain the program's efficiency. Enhancements may include adding new features, performance upgrades, and user interface updates. 

• Dependencies: 

This program relies on the BioPython module and the Tkinter library for Python. These dependencies will be monitored for any updates. If these libraries are updated, the program will be tested with the new versions to ensure compatibility.

2.	User Feedback: 

• User feedback is crucial for the continuous improvement of the program. A forum will be established on Google Groups (https://groups.google.com/g/fasta2structure) to facilitate communication with users. The developer will monitor this forum and consider inquiries and suggestions for program improvement.

4.	Documentation: 

•The program's documentation will be maintained and updated as necessary.

5.	Testing: 

•After each update or bug fix, tests will be conducted to ensure that the program is still functioning as expected. The tests will include basic functionality, usability testing, and stress testing.

These maintenance procedures will be reviewed and updated as necessary to ensure continuous and efficient functionality.



JupyterLab interface: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/Fasta2Structure-cli/main?urlpath=%2Flab%2Ftree%2Findex.ipynb)  
Jupyter Notebook 7+:  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/Fasta2Structure-cli/main?urlpath=%2Ftree%2Findex.ipynb)




