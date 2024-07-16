#!/usr/bin/env python
# `test_no_changes_introduced_to_results.py` by Wayne Decatur
# Use in folder with associated `conftest.py`
import pytest
import os
import fnmatch
import filecmp

# Run this file like `pytest -v tests/test_no_changes_introduced_to_results.py` 

# There is an associated `conftest.py` file that will be automatically 
# discovered and used by pytest that will handle setting things up for these 
# tests by doing the additional preparation necessary by running the current
# (presumably new) verison of `improved_Fasta2Structure.py` to make the files 
# of results corresponding to the previously stored versons made by 
# `Fasta2Structure.py`(GUI-based). 



#*******************************************************************************
##################################
#  FILE PATHS       #

##################################
#

current_provided_example = "tests/current_results_provided_by_Adam_Bessa/Structure.str"
provided_example_as_of_when_I_forked = "Example_data/Results/Structure.str"
provided_example_adjusted_to_match_what_I_expect = "Example_data/Results/EXPECTED_in_July2024_Structure.str"
provided_log_file = "Example_data/Results/log.log"
guiFasta2StructureDOTpy_results = "tests/results_observed_from_original_with_Example_data"
what_I_observe_Fasta2StructureDOTpy_give_for_all_three_example_datasets = "tests/results_observed_from_original_with_Example_data/from_all_three_at_once_Structure.str"
log_I_observe_Fasta2StructureDOTpy_give_for_all_three_example_datasets = "tests/results_observed_from_original_with_Example_data/from_all_three_at_once_log.log"

#
#*******************************************************************************
#*****************************END FILE PATHS************************************





###---------------------------HELPER FUNCTIONS-------------------------------###

def make_corresponding_GUIobtained_filename(file_name):
    '''
    Takes a filename and makes it match pattern I used to name things in `results_observed_from_original_with_Example_data` based on names in `Example_data/Datasets`
    Specific example
    ================
    Calling function with
        ("ITS.fas")
    returns
        "from_ITS.fas_Structure.str"
    '''
    return "from_{}_Structure.str".format(file_name)

def make_corresponding_GUIobtained_logname(file_name):
    '''
    Takes a filename and makes it match pattern I used to name things in `results_observed_from_original_with_Example_data` based on names in `Example_data/Datasets`
    Specific example
    ================
    Calling function with
        ("ITS.fas")
    returns
        "from_ITS.fas_log.log"
    '''
    return "from_{}_log.log".format(file_name)

def read_and_process_file4content_check(file_path):
    '''
    read file for content check
    '''
    processed_data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = [part for part in line.split() if part]
            if parts:
                processed_data.append(parts)
    return processed_data

def compare_files_content(file1_path, file2_path):
    '''
    Compare content ignoring whitespace differences
    '''
    data1 = read_and_process_file4content_check(file1_path)
    data2 = read_and_process_file4content_check(file2_path)

    assert len(data1) == len(data2), f"Files have different number of lines: {len(data1)} vs {len(data2)}"

    for i, (line1, line2) in enumerate(zip(data1, data2), 1):
        assert line1 == line2, f"Difference found at line {i}:\nFile 1: {' '.join(line1)}\nFile 2: {' '.join(line2)}"

    return True  # If we get here, the files are identical in content

def compare_file_content_equality(file1_path, file2_path, msg="Files are not identical in content, ignoring whitespace differences."):
    '''
    Compare two files content ignoring whitespace differences

    Has a default assertion message, but you can pass your own string as third
    argument in call or only pass the two paths and use the default.
    '''
    assert compare_files_content(file1_path, file2_path), msg

def parse_number_FASTA_selected(file_path):
    '''
    parse out number of files selected
    '''
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        log_content=file.read()
        return log_content.split("FASTA files selected.",1)[0].split()[-1].strip()

