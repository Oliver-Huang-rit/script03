#!/usr/bin/env python3
# Author: Oliver Huang
# Date: 10/14/2021

import os
import sys
from os import system, name
from datetime import date
import subprocess
import csv
import re
import time
from subprocess import check_output

#clear the terminal
def clear_terminal():
    if name == 'nt': # if the system is Windows
        _ = system('cls')
    else: # if is other system
        _ = system('clear')

def print_manu():
    print("\n\n-----------------------------------------------------\n\n")
    print("Enter Selection (1, 2, or 3):\n\n")
    print("\t1 - Create a shortcut in your home directory.\n")
    print("\t2 - Remove a shortcaut from your home directory.\n")
    print("\t3 - Run shortcut Report\n\n")

def create_link():
    print("Current path: ", os.getcwd(),"\n")
    source = input("Enter the source file: ")
    target = input("Enter the target file: ")
    t_re = subprocess.call(["find", target])
    if t_re == 1:
        s_re = (str)(check_output(["sudo", "find", "/home", "-name", source]))
        while (s_re == "b\'\'"):
            print("\nCan not find the source file, please try again")
            target = input("Enter the source file: ")
            s_re = (str)(check_output(["sudo", "find", "/home", "-name", source]))
        s_path = os.path.abspath(source)
        os.chdir(os.path.expanduser('~'))
        subprocess.call(["ln", "-s", source, target])
        subprocess.call(["ls", "-ld", target])
    else:
        print("\nTarget exit, please try again...\n")
        time.sleep(0.5)
        create_link()

def delete_link():
    os.chdir(os.path.expanduser('~'))
    print("Current path: ", os.getcwd(),"\n")
    target = input("Enter the shortcut: ")
    t_re = subprocess.call(["find", target])
    if t_re == 0:
        l_re = subprocess.call(["readlink", target])
        if l_re == 0:
            subprocess.call(["/bin/rm", target])
        else:
            print("The shortcut is not a symlink, please try again...")
            time.sleep(1)
    else:
        print("The shortcut does not exit, please try again...")
        time.sleep(1)

def run_report():
    os.chdir(os.path.expanduser('~'))
    title = "Symbolic Link"
    for i in range (0, 13):
        title += " "
    title += "Target Path"
    print("\033[33", title, "\033[0m\n")
    
    files = (str)(check_output("ls"))
    files = files.split("b'")
    files = files[1]
    files = files.split("'")
    files = files[0]
    files = files.splitlines()
    files = files[0]
    files = files.split("\\n")

    for i in range(0, len(files) - 1):
        re = subprocess.call(["readlink", files[i]])
        if re == 0:
            current = files[i]
            for i in range(0, 20 - len(current)):
                current += " "
            path = (str)(check_output(["readlink", files[i]]))
            path = path.split("b'")
            path = path[1]
            path = path.split("'")
            path = path[0]
            path = path.splitlines()
            path = path[0]
            path = path.split("\\n")
            path = path[0]
            current += path
            print(current, "\n")

def main():
    os.chdir(os.path.expanduser('~'))
    clear_terminal()
    print_manu()
    print("Current path: ", os.getcwd(),"\n")
    selected = input("Plrase enter a \033[32mnumber (1, 2, or 3)\033[0m or \033[31m\"quit\"\033[0m to quit the program: ")
    while selected != "quit":
        if selected == "1":
            create_link()
        elif selected == "2":
            delete_link()
        elif selected == "3":
            run_report()
        else:
            print("Unrecognized input, please try again...\n")
        time.sleep(1)
        clear_terminal()
        print_manu()
        print("Current path: ", os.getcwd(),"\n")
        selected = input("Plrase enter a \033[32mnumber (1, 2, or 3)\033[0m or \033[31m\"Q\q\"\033[0m to quit the program: ")


main()