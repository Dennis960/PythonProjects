import os
import sys
import time

# get path to the directory this file is in
dir = os.path.dirname(os.path.abspath(__file__))
# go into parent directory
dir = os.path.dirname(dir)

# get a list of all folders in the parent directory
folders = os.listdir(dir)
# remove any files from the list
folders = [folder for folder in folders if os.path.isdir(os.path.join(dir, folder))]
# create a dict of the folders and their contents with the folder name as the key. The value is a list of all files in the folder with their date modified.
files = {folder: [(file, os.path.getmtime(os.path.join(dir, folder, file))) for file in os.listdir(os.path.join(dir, folder))] for folder in folders}
# convert date modified to a german readable format
files = {folder: [(file, time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(date))) for file, date in files[folder]] for folder in files}

# for each folder find the file with the earliest date modified. Save it together with the parent folder name
files = {folder: min(files[folder], key=lambda x: x[1]) for folder in files}

folder_dates = {folder: date for folder, (file, date) in files.items()}

# remove .git
folder_dates.pop(".git", None)

print(folder_dates)