# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
import jinja2
import sys
import json
import shutil
import argparse

log = logging.getLogger(__name__)


def list_files(folder_path):
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name)

def read_file(file_path):
    with open(file_path, 'r') as f:
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line
        content = ""
        for line in f:
            content += line
    return json.loads(raw_metadata), content

def write_output(output_folder, name, html):
    with open(os.path.join(output_folder, name+'.html'), "w+") as f:
        f.write(html)

# reset (create and/or delete) the output folder
def reset_output_folder(output_folder_path, force_deletion=False):
    if os.path.exists(output_folder_path) and os.path.isdir(output_folder_path):
        if not force_deletion:
            log.warning("The output directory already exists. Run with --force_deletion to force the deletion of the output directory.")
            return False
        else:
            shutil.rmtree(output_folder_path)
    os.makedirs(output_folder_path)
    return True

def generate_site(input_folder_path, output_folder_path, force_deletion=False):
    log.info("Resetting output folder")
    if not reset_output_folder(output_folder_path, force_deletion):
        return False
    
    log.info("Generating site from %r", input_folder_path)
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(f"{input_folder_path}/layout"))
    
    for file_path in list_files(input_folder_path):
        metadata, content = read_file(file_path)
        template_name = metadata['layout']

        template = jinja_env.get_template(template_name)
        data = dict(metadata, content=content)
        html = template.render(**data)
        
        # get the name of the current file
        file_name = file_path.split('/')[-1]
        base, _ = os.path.splitext(file_name)
        
        log.info("Writing %r with template %r", base, template_name)
        write_output(output_folder_path, base, html)
    
    return True


def main(args):
    generate_site(args.input_folder_path, args.output_folder_path, args.force_deletion)

if __name__ == '__main__':
    # allow the program to be run with the required parameters, 
    # but also with optional parameters, such as logging level
    # or force-deletion in case the output folder already exists
    parser = argparse.ArgumentParser(description='Generate html files from template')
    parser.add_argument("input_folder_path", help="The source folder containing the templates.")
    parser.add_argument("output_folder_path", help="The output folder where we write the generated html files.")
    parser.add_argument("--log", help="The log level of the program. Defaults to INFO", default="INFO")
    parser.add_argument("--force_deletion", help="Force the deletion of the output directory", action="store_true")
    args = parser.parse_args()
    
    # get the value from the log level provided in parameters
    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    
    logging.basicConfig(level=numeric_level)
    main(args)



