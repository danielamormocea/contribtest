import difflib
import pytest
import generate
import os
import shutil

# compare one output file and one expected file while ignoring empty lines
def compare_files(output, expected_output):
    output_lines = [x for x in open(output).readlines() if x.strip()]
    expected_output_lines = [x for x in open(expected_output).readlines() if x.strip()]


    for line_output, line_expected_output in zip(output_lines, expected_output_lines):
        if line_output != line_expected_output:
            assert False

    return True

# compare all output and all expected files using compare_files
# matching the files by names
def compare_all_files(output, expected):
    expected_files = os.listdir(expected)
    for name in os.listdir(output):
        if os.path.isfile(os.path.join(output, name)) and (name in expected_files):
            if not compare_files(os.path.join(output, name), os.path.join(expected, name)):
                return False

    return True

# test the general no-error scenario
def test_generate_site():
    input_folder = "test/source"
    output_folder = "test/output"
    expected_output_folder = "test/expected_output"

    generate.generate_site(input_folder, output_folder)

    result = compare_all_files(output_folder, expected_output_folder)

    # CLEANUP
    shutil.rmtree(output_folder)

    assert result

# test corner case - input folder does not exist
def test_generate_site_no_input():
    input_folder = ""
    output_folder = "test/output"

    with pytest.raises(FileNotFoundError):
        generate.generate_site(input_folder, output_folder)
    
    # CLEANUP
    shutil.rmtree(output_folder)
    
    assert True

# test corner case - output folder is of wrong format
def test_generate_site_wrong_output():
    input_folder = "test/source"
    output_folder = ""
    
    with pytest.raises(FileNotFoundError):
        generate.generate_site(input_folder, output_folder)
    
    assert True

# test corner case - output folder already exists as file
def test_generate_site_existing_output():
    input_folder = "test/source"
    output_folder = "generate.py"
    
    with pytest.raises(FileExistsError):
        generate.generate_site(input_folder, output_folder)
    
    assert True