def extract_tag(file_path, process_number):
    '''
    from the content that will be in a log file of runs of the fasta2structure 
    example data get the 'tag' from the file base name I can use to match the 
    corresponding input data. The process number is the step number for logs
    made with more than one input file as part of the input.
    For example, for `Example_data/Datasets/ITS.fas`,
    the tag is `ITS.fas`.

    Except thete is an issue with the `log.log` that Adam Bessa provides
    in `Example_data/Results/`.
    These are the corresponding tags/names of FASTA file there and so I'll add 
    special handling for those since they don't conform to all the others.
    Avicennia-ITS_Phase.fas', 'Avicennia-trnD-trnT_ediphase.fas', 'Avicennia-trnH-trnK_editphase.fas
    '''
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        log_content=file.read()
        if 'Avicennia-' in log_content:
            return log_content.split(".fas",process_number)[process_number-1].split("Avicennia-")[1].split("_",1)[0]+".fas"
        else:
            return log_content.split(".fas",process_number)[process_number-1].split("/")[-1]+".fas"

def parse_variable_sites_info(file_path,process_number):
    '''
    parse out the variable sites string corresponding to the step number 
    (process_number) of such data in the log text content for where there is 
    more than one input file when the script is called.
    '''
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        log_content=file.read()
        return "["+log_content.split("[",process_number)[process_number].split("]")[0]+"]"

def compare_log_info(file1_path, file2_path):
    '''
    Compare number of number of FASTA files selected and variable sites info in 
    two specified log files
    '''
    # parse out number of files selected
    sel1 = parse_number_FASTA_selected(file1_path)
    sel2 = parse_number_FASTA_selected(file2_path)

    assert sel1 == sel2, f"Files have different number of FASTA files selected: {sel1} vs {sel2}"

    # There will be a number of variable sites information to compare equal to the number of files selected
    # make a dictionary to relate the names/tag for each one so matching the same
    # parse out variable sites information. One for file1 and one for file2.
    # Note that the dictonary is made with the 'tag' from the name of the input
    # file as key so the actual order of occurence/listing in the log file 
    # content won't matter for the comparison.
    tag_and_variable_sites_f1 = {}
    tag_and_variable_sites_f2 = {}
    for i in range(int(sel1)):
        tag1 = extract_tag(file1_path,i+1)
        tag_and_variable_sites_f1[tag1] = parse_variable_sites_info(file1_path, i+1)
        tag2 = extract_tag(file2_path,i+1)
        tag_and_variable_sites_f2[tag2] = parse_variable_sites_info(file2_path, i+1)

    # sanity check: the number of keys should match sel1 and keys in the 
    # dictionary should be same.
    assert len(tag_and_variable_sites_f1) == int(sel1), f"The length of the dictionary keys old example logs, {len(tag_and_variable_sites_f1)}, for the file name tags should be the same as the number of FASTA files input into the log, {sel1}."
    assert len(tag_and_variable_sites_f2) == int(sel1), f"The length of the dictionary keys for current example logs, {len(tag_and_variable_sites_f2)}, for the file name tags should be the same as the number of FASTA files input into the log, {sel1}."
    assert len(tag_and_variable_sites_f1) == len(tag_and_variable_sites_f2), f"The number of the dictionary keys for current example logs, {len(tag_and_variable_sites_f2)}, for the file name tags should be the same as the value for length of the dictionary keys for current example logs, {len(tag_and_variable_sites_f2)}."
    assert tag_and_variable_sites_f1.keys() == tag_and_variable_sites_f2.keys(), f"The keys in the two dictionaries should match."


    # Now iterate on the dictionary and compare the variable sites for each tag.
    # Because the tags were used for the dictionary the actual order of the 
    # content appearing in the logs is moot. It is just checking the associated
    # data from the same input file matches.
    for fastafile,vs1 in tag_and_variable_sites_f1.items():
        vs2 = tag_and_variable_sites_f2[fastafile]

        assert vs1 == vs2, f"Files have different details for variable sites concerning the `{fastafile}` pair: {sel1} vs {sel2}"

    return True  # If we get here, the files have same FASTA file number and variable sites info



