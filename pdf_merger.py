import os
from PyPDF2 import PdfFileMerger, PdfFileReader
from os.path import expanduser
from typing import *
import re
import pathlib
import datetime



DEV_PDFS = "./pdfs"
DEV_MODE = True


def merge_custom_order(files: List[object], path_of_dir: str, merger: PdfFileMerger) -> bool:
    """
    Merge the pdfs located at path_of_dir in a custom order which is specified by the user.
    
    For example, the string "512" will merge the fifth, first, and second files
    together in that exact order.

    Return true if the files were merged successfully, false otherwise.
    """
    print_seperator()
    order = input("Specify an order to merge in: (for example, \"132\")")
    while(not re.search("^[1-9]{2,}$", order)):
        order = input("Specify an order to merge in: (for example, \"132\")")
    
    for char in order:
        if 1 <= int(char) <= len(files) + 1:
            merger.append(PdfFileReader(files[int(char) - 1], strict=False))
        else:
            print("Error! Please try again!")
            return False
    return True

def delete_merged_files():
    pass

def print_seperator() -> None:
    """
    Prints out a visual sperator in the output window.
    """
    print("\n" + "*"*100 +  "\n") 

def choose_which_merge(files: List[object], path_of_dir: str) -> bool:
    """
    This method chooses which type of merge to do based on the user's input.
    Return true if the files at path_of_dir were successfully merged, false otherwise.
    """

    choice = input(
        """What order would you like to merge the files in? Please type the corresponding number of your choice:\n
        (1)Some or all in a custom order (ex. 132 (first, then third, then second))
        \n\t(2)All PDFs in the way they appear in the directory
        \n\t(3)All PDFS from Oldest to newest modifications
        \n\t(4)All PDFs from Newest to Oldest modifications
        \n\t(5)All PDFS from Oldest to newest creation dates
        \n\t(6)All PDFs from Newest to Oldest creation dates
        \n\t(7)All PDFs alphabetical order
        \n\t(8)All PDFs in reverse alphabetical order
               
        """)
    
    merger = PdfFileMerger(strict=False)
    success = False


    if(choice.strip() in ['1', '(1)']):
        success = merge_custom_order(files, path_of_dir, merger)
    elif(choice.strip() in ['2', '(2)']):
        success = merge_same_order_as_listed(files, path_of_dir, merger)
    elif(choice.strip() in ['3', '(3)']):
        success = merge_by_date_of_last_creation(files, path_of_dir, merger, True)
    elif(choice.strip() in ['4', '(4)']):
        success = merge_by_date_of_last_creation(files, path_of_dir, merger, False)
    elif(choice.strip() in ['5', '(5)']):
        success = merge_by_date_of_last_creation(files, path_of_dir, merger, True)
    elif(choice.strip() in ['6', '(6)']):
        success = merge_by_date_of_last_creation(files, path_of_dir, merger, False)
    elif(choice.strip() in ['7', '(7)']):
        success = merge_alphabetically(files, path_of_dir, merger, True)
    elif(choice.strip() in ['8', '(8)']):
        success = merge_alphabetically(files, path_of_dir, merger, False)
    

    if success:
        print_seperator()
        name = input("Success! Please choose a name for your new file: ")
        if not name.endswith(".pdf"):
            name += ".pdf"
        print(path_of_dir + "/" + name)
        merger.write(path_of_dir + "/" + name)

        delete_choice = input("Would you like to delete the files that were merged? (Y/N)")
        while delete_choice.lower() not in ['y', 'n']:
            delete_choice = input("Would you like to delete the files that were merged? (Y/N)")
        
        if delete_choice.lower() == 'y':
            delete_merged_files()

        return True

    print_seperator()
    print("An error occurred.")
    return False


def merge_alphabetically(files: List[object], path_of_dir: str, merger: PdfFileMerger, low_to_high:bool) -> bool:
    """
    Merge the files located at path_of_dir in alphabetic order.

    """
    if low_to_high:
        files.sort(key=lambda x: x.name)
    else:
         files.sort(key=lambda x: x.name, reverse=True)


    for file in files:
        try:
            merger.append(file)
        except:
            return False
    return True




def merge_by_date_of_last_modification(files: List[object], path_of_dir: str, merger: PdfFileMerger, old_to_new: bool) -> bool:
    """
    Merge the files located at path_of_dir in the order of the file that was more recently 
    modified to the file that was modified first if old_to_new is False, if old_to_new is True 
    then the files are merged in the opposite order. 

    """
    if(old_to_new):
        files.sort(key=lambda x: os.stat(x.name).st_mtime)
    else:
         files.sort(key=lambda x: os.stat(x.name).st_mtime, reverse=True)


    for file in files:
        try:
            merger.append(file)
        except:
            return False
    return True



def merge_same_order_as_listed(files: List[object], path_of_dir: str, merger: PdfFileMerger) -> bool:
    """
    Merge the files in the order that they are seen in the directory. 
    """

    for file in files:
        try:
            merger.append(file)
        except:
            return False
    return True


def merge_by_date_of_last_creation(files: List[object], path_of_dir: str, merger: PdfFileMerger, old_to_new: bool) -> bool:
    """
    Merge the files located at path_of_dir in the order of oldest to newest in terms of their creation dates if old_to_new is False, if 
    old_to_new is True then that aforementioned order is reversed.

    """

    
    if(old_to_new):
        files.sort(key=lambda x: os.stat(x.name).st_birthtime)
    else:
         files.sort(key=lambda x: os.stat(x.name).st_birthtime, reverse=True)


    for file in files:
        try:
            merger.append(file)
        except:
            return False
    return True



if __name__ == "__main__":
    if(not DEV_MODE):
        path_of_dir = input("Input the path of the directory which contains the pdfs you would like to use: ")
    else:
        path_of_dir = DEV_PDFS
        home = expanduser("~")

        if "~" in path_of_dir:
            path_of_dir = path_of_dir.replace("~", home)

    print("Files found: ")
    # create the file objects
    pdf_files = []
    pdf_counter = 1
    for i, filename in enumerate(os.listdir(path_of_dir)):
        if filename.endswith(".pdf"):
            complete_file_path = path_of_dir + "/" + filename
            try:
                fname = pathlib.Path(complete_file_path)
                last_modified = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
                creation_date = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
                print("\t" + str(pdf_counter) + '. ' + filename  + ". Created at " + str(creation_date) + ". Last modified at " + str(last_modified))
                pdf_files.append(open(complete_file_path, "rb"))
                pdf_counter += 1
            except:
                print("Error creating file object for file " + filename)

    

    choose_which_merge(pdf_files, path_of_dir)

        


    

    

    






