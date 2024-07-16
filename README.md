[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/Fasta2Structure-cli/main?urlpath=%2Flab%2Ftree%2Findex.ipynb)

---------------
Attribution
----------
This fork of [the official Fasta2Structure repository](https://github.com/AdamBessa/Fasta2Structure) was set up to take advantage of the MyBinder system to offer a resource to run Fasta2Structure without the user needing to download, install, or maintain any software. Plus, no need to be running it in a typical desktop situation and so the Fasta2Structure script is more convenient to use pretty much anywhere. See [here](https://mybinder.readthedocs.io/en/latest/) for documentation about Binder as deployed at [MyBinder.org](https://mybinder.org/).  
Please see [the official Fasta2Structure repository](https://github.com/AdamBessa/Fasta2Structure) for more information about Fasta2Structure.  
**Remember, if you are using Fasta2Structure, please cite**:  
[Fasta2Structure: a user-friendly tool for converting multiple aligned FASTA files to STRUCTURE format. Bessa-Silva A. BMC Bioinformatics. 2024 Feb 15;25(1):73. doi: 10.1186/s12859-024-05697-7. PMID: 38365590](https://pubmed.ncbi.nlm.nih.gov/38365590/)


# Fasta2Structure-cli
Fasta2Structure: A User-Friendly Tool for Converting Multiple Aligned FASTA Files to STRUCTURE Format, that is even more user-friendly because it doesn't need Tkinter and can thus run well anywhere, such as on a computer cluster or in Jupyter running remotely or in conjunction with software to make pipelines like Snakemake & NextFlow.  
Plus, combined with Jupyter served by the MyBinder service it will make it easier for anyone to try the software or use it without installing anything on their own computer.  

To make it more convenient to use, I've modified the Fasta2Structure script to allow more ways to run it to produce Fasta2Structure-cli. It will run on the command line if you supply arguments specifying files as input or fallback to running on the command line if Tkinter cannot connect to a graphical display.    
You can still try the original GUI-based (Tkinter) software presently available at https://github.com/AdamBessa/Fasta2Structure without installing anything on your computer. You can go [here](https://gist.github.com/fomightez/e65761a066f56cbbc4c9b5b882c87380) and find a step-by-step to use a remote virtual desktop to test the Fasta2Structure script. Only you'll find it isn't as convenient as what is provided here.

I have added a series of extensive tests to make sure the Fasta2Structure-cli gives the same result as running the GUI-based (Tkinter) `Fasta2Structure.py` presently available at https://github.com/AdamBessa/Fasta2Structure. 

#### Background (from original source repo by Adam Bessa)

The STRUCTURE software has gained popularity as a tool for population structure and genetic analysis. However, tailoring data to meet STRUCTURE's specific requirements can be challenging and prone to errors, particularly when managing multilocus data. Here, I introduce a graphical user interface (GUI) application designed to simplify the process of converting multiple sequence alignments into a single, cohesive file that is compatible with the STRUCTURE software. The application has been developed using Tkinter for the GUI and Biopython for handling FASTA files. It processes the files, identifies variable sites, and converts the sequences into a binary format. Subsequently, the sequences are concatenated and displayed within the graphical interface's text area, enabling users to review and verify the results. Furthermore, the program saves the concatenated results in a file, thereby providing a ready-to-use input for the STRUCTURE software. This application presents an efficient and reliable solution for transforming multiple aligned FASTA files into a concatenated binary format file, which is compatible with the STRUCTURE software. With its user-friendly graphical interface and error-reduction strategy, this tool proves to be invaluable for researchers engaged in population structure and genetic analysis. This program is designed to convert FASTA files into a binary representation that is then used to identify variable sites. This binary representation is then saved in a structure (.str) file. Variable sites are defined as positions in the sequence where the nucleotides differ among the sequences in the alignment. These sites are identified and flagged, and the resulting data is saved in a specific format that can be used for further analysis. The program allows users to select multiple FASTA files at once and performs the conversion of all selected files in the background. During the conversion, progress is indicated via a progress bar and a text label.



## Demostration

A session will open with all the necessary packages to support running the imporved Fasta2Structure script. The documentation for the original script `Fasta2Structure.py` details this more, see [there](https://github.com/AdamBessa/Fasta2Structure).
I have added a notebook that will open when the MyBinder session starts up that will illustrate using the improved script.  


## Want to try the original without installing anything?

You can still try the original GUI-based (Tkinter) software presently available at https://github.com/AdamBessa/Fasta2Structure without installing anything on your computer. You can go [here](https://gist.github.com/fomightez/e65761a066f56cbbc4c9b5b882c87380) and find a step-by-step to use a remote virtual desktop to test the Fasta2Structure script. Only you'll find it isn't as convenient as what is provided here.



![image](https://github.com/AdamBessa/Fasta2Structure/assets/16911690/c5e83473-58d3-4206-ab7b-216f004cff3d)



![image](https://github.com/AdamBessa/Fasta2Structure/assets/16911690/85827670-c6db-4463-b625-f4148fa56d3a)



![image](https://github.com/AdamBessa/Fasta2Structure/assets/16911690/2f3363e9-4b9a-4c30-b53e-3969d9021a11)


-----------------------------------------------------------------------------------------


JupyterLab interface: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/Fasta2Structure-cli/main?urlpath=%2Flab%2Ftree%2Findex.ipynb)  
Jupyter Notebook 7+:  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/Fasta2Structure-cli/main?urlpath=%2Ftree%2Findex.ipynb)




