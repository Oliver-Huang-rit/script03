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

# the function to clear the terminal
def clear_terminal():
    if name == 'nt': # if the system is Windows
        _ = system('cls')
    else: # if is other system
        _ = system('clear')

# the function to print the menu
def print_menu():
    print("\n\n--------------------------------------------------------------\n\n")
    print("Enter Selection (1, 2, or 3):\n\n")
    print("\t1 - Create a shortcut in your home directory.\n") # first choice
    print("\t2 - Remove a shortcaut from your home directory.\n") # second choice
    print("\t3 - Run shortcut Report\n\n") # third choice

# the fucntion to create the link
def create_link():
    print("Current path: ", os.getcwd(),"\n") # inform the current path
    source = input("Enter the source file: ") # get the source
    target = input("Enter the target file: ") # get the target
    t_re = subprocess.call(["find", target])
    if t_re == 1: # if target doesn't exist
        s_re = (str)(check_output(["sudo", "find", "/home", "-name", source]))
        while (s_re == "b\'\'"): # asking for input as long as the source does not exit
            print("\nCan not find the source file, please try again")
            source = input("Enter the source file: ") # ask for source
            s_re = (str)(check_output(["sudo", "find", "/home", "-name", source]))
        s_path = os.path.abspath(source) # get the absolute path of th source
        os.chdir(os.path.expanduser('~')) # make sure is at the home directory
        subprocess.call(["ln", "-s", source, target]) # create the symlink
        subprocess.call(["ls", "-ld", target]) # display the symlink
        time.sleep(1)
    else: # if target exist
        print("\nTarget exit, please try again...\n")
        time.sleep(0.5) # let user see the message
        create_link() # restart at the beginning of this function

# the fucntion to delete the link
def delete_link():
    os.chdir(os.path.expanduser('~'))  # make sure is at the home directory
    print("Current path: ", os.getcwd(),"\n") # show the current directory
    target = input("Enter the shortcut: ") # ask for the shortcut to be deleted
    t_re = subprocess.call(["find", target])
    if t_re == 0: # if the shortcut exit
        l_re = subprocess.call(["readlink", target])
        if l_re == 0: # if the shortcut is a symlink
            subprocess.call(["/bin/rm", target]) # delete the symlink
        else: # if the shortcut is not a symlink
            print("The shortcut is not a symlink, please try again...")
            time.sleep(1) # get back to the menu
    else: #if the shortcut does not exit
        print("The shortcut does not exit, please try again...")
        time.sleep(1) # back to the menu

# the function to display the report
def run_report():
    os.chdir(os.path.expanduser('~')) # make sure is at the home directory
    
    # the following block of code get all the files in the
    # home direcotry and put them into an array
    files = (str)(check_output("ls"))
    files = files.split("b'")
    files = files[1]
    files = files.split("'")
    files = files[0]
    files = files.splitlines()
    files = files[0]
    files = files.split("\\n")

    # list inited to contain symlink
    currents = [None] * len(files)
    index = 0

    # check the files in the home directory one by one to see if is a symlink
    for i in range(0, len(files) - 1):
        re = subprocess.call(["readlink", files[i]])
        if re == 0: # if is a symlink
            current = files[i]
            # the following block of code create the row needed
            # to be printed and put it into the currents list
            # and incremet the index of the currents list by 1
            for n in range(0, 20 - len(current)):
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
            currents[index] = current
            index += 1
    
    clear_terminal() # clear terminal for a better view

    print("Current path: ", os.getcwd(),"\n\n") # show the current directory

    # the following block of code create and print the title of the report
    title = "Symbolic Link"
    for i in range (0, 13):
        title += " "
    title += "Target Path"
    print("\033[33m", title, "\033[0m\n", sep = "")

    # print the symlinks and their target path one by one
    for i in range(0, len(currents)):
        if (currents[i] != None):
            print(currents[i])
    time.sleep(2)

# the main function
def main():
    os.chdir(os.path.expanduser('~')) # make sure is at the home directory
    clear_terminal() # clear the terminal
    print_menu() # print the menu
    print("Current path: ", os.getcwd(),"\n") # print the current directory
    # asking for input
    selected = input("Plrase enter a \033[32mnumber (1, 2, or 3)\033[0m or \033[31m\"quit\"\033[0m to quit the program: ")
    while selected != "quit": # run the loop as long as the user does not want to quit
        if selected == "1": # if the user want to create a symlink
            create_link()
        elif selected == "2": # if the user want to delete a sysmlink
            delete_link()
        elif selected == "3": # if the user want to read the report
            run_report()
        else: # if user input unrecognized input
            print("Unrecognized input, please try again...\n")
        clear_terminal() # clear the terminal for better view
        print_menu() # print the menu
        print("Current path: ", os.getcwd(),"\n") # show the current directory
        # ask for input
        selected = input("Plrase enter a \033[32mnumber (1, 2, or 3)\033[0m or \033[31m\"quit\"\033[0m to quit the program: ")


main() # run the main