def compare_file_number_and_variable_sites_in_log(file1_path, file2_path, msg="Files are not identical in content, ignoring whitespace differences."):
    '''
    Compare number of number of FASTA files selected and variable sites info in 
    two specified log files

    Has a default assertion message, but you can pass your own string as third
    argument in call or only pass the two paths and use the default.
    '''
    assert compare_log_info(file1_path, file2_path), msg



#import the shared helper function from `conftest.py`
#from conftest import make_corresponding_GUIobtained_filename

# import the function that gives string `example_datasets_location` because cannot
# use a pytest fixture to pass this one since used in `@pytest.mark.parametrize()`
# that seemed incompatible with fixtures
from conftest import get_example_datasets_location
example_datasets_location = get_example_datasets_location()

###--------------------------END OF HELPER FUNCTIONS--------------------------###
###--------------------------END OF HELPER FUNCTIONS--------------------------###







# Check the `Structure.str` files all match.
#--------------------------------------------------------------------------#
# First check `Structure.str` currently at Adam Bessa's 
# AdamBessa/Fasta2Structure repo matches one I got when forked my repo. If
# altered I need to update things and check what is necessary to update:
# - Did Adam just chane the results provided?
# - Did the script change? If so, can I easily work in changes so my 
#   'improved' version is consistent.
# This check is especially so I am aware in light of https://github.com/AdamBessa/Fasta2Structure/issues/4
def test_current_result_matches_results_in_my_fork():
    assert filecmp.cmp(current_provided_example, provided_example_as_of_when_I_forked), "The current results Adam Bessa provides don't match what was there when I forked."
test_current_result_matches_results_in_my_fork()

# Next check if the results from each one used as input individually matches 
# because probably the main test will fail if even simplest one do.
@pytest.mark.parametrize("filename", [f for f in os.listdir(example_datasets_location) if fnmatch.fnmatch(f, '*.fas')])
def test_old_script_results_vs_new_results_from_new_script(filename,dir_with_new_results_set_inCONFTEST, ind_results_noms):    # call the variables coming over from conftest.py in the function
    dir_with_new_results = dir_with_new_results_set_inCONFTEST # need because cannot name the function same as this one for some reason the fixture is set up in module. Tried a lot of tricks to not have it be that way but nothing seemed to work. Because strign getting confused with fixture function.
    GUI_results_name = make_corresponding_GUIobtained_filename(filename)
    GUI_results_path = os.path.join(guiFasta2StructureDOTpy_results, GUI_results_name)
    correspond_name_for_new = [item for item in ind_results_noms if item.startswith(f"tmp_{filename}")][0]
    correspond_path_for_new = os.path.join(dir_with_new_results, correspond_name_for_new)
    assert filecmp.cmp(GUI_results_path, correspond_path_for_new), f"The results in the file `{GUI_results_name}` generated by Fasta2Structure.py (GUI) and `{correspond_name_for_new}` generated by improved_Fasta2Structure.py were expected to match; however, THEY DON'T MATCH!"
'''Claude.ai said that above using pytest's parametrize decorator was better approach then what I had, which is below, because it will automatically make a test for each one that way whereas mine had a single test, like the following earlier draft:
def test_old_script_results_vs_new_results_from_new_script():
    for filename in os.listdir(example_datasets_location):
            if fnmatch.fnmatch(filename, '*.fas'):
                GUI_results_name = make_corresponding_GUIobtained_filename(filename)
                GUI_results_path = os.path.join(guiFasta2StructureDOTpy_results, GUI_results_name)
                correspond_name_for_new = [item for item in ind_results_noms if item.startswith(f"tmp_{filename}")][0]
                correspond_path_for_new = os.path.join(dir_with_new_results, correspond_name_for_new)
                assert filecmp.cmp(GUI_results_path, correspond_path_for_new), f"The results in {GUI_results_name} and {correspond_name_for_new} were expected to match, however, THEY DON't MATCH!"
'''

# Check provided 'Result' from Adam Bessa I got when I forked the repo is still his
# provided 'Result' because I posted an issue saying this isn't like what I see [here](https://github.com/AdamBessa/Fasta2Structure/issues/4#issue-2352073543)
# and if he updates I need to check if content any different so I can know if 
# I also need to check if my improved script gives same result as original script.
# Or to look and see if original script changed and incorporate differnces into 
# my improved script to see if then get provided same result. So this check
# will help keep my notified.
# Compare `tests/current_results_provided_by_Adam_Bessa/Structure.str` and `Example_data/Results/Structure.str`
# which are defined above as: `current_provided_example` 
# & `provided_example_as_of_when_I_forked`
def test_AdamBessa_has_not_changed_provided_results_file():
    assert filecmp.cmp(current_provided_example, provided_example_as_of_when_I_forked), f"The results in the file `{os.path.basename(current_provided_example)}` (located in `{os.path.dirname(current_provided_example)}`) currently provided by Adam Bessa as a representative result and the earlier example `{os.path.basename(provided_example_as_of_when_I_forked)}` provided as 'Result' by Fasta2Structure.py developer Adam Bessa (located in {os.path.dirname(provided_example_as_of_when_I_forked)}) when I forked the repo were expected to match; however, THEY DON'T MATCH! Adam Bessa has probably updated provided results AND  I WILL NEED TO ASSESS if improved script needs updating."

# Next THE BIG main checks! 
# Check if the results when give all three examples at the same time matches 
# what had been provided by AdamBessa earlier in the case of the combined data.
# Just going to check content because I found inconsistency with how 
# `Fasta2Structure.py (GUI-based)` handling spacing around `-9` in my hands and 
# so I cannot easily go from them embedded in tabs to the spacing versions I find 
# with `Fasta2Structure.py (GUI-based)` in my hand. So do not consider whitespace.
def test_provided_has_same_content_as_new_results_with_data_where_all_three_genes_targeted_as_input_at_same_time(dir_with_new_results_set_inCONFTEST, unique_prefix_for_with_three):   #`unique_prefix_for_with_three` comes from conftest, passing into here via pytest fixture
    dir_with_new_results = dir_with_new_results_set_inCONFTEST # need because cannot name the function same as this one for some reason the fixture is set up in module. Tried a lot of tricks to not have it be that way but nothing seemed to work. Because strign getting confused with fixture function.
    compare_file_content_equality(provided_example_adjusted_to_match_what_I_expect, f"{dir_with_new_results}/{unique_prefix_for_with_three}_Structure.str", f"The results in the file `{os.path.basename(provided_example_adjusted_to_match_what_I_expect)}` (located in `{os.path.dirname(provided_example_adjusted_to_match_what_I_expect)}`) provided as 'Result' by Fasta2Structure.py developer Adam Bessa (but processed slightly to match more of what I'm seeing in my hands) and `{unique_prefix_for_with_three}_Structure.str` (located in `{dir_with_new_results}`) generated by improved_Fasta2Structure.py with `Example_data/Datasets/ITS.fas Example_data/Datasets/trnD-trnT.fas Example_data/Datasets/trnH-trnK.fas` were expected to match; however, THEY DON'T HAVE SAME CONTENT, ignoring whitespace! THIS IS VERY, VERY BAD!!! THIS IS BIG PROBLEM!!!")
# Check if the results when give all three examples at the same time matches 
# what I myself had obtained from Fasta2Structure.py (GUI-based) previously in the case of the combined data.
def test_old_vs_new_results_with_data_where_all_three_genes_targeted_as_input_at_same_time(dir_with_new_results_set_inCONFTEST, unique_prefix_for_with_three, three_nom_prefix):   #`unique_prefix_for_with_three` comes from conftest, passing into here via pytest fixture
    dir_with_new_results = dir_with_new_results_set_inCONFTEST # need because cannot name the function same as this one for some reason the fixture is set up in module. Tried a lot of tricks to not have it be that way but nothing seemed to work. Because strign getting confused with fixture function.
    GUI_results_name_all_three = f"{three_nom_prefix}_Structure.str"
    GUI_results_path_all_three = os.path.join(guiFasta2StructureDOTpy_results, GUI_results_name_all_three)
    assert filecmp.cmp(GUI_results_path_all_three, f"{dir_with_new_results}/{unique_prefix_for_with_three}_Structure.str"), f"The results in the file `{os.path.basename(provided_example_adjusted_to_match_what_I_expect)}` (located in `{os.path.dirname(provided_example_adjusted_to_match_what_I_expect)}`) generated by Fasta2Structure.py (GUI-based) after selecting all three genes at same time and `{unique_prefix_for_with_three}_Structure.str` (located in `{dir_with_new_results}`) generated by improved_Fasta2Structure.py with `Example_data/Datasets/ITS.fas Example_data/Datasets/trnD-trnT.fas Example_data/Datasets/trnH-trnK.fas` were expected to match; however, THEY DON'T MATCH! THIS IS VERY, VERY BAD!!! THIS IS BIG PROBLEM!!!"


