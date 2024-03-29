**Banned function scaner**

As part of SDL task **[T196]**(https://sdp-prod.intel.com/library/tasks/T196/) - we need to map and clean the usage of Banned functions. 
This tools scans a directory recursively for banned functions in C/C++ code. It can be used by both development and validation teams and can be a base for a gated checkin script.

README for check_banned_C_functions.py

C/C++ code is considered all files that ends with: .c, .cc, .cpp, .C, .cxx, .c++, .h, .hh, .hpp, .H, .hxx, .h++

Usage:  python check_banned_C_functions.py <root_dir> <banned> [-xf excluded_files] [-xff xf_file] [-xd excluded_dirs] [-o output]

root_dir: path to the directory where the repository is
banned: path to a text file of banned functions separated by a comma ',' (whitespaces are allowed)
excluded_files: list of file names to ignore during the scan separated by a comma. You can use regex but dot keeps it's regular meaning (https://docs.python.org/2/library/re.html)
				You cannot add '\' to exclude a file only from a specific folder (cannot do -xf dir/file.c)
				Example: -xf file1.h,file2.c,myfile*.cpp - this will skip file1.h, file2.c and files that match the pattern myfile*.cpp
xf_file: path to a text file with a list of excluded files. the content of this file will be appended to excluded_files and therefore should have the same format
excluded_dirs: like excluded_files but for directories and with the same rules
output: file name where the final report will be stored. All previous data on that file will be erased. default is banned_c_functions_report.txt


Examples:
1. python check_banned_C_functions.py C:\Users\user\Desktop\test banned_list.txt
2. python check_banned_C_functions.py C:\Users\user\Desktop\test banned_list.txt -xf file1.c,file1.h,file2*.c -xd debug -o report.txt
3. python check_banned_C_functions.py C:\Users\user\Desktop\test banned_list.txt -xf dir1/file.c - forbidden! you cannot add '/' to exclude file from specific folder

README for the available input files - Full banned function list, Min banned function list and a list of sensitive functions to be targeted during security code review.

Conntact: 
    Dan Horovitz (dan.horovitz@intel.com) for any aditional help and sugestions. 
    
Planned backlog:
1) Keep updateing the lists.
2) Add support for C#
3) Add support for Java
4) Add support for JS 
