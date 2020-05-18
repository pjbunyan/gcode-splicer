import argparse
import os.path
import sys
import re

def continue_question(explanation = ''):
    """Asks the user if they want to continue with an optional explanation
        for why they are being asked. Returns 'y' or 'n' from the user."""
    if explanation:
        question = explanation + ', do you wish to continue? [Y/n]:'
    else:
        question = 'Do you wish to continue? [Y/n]:'
        
    answer = input(question).strip().lower()[0]
    while answer not in ('y','n'):
        answer = input(question).strip().lower()[0]
        
    return answer

def open_file(filename, mode):

    if 'w' in mode and os.path.exists(output_filename):
        if 'n' == continue_question('File ' + output_filename 
                                    + ' already exists'):
            sys.exit()

    try: 
        file = open(filename, mode)
    except FileNotFoundError:
        print('File', input_filename, '''does not exist or you do not
            have permission to read it''')
        sys.exit()
    except PermissionError:
        print('You do not have permission to write to', output_filename)
        sys.exit()

    return file
    
def compare_list_lengths(lists):
    if all(isinstance(element, list) for element in lists):
        first_length = len(lists[0])
        return all((len(list) == first_length) for list in lists[1:])
    else:
        return False
        
def get_lines(file, start_line = 0, end_line = None):
    lines = []
    for line in file[start_line:end_line]:
        lines.append(line)
    
    return lines
        
def parse_input_files(file_list):
    layer_start_pattern = re.compile(r';LAYER:\d+\n')
    files = []
    files_layer_changes = []
    for filename in file_list:
        file = open_file(filename, 'r')
        file_contents = []
        layer_changes = []
        for line_num, line in enumerate(file):
            file_contents.append(line)
            if layer_start_pattern.match(line):
                layer_changes.append(line_num)
        files.append(file_contents)
        files_layer_changes.append(layer_changes)
        file.close()
        
    return files, files_layer_changes
    
def splice_files(files, files_layer_changes, start_layer):
    output_file = []

    num_files = len(files)
    num_layers = len(files_layer_changes[0])
    num_layers_per_file = int((num_layers - start_layer) / num_files)
        
    start_line = 0
    end_layer = start_layer
    end_line = files_layer_changes[0][end_layer]
    for file_num, file in enumerate(files[:-1]):
        end_layer += num_layers_per_file
        end_line = files_layer_changes[file_num][end_layer]
        lines = get_lines(file, start_line, end_line);
        output_file.extend(lines)
        start_line = end_line
    
    last_file = files[-1]
    print(start_line)
    lines = get_lines(last_file, start_line);
    output_file.extend(lines)
    
    return output_file

def main(input_filenames, output_filename, start_layer):
    
    files, files_layer_changes = parse_input_files(input_filenames)
        
    #If there aren't an equal number of layers in all files then we
    #shouldn't try to combine them
    if compare_list_lengths(files_layer_changes) == False:
        print('Files do not contain an equal number of layers!')
        sys.exit()
        
    output_lines = splice_files(files, files_layer_changes, start_layer)
    
    output_file = open_file(output_filename, 'w')
    output_file.writelines(output_lines)
    output_file.close()
    
    
    


if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('gcode_files', type = str, nargs = '+',
                        help = 'specify the names of the input files')
    parser.add_argument('-o', '--output-file', type = str, nargs=None,
                        help = '''specify the output file.''')
    parser.add_argument('-s', '--start-layer', type = int, nargs = '?',
                        const = 0, help = '''The layer to start 
                        switching at. Defaults to Layer 1''')
    args = parser.parse_args()
    
    input_filenames = args.gcode_files
    if args.output_file:
        output_filename = args.output_file
    else:
        output_filename = input_filenames[0]
    if args.start_layer:
        start_layer = args.start_layer
    else:
        start_layer = 1;
        
    main(input_filenames, output_filename, start_layer)
