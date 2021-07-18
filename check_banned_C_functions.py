#!/usr/bin/python
from __future__ import print_function
import re
import os
import string
import argparse


def get_files(root_dir, excluded_dirs, excluded_files, xf_file):
    print("Looking for all relevant files.. ", end='')

    # concatenate the content of xf_file to excluded_files
    if xf_file is not None:
        with open(xf_file, "r") as f:
            if excluded_files != "x^":
                excluded_files += "," + f.read().strip()
            else:
                excluded_files = "," + f.read().strip()

    # prepare the regex pattern. we replace '.' with '\.' to keep the regular meaning of dot
    dirs_regex  = re.compile( excluded_dirs.replace(".", "\\.").replace(",", "|") )
    files_regex = re.compile( excluded_files.replace(".", "\\.").replace(",", "|") )

    code_files = []
    file_extensions = (".c", ".cc", ".cpp", ".C", ".cxx", ".c++", ".h", ".hh", ".hpp", ".H", ".hxx", ".h++")
    for root, dirs, files in os.walk(root_dir):
        # modify dirs to avoid traversing in excluded directories
        dirs[:] = [d for d in dirs if dirs_regex.match(d) is None]
        for file in files:
            if file.endswith(file_extensions) and files_regex.match(file) is None:
                code_files.append(os.path.join(root, file))

    print("Done.")
    return code_files


def get_banned_functions(file):
    with open(file, "r", errors='ignore') as f:
        banned_functions = f.read().split(",")
    for i in range(len(banned_functions)):
        banned_functions[i] = banned_functions[i].strip()
    return banned_functions


def scan_files(code_files, banned_functions, output):
    for file in code_files:
        # read all lines
        data = []
        with open(file, "r", errors='ignore') as f:
            data = f.readlines()
        i = 0
        while i < len(data):
            line = data[i].strip()
            # if line is empty or a comment, skip it
            if line == "" or line.startswith("//"):
                i += 1
            # if line starts a block of comment skip the entire block
            elif line.startswith("/*"):
                while line.find("*/") == -1:
                    i += 1
                    line = data[i].strip()
                # remove from data[i] the comment and run again the loop in case there is code
                # after the comment in the same line
                data[i] = line[line.find("*/")+2:]
            else:
                # remove trailing comment if exists
                if line.find("//") != -1:
                    line = line[0:line.find("//")]
                elif line.find("/*") != -1:
                    line = line[0:line.find("/*")]
                # check for banned function
                for bf in banned_functions:
                    if line.find(bf) == -1:
                        continue

                    split = line.split(bf)
                    for k in range(len(split)-1):
                        prefix, suffix = split[k], split[k+1]
                        # First check prefix for whitelisted patterns:
                        if prefix and prefix[-1] in tuple(string.ascii_letters + string.digits + '"' + "'" + '_' + '.'):
                            continue
                        # if suffix is empty and we are in the end of the line - set suffix to be next line
                        if suffix == "" and k+1 == len(split)-1 and i+1<len(data):
                            suffix = data[i+1]
                        # check suffix starts with "(" (to assure it is a function call)
                        if (suffix.lstrip().startswith("(")):
                            output.write("file: %s; function: %s; line: %d; code: %s\n" % (file, bf, i + 1, line))

                i += 1


def main():
    parser = argparse.ArgumentParser(description='Scans a repository for banned C functions.')
    parser.add_argument("root_dir", help="root directory of the repository you want to scan")
    parser.add_argument("banned", help="text file with the list of banned C functions separated by a comma (white spaces are allowed)")
    # default value is "x^" that won't match anything as regex
    parser.add_argument("-xf", "--exclude-files", dest="excluded_files", default = "x^",
                        help="List of files to ignore separated by a comma. You can use regex (except the dot character"
                             " that keeps it's regular meaning).\n Note: all files with a given name will be excluded"
                             " - do not add directory name before the file name.")
    parser.add_argument("-xff", "--exclude-many-files", dest="xf_file",
                        help="text file with input for --exclude-files (can use both -xf and -xmf)")
    # default value is "x^" that won't match anything as regex
    parser.add_argument("-xd", "--exclude-dirs", dest="excluded_dirs", default = "x^",
                        help="List of directories to ignore separated by ','. You can use regex (but dot keeps it's regular meaning)")
    parser.add_argument("-o", "--output", default="banned_c_functions_report.txt",
                        help="output file to save the result for further analysis")
    args = parser.parse_args()

    code_files = get_files(args.root_dir, args.excluded_dirs, args.excluded_files, args.xf_file)
    banned_functions = get_banned_functions(args.banned)
    print("Scanning the files now. Writing the output to: " + args.output)
    output = open(args.output, "w")
    scan_files(code_files, banned_functions, output)
    output.close()


if __name__ == "__main__":
    main()