# Use code to check the INFO (number FASTA files selected & the elements in 
# Variable sites) in `log.log` files match
#--------------------------------------------------------------------------#

# check the individual logs where each input used individually matches 
# because probably the main log where all three targeted will fail if even 
# simplest logs fail.
@pytest.mark.parametrize("filename", [f for f in os.listdir(example_datasets_location) if fnmatch.fnmatch(f, '*.fas')])
def test_old_script_logs_vs_new_logs_from_new_script(filename,dir_with_new_results_set_inCONFTEST, ind_log_noms):    # call the variables coming over from conftest.py in the function
    dir_with_new_results = dir_with_new_results_set_inCONFTEST # need because cannot name the function same as this one for some reason the fixture is set up in module. Tried a lot of tricks to not have it be that way but nothing seemed to work. Because strign getting confused with fixture function.
    GUI_log_name = make_corresponding_GUIobtained_logname(filename)
    GUI_log_path = os.path.join(guiFasta2StructureDOTpy_results, GUI_log_name)
    correspond_name_for_newlog = [item for item in ind_log_noms if item.startswith(f"tmp_{filename}")][0]
    correspond_path_for_newlog = os.path.join(dir_with_new_results, correspond_name_for_newlog)
    compare_file_number_and_variable_sites_in_log(GUI_log_path, correspond_path_for_newlog, f"The log in the file `{GUI_log_name}` generated by Fasta2Structure.py (GUI) and `{correspond_name_for_newlog}` generated by improved_Fasta2Structure.py were expected to match; however, THEY DON'T MATCH!")

# check the log with all three at once matches the data in the `provided_log_file`
def test_log_Adam_Bessa_provided_matches_current_for_all_three_at_once(dir_with_new_results_set_inCONFTEST, three_nom_prefix, unique_prefix_for_with_three):    # call the variables coming over from conftest.py in the function
    dir_with_new_results = dir_with_new_results_set_inCONFTEST # need because cannot name the function same as this one for some reason the fixture is set up in module. Tried a lot of tricks to not have it be that way but nothing seemed to work. Because strign getting confused with fixture function.
    current_log_all_three = f"{dir_with_new_results}/{unique_prefix_for_with_three}_log.log"
    compare_file_number_and_variable_sites_in_log(provided_log_file,current_log_all_three)

# check the log with all three at once also matches the content in `from_all_three_at_once_log.log`, which is the log obtained when I give all three examples at the same time matches to Fasta2Structure.py (GUI-based) previous times in the case of the combined data.
def test_log_I_got_previously_with_all_three_at_once_matches_current_for_all_three_at_once(dir_with_new_results_set_inCONFTEST, three_nom_prefix, unique_prefix_for_with_three):    # call the variables coming over from conftest.py in the function
    dir_with_new_results = dir_with_new_results_set_inCONFTEST # need because cannot name the function same as this one for some reason the fixture is set up in module. Tried a lot of tricks to not have it be that way but nothing seemed to work. Because strign getting confused with fixture function.
    current_log_all_three = f"{dir_with_new_results}/{unique_prefix_for_with_three}_log.log"
    compare_file_number_and_variable_sites_in_log(log_I_observe_Fasta2StructureDOTpy_give_for_all_three_example_datasets,current_log_all_three)

