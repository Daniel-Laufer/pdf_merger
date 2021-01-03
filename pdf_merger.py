import os
from PyPDF2 import PdfFileMerger, PdfFileReader
from os.path import expanduser
from typing import *
import re


DEV_PDFS = "./pdfs"
DEV_MODE = True


def merge_custom_order(files: List[object], path_of_dir: str, merger: PdfFileMerger) -> bool:
    """
    Merge the pdfs in a custom order which is specified by the user.
    
    For example, the string "512" will merge the fifth, first, and second files
    together in that exact order.

    Return true if the files were merged successfully, false otherwise.
    """
    print_seperator()
    order = input("Specify an order to merge in: (for example, \"132\")")
    while(not re.search("^[1-9]{2,}$", order)):
        order = input("Specify an order to merge in: (for example, \"132\")")
    
    for char in order:
        print(len(files))
        if 1 <= int(char) <= len(files) + 1:
            merger.append(PdfFileReader(files[int(char) - 1], strict=False))
        else:
            print("Error! Please try again!")
            return False
    return True

def print_seperator() -> None:
    """
    Prints out a visual sperator in the output window.
    """
    print("\n" + "*"*100 +  "\n") 


def choose_which_merge(files: List[object], path_of_dir: str) -> bool:
    """
    This method chooses which type of merge to do based on the user's input.
    Return true if the files were successfully merged, false otherwise.
    """

    choice = input(
        """What order would you like to merge the files in? Please type the corresponding number of your choice:\n
        (1)Some or all in a custom order (ex. 132 (first, then third, then second))
        \n\t(2)All PDFs in the way they appear in the directory
        \n\t(3)All PDFS from Oldest to newest
        \n\t(4)All PDFs Alphabetically
        \n\t(5)All PDFs from Newest to Oldest\n        
        """)
    
    merger = PdfFileMerger(strict=False)
    
    if(choice.strip() in ['1', '(1)']):
        success = merge_custom_order(files, path_of_dir, merger)
            

    if success:
        print_seperator()
        name = input("Success! Please choose a name for your new file: ")
        if not name.endswith(".pdf"):
            name += ".pdf"
        merger.write(path_of_dir + "/" + name)
        return True
    print_seperator()
    print("An error occurred.")
    return False

        




 



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
            try:
                print("\t" + str(pdf_counter) + '. ' + filename)
                pdf_files.append(open(path_of_dir + "/" + filename, "rb"))
                pdf_counter += 1
            except:
                print("Error creating file object for file " + filename)

    
    choose_which_merge(pdf_files, path_of_dir)

        


    

    

